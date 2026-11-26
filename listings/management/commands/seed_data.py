import os
from datetime import date, timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import Profile
from listings.models import City, Amenity, Property, PropertyImage, Review, Inquiry


CITIES = [
    ('Pune', 'pune', 'Maharashtra', Decimal('18.520400'), Decimal('73.856700')),
    ('Mumbai', 'mumbai', 'Maharashtra', Decimal('19.076000'), Decimal('72.877700')),
    ('Bangalore', 'bangalore', 'Karnataka', Decimal('12.971600'), Decimal('77.594600')),
]

AMENITIES = [
    ('Wi-Fi', 'fa-wifi', 'basic'),
    ('Air conditioning', 'fa-snowflake', 'comfort'),
    ('Parking', 'fa-car', 'basic'),
    ('In-unit laundry', 'fa-washing-machine', 'comfort'),
    ('Kitchen', 'fa-kitchen-set', 'basic'),
    ('Balcony', 'fa-sun', 'lifestyle'),
    ('Security guard', 'fa-shield-halved', 'safety'),
    ('CCTV', 'fa-video', 'safety'),
    ('Lift', 'fa-arrow-up', 'basic'),
    ('Gym', 'fa-dumbbell', 'lifestyle'),
    ('Pet friendly', 'fa-paw', 'lifestyle'),
    ('Furnished', 'fa-couch', 'comfort'),
]

PROPERTIES = [
    ('Sunshine Residency', 'pune', 'Koregaon Park', 18500, 37000, 1500, 'flat', 2, 2, 980, 'fully', True, True, 'Bright 2BHK near Koregaon Park with a balcony, modular kitchen and covered parking. Walkable to cafes, parks and the metro.'),
    ('Green View Apartment', 'pune', 'Baner', 14200, 28400, 1200, 'flat', 2, 1, 850, 'semi', True, False, 'Calm apartment in Baner with green views, 24x7 security and easy access to the highway and IT parks.'),
    ('The Banyan House', 'pune', 'Kalyani Nagar', 26500, 53000, 2000, 'house', 3, 3, 1450, 'fully', True, True, 'Independent house with a private terrace, two car parks and a small garden. Ideal for a family looking for space.'),
    ('Studio Nest PG', 'pune', 'Viman Nagar', 9500, 19000, 800, 'pg', 1, 1, 320, 'fully', False, False, 'Fully furnished PG room for working professionals with Wi-Fi, housekeeping and a shared lounge.'),
    ('Riverwalk Villa', 'pune', 'Kharadi', 34000, 68000, 2500, 'villa', 3, 3, 1800, 'fully', True, True, 'Premium villa in a gated community with a private garden, gym access and a quiet neighbourhood.'),
    ('Casa Lavelle', 'pune', 'Camp', 21000, 42000, 1600, 'flat', 2, 2, 1020, 'semi', True, False, 'Heritage-style apartment in a prime central location with high ceilings and excellent connectivity.'),
    ('Skyline Flat', 'pune', 'Aundh', 16800, 33600, 1300, 'flat', 2, 2, 910, 'semi', False, False, 'Well-maintained flat close to schools, supermarkets and the Aundh retail strip.'),
    ('Cozy Corner Room', 'pune', 'Shivaji Nagar', 8200, 16400, 700, 'pg', 1, 1, 260, 'fully', False, False, 'Affordable furnished room near the railway station, suitable for students and interns.'),

    ('Sea Breeze Apartment', 'mumbai', 'Bandra West', 52000, 104000, 3500, 'flat', 2, 2, 1100, 'fully', True, True, 'Bright apartment near Bandra with sea views, lift, security and walking distance to cafes and the station.'),
    ('Harbour View Flat', 'mumbai', 'Powai', 38500, 77000, 2800, 'flat', 2, 2, 960, 'semi', True, False, 'Lake-facing flat in Powai with a balcony, gym access and excellent connectivity to business parks.'),
    ('The Palm Villa', 'mumbai', 'Juhu', 78000, 156000, 5000, 'villa', 4, 4, 2400, 'fully', True, True, 'Luxury villa near Juhu beach with private parking, terrace and round-the-clock security.'),
    ('Andheri Studio', 'mumbai', 'Andheri West', 27500, 55000, 2000, 'flat', 1, 1, 620, 'fully', False, False, 'Compact studio apartment near the metro, ideal for a single professional or couple.'),
    ('Greenfield Residency', 'mumbai', 'Navi Mumbai', 22000, 44000, 1700, 'flat', 2, 1, 870, 'semi', True, False, 'Family-friendly building with a playground, parking and quick access to the expressway.'),
    ('City Light PG', 'mumbai', 'Dadar', 13500, 27000, 1000, 'pg', 1, 1, 300, 'fully', False, False, 'Managed PG near Dadar station with meals, Wi-Fi and housekeeping included.'),

    ('Silicon Valley Flat', 'bangalore', 'Koramangala', 32000, 64000, 2400, 'flat', 2, 2, 1050, 'fully', True, True, 'Modern 2BHK in Koramangala with a workstation, balcony and close proximity to startups and cafes.'),
    ('Gardenia Home', 'bangalore', 'Indiranagar', 28500, 57000, 2100, 'flat', 2, 2, 980, 'semi', True, False, 'Quiet apartment on a tree-lined street with parking, lift and excellent metro connectivity.'),
    ('The Oak House', 'bangalore', 'Whitefield', 41000, 82000, 3000, 'house', 3, 3, 1600, 'fully', True, True, 'Independent house in Whitefield with a home office, garden and two covered parking spots.'),
    ('Lakeview Studio', 'bangalore', 'HSR Layout', 19500, 39000, 1500, 'flat', 1, 1, 610, 'fully', False, False, 'Furnished studio near HSR Layout with lake views, Wi-Fi and easy access to the ring road.'),
    ('Tech Park PG', 'bangalore', 'Electronic City', 11000, 22000, 900, 'pg', 1, 1, 280, 'fully', False, False, 'Budget PG for tech professionals with shuttle access, Wi-Fi and 24x7 security.'),
]


