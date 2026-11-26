from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignUpForm


class HomeHeavenLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to HomeHeaven! Your account is ready.')
            return redirect('core:home')
        messages.error(request, 'Please correct the highlighted fields.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def dashboard(request):
    from listings.models import Property, Inquiry, SavedProperty

    profile = getattr(request.user, 'profile', None)
    is_admin = bool(profile and profile.is_admin_role)

    if is_admin:
        properties = Property.objects.all().order_by('-created_at')
        inquiries = Inquiry.objects.all().order_by('-created_at')
    else:
        properties = Property.objects.filter(owner=request.user).order_by('-created_at')
        inquiries = Inquiry.objects.filter(property__owner=request.user).order_by('-created_at')

    context = {
        'is_admin': is_admin,
        'properties': properties[:12],
        'inquiries': inquiries[:12],
        'total_properties': properties.count(),
        'total_inquiries': inquiries.count(),
        'saved_count': SavedProperty.objects.filter(user=request.user).count(),
        'profile': profile,
        'inquiry_count': Inquiry.objects.filter(user=request.user).count(),
        'property_count': Property.objects.filter(is_active=True).count(),
    }
    return render(request, 'accounts/dashboard.html', context)
