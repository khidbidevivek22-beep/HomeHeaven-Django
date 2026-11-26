from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.listing_list, name='list'),
    path('toggle-save/<int:property_id>/', views.toggle_save, name='toggle_save'),
    path('saved/', views.saved_list, name='saved'),
    path('compare/', views.compare, name='compare'),
    path('my-inquiries/', views.my_inquiries, name='my_inquiries'),
    path('<slug:slug>/', views.listing_detail, name='detail'),
]
