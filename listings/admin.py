from django.contrib import admin
from .models import City, Amenity, Property, PropertyImage, Review, Inquiry, SavedProperty


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'state')


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon')
    list_filter = ('category',)
    search_fields = ('name',)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'locality', 'rent', 'property_type', 'is_verified', 'is_featured')
    list_filter = ('city', 'property_type', 'furnishing', 'is_verified', 'is_featured', 'no_brokerage')
    search_fields = ('title', 'locality', 'address', 'city__name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'author', 'rating', 'created_at')
    list_filter = ('rating',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'property__title')


admin.site.register(SavedProperty)
