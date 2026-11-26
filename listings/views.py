from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Property, PropertyImage, City, Amenity, SavedProperty, Inquiry, Review
from .forms import InquiryForm


CITY_COORDS = {
    'Pune': (18.5204, 73.8567),
    'Mumbai': (19.0760, 72.8777),
    'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867),
}


def _int(value, default=None):
    try:
        return int(value) if value not in (None, '') else default
    except (TypeError, ValueError):
        return default


def listing_list(request):
    qs = Property.objects.filter(is_active=True).select_related('city').prefetch_related('images', 'amenities')

    q = request.GET.get('q', '').strip()
    city = request.GET.get('city', '').strip()
    property_type = request.GET.get('property_type', '').strip()
    min_rent = _int(request.GET.get('min_rent'))
    max_rent = _int(request.GET.get('max_rent'))
    bedrooms = _int(request.GET.get('bedrooms'))
    furnishing = request.GET.get('furnishing', '').strip()
    amenity_ids = request.GET.getlist('amenities')
    verified = request.GET.get('verified') == '1'
    no_brokerage = request.GET.get('no_brokerage') == '1'
    sort = request.GET.get('sort', 'recommended')

    if q:
        qs = qs.filter(
            Q(title__icontains=q) | Q(locality__icontains=q) |
            Q(city__name__icontains=q) | Q(address__icontains=q)
        )
    if city:
        qs = qs.filter(city__slug=city)
    if property_type:
        qs = qs.filter(property_type=property_type)
    if min_rent is not None:
        qs = qs.filter(rent__gte=min_rent)
    if max_rent is not None:
        qs = qs.filter(rent__lte=max_rent)
    if bedrooms:
        qs = qs.filter(bedrooms__gte=bedrooms)
    if furnishing:
        qs = qs.filter(furnishing=furnishing)
    if amenity_ids:
        for aid in amenity_ids:
            qs = qs.filter(amenities__id=aid)
    if verified:
        qs = qs.filter(is_verified=True)
    if no_brokerage:
        qs = qs.filter(no_brokerage=True)

    if sort == 'rent_low':
        qs = qs.order_by('rent')
    elif sort == 'rent_high':
        qs = qs.order_by('-rent')
    elif sort == 'newest':
        qs = qs.order_by('-created_at')
    elif sort == 'area':
        qs = qs.order_by('-area_sqft')
    else:
        qs = qs.order_by('-is_featured', '-created_at')

    qs = qs.distinct()
    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    map_items = []
    for p in qs[:60]:
        map_items.append({
            'id': p.id,
            'title': p.title,
            'locality': p.locality,
            'city': p.city.name,
            'rent': p.rent,
            'lat': float(p.latitude),
            'lng': float(p.longitude),
            'url': p.get_absolute_url(),
        })

    saved_ids = []
    if request.user.is_authenticated:
        saved_ids = list(SavedProperty.objects.filter(user=request.user).values_list('property_id', flat=True))

    context = {
        'page_obj': page_obj,
        'properties': page_obj.object_list,
        'cities': City.objects.filter(is_active=True).order_by('name'),
        'amenities': Amenity.objects.all().order_by('category', 'name'),
        'filters': {
            'q': q, 'city': city, 'property_type': property_type,
            'min_rent': request.GET.get('min_rent', ''),
            'max_rent': request.GET.get('max_rent', ''),
            'bedrooms': request.GET.get('bedrooms', ''),
            'furnishing': furnishing, 'amenities': [int(a) for a in amenity_ids if a.isdigit()],
            'verified': verified, 'no_brokerage': no_brokerage, 'sort': sort,
        },
        'map_items': map_items,
        'saved_ids': saved_ids,
        'default_center': CITY_COORDS.get(
            (City.objects.filter(slug=city).first().name if city else 'Pune') or 'Pune',
            CITY_COORDS['Pune']
        ),
    }
    return render(request, 'listings/list.html', context)


def listing_detail(request, slug):
    prop = get_object_or_404(
        Property.objects.select_related('city', 'owner').prefetch_related('images', 'amenities', 'reviews'),
        slug=slug, is_active=True
    )
    prop.views += 1
    Property.objects.filter(pk=prop.pk).update(views=prop.views)

    images = prop.images.all()
    reviews = prop.reviews.select_related('author').all()
    similar = Property.objects.filter(city=prop.city, is_active=True).exclude(pk=prop.pk).select_related('city').prefetch_related('images')[:3]

    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedProperty.objects.filter(user=request.user, property=prop).exists()

    form = InquiryForm(initial={
        'name': request.user.get_full_name() or request.user.username if request.user.is_authenticated else '',
        'email': request.user.email if request.user.is_authenticated else '',
    })

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, 'Please log in to send an enquiry.')
            return redirect(f'/accounts/login/?next={prop.get_absolute_url()}')
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = prop
            inquiry.user = request.user
            inquiry.save()
            messages.success(request, 'Enquiry sent! The owner will contact you shortly.')
            return redirect(prop.get_absolute_url())

    return render(request, 'listings/detail.html', {
        'property': prop,
        'images': images,
        'reviews': reviews,
        'similar': similar,
        'is_saved': is_saved,
        'form': form,
        'map_center': (float(prop.latitude), float(prop.longitude)),
    })


@login_required
def toggle_save(request, property_id):
    if request.method != 'POST':
        return JsonResponse({'saved': False, 'message': 'POST required.'}, status=405)

    prop = get_object_or_404(Property, pk=property_id, is_active=True)
    saved = SavedProperty.objects.filter(user=request.user, property=prop).first()
    if saved:
        saved.delete()
        return JsonResponse({'saved': False, 'message': 'Removed from saved homes.'})
    SavedProperty.objects.create(user=request.user, property=prop)
    return JsonResponse({'saved': True, 'message': 'Saved to your homes.'})


@login_required
def saved_list(request):
    items = Property.objects.filter(saved_by__user=request.user, is_active=True).select_related('city').prefetch_related('images')
    return render(request, 'listings/saved.html', {'properties': items})


@login_required
def compare(request):
    ids = request.GET.getlist('id')
    items = Property.objects.filter(pk__in=ids, is_active=True).prefetch_related('images', 'amenities')
    return render(request, 'listings/compare.html', {'properties': items})


@login_required
def my_inquiries(request):
    items = Inquiry.objects.filter(user=request.user).select_related('property').order_by('-created_at')
    return render(request, 'listings/my_inquiries.html', {'inquiries': items})
