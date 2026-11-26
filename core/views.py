from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from listings.models import Property, City, Review
from .forms import ContactForm


def home(request):
    featured = Property.objects.filter(is_featured=True).select_related('owner')[:6]
    if not featured:
        featured = Property.objects.all().order_by('-created_at')[:6]
    cities = City.objects.filter(is_active=True).order_by('name')
    reviews = Review.objects.select_related('property', 'author').order_by('-created_at')[:3]
    return render(request, 'home.html', {
        'featured': featured,
        'cities': cities,
        'reviews': reviews,
    })


def about(request):
    return render(request, 'core/about.html')


def how_it_works(request):
    return render(request, 'core/how_it_works.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            if settings.EMAIL_HOST_PASSWORD:
                send_mail(
                    f'HomeHeaven enquiry from {name}',
                    f'From: {name} <{email}>\n\n{message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            messages.success(request, 'Thanks! Your message has been recorded. We will get back to you.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
