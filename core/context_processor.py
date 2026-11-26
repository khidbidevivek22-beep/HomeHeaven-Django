from listings.models import Property, City


def site_stats(request):
    return {
        'site_total_properties': Property.objects.count(),
        'site_cities': City.objects.filter(is_active=True).order_by('name'),
    }