class Command(BaseCommand):
    help = 'Seed HomeHeaven with realistic demo data.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding HomeHeaven Django data...')

        city_objs = {}
        for name, slug, state, lat, lng in CITIES:
            city, _ = City.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'state': state, 'latitude': lat, 'longitude': lng, 'is_active': True},
            )
            city_objs[slug] = city

        for name, icon, category in AMENITIES:
            Amenity.objects.get_or_create(name=name, defaults={'icon': icon, 'category': category})

        admin_user, _ = User.objects.get_or_create(
            username='suchit',
            defaults={'email': 'suchit@example.com', 'is_staff': True, 'is_superuser': True},
        )
        if not admin_user.check_password(os.environ["HOMEHEAVEN_ADMIN_PASSWORD"]):
            admin_user.set_password(os.environ["HOMEHEAVEN_ADMIN_PASSWORD"])
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
        admin_profile, _ = Profile.objects.get_or_create(user=admin_user)
        admin_profile.role = 'admin'
        admin_profile.save()

        tenant, _ = User.objects.get_or_create(username='anu', defaults={'email': 'anu@example.com'})
        if not tenant.check_password(os.environ.get("HOMEHEAVEN_TENANT_PASSWORD", os.urandom(32).hex())):
            tenant.set_password(os.environ.get("HOMEHEAVEN_TENANT_PASSWORD", os.urandom(32).hex()))
            tenant.save()
        tenant_profile, _ = Profile.objects.get_or_create(user=tenant)
        tenant_profile.role = 'tenant'
        tenant_profile.save()

        image_dir = os.path.join(settings.MEDIA_ROOT, 'listings')
        image_files = []
        if os.path.isdir(image_dir):
            image_files = sorted([
                f for f in os.listdir(image_dir)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
            ])

        amenity_objs = list(Amenity.objects.all())
        created = 0
        for index, data in enumerate(PROPERTIES):
            title, city_slug, locality, rent, deposit, maintenance, ptype, beds, baths, area, furnishing, verified, featured, description = data
            city = city_objs[city_slug]
            slug = f'{title.lower().replace(" ", "-")}-{index + 1}'
            prop, made = Property.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'city': city,
                    'locality': locality,
                    'address': f'{locality}, {city.name}, {city.state}',
                    'latitude': city.latitude + Decimal(str(round((index % 5) * 0.012, 6))),
                    'longitude': city.longitude + Decimal(str(round((index % 4) * 0.014, 6))),
                    'rent': rent,
                    'deposit': deposit,
                    'maintenance': maintenance,
                    'property_type': ptype,
                    'bedrooms': beds,
                    'bathrooms': baths,
                    'area_sqft': area,
                    'furnishing': furnishing,
                    'available_from': date.today() + timedelta(days=(index % 4) * 7),
                    'lease_term': '12 months' if beds > 1 else '6 months',
                    'description': description,
                    'owner': admin_user,
                    'is_verified': verified,
                    'is_featured': featured,
                    'no_brokerage': True,
                    'is_active': True,
                    'views': 40 + index * 7,
                },
            )
            if made:
                created += 1
                prop.amenities.set(amenity_objs[:6 + (index % 5)])
                if image_files:
                    for img_index in range(3):
                        filename = image_files[(index * 3 + img_index) % len(image_files)]
                        PropertyImage.objects.create(
                            property=prop,
                            image=f'listings/{filename}',
                            caption=f'{title} â€” view {img_index + 1}',
                            order=img_index,
                        )

        review_texts = [
            'Great location and the photos matched the flat exactly. The team replied quickly.',
            'Clean, well-maintained and genuinely broker-free. The rent breakdown was clear.',
            'I saved this home, booked a tour and moved in within a week. Smooth process.',
            'Good value for the area. Parking and security were the deciding factors for me.',
        ]
        for i, text in enumerate(review_texts):
            prop = Property.objects.all()[i % Property.objects.count()]
            Review.objects.get_or_create(
                property=prop,
                author=tenant if i % 2 == 0 else admin_user,
                defaults={'rating': 5 if i < 3 else 4, 'comment': text},
            )

        Inquiry.objects.get_or_create(
            property=Property.objects.first(),
            user=tenant,
            name='Anu Sharma',
            email='anu@example.com',
            defaults={
                'phone': '+91 98765 43210',
                'message': 'Is this home still available for a 12-month lease?',
                'status': 'new',
            },
        )
        Inquiry.objects.get_or_create(
            property=Property.objects.all()[1],
            user=admin_user,
            name='Suchit Patil',
            email='suchit@example.com',
            defaults={
                'phone': '+91 98765 11111',
                'message': 'Please confirm the security deposit amount.',
                'status': 'contacted',
            },
        )

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete: {created} new properties, {City.objects.count()} cities, '
            f'{Amenity.objects.count()} amenities, {Property.objects.count()} total listings.'
        ))


