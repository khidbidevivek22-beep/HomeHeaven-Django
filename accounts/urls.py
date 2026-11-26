from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeHeavenLoginView, signup, dashboard

app_name = 'accounts'

urlpatterns = [
    path('login/', HomeHeavenLoginView.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='core:home'), name='logout'),
]
