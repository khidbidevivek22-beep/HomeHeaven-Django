from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class City(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    state = models.CharField(max_length=80)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=18.520400)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=73.856700)
    image = models.ImageField(upload_to='cities/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Amenity(models.Model):
    CATEGORY_CHOICES = [
        ('basic', 'Basics'),
        ('comfort', 'Comfort'),
        ('safety', 'Safety'),
        ('lifestyle', 'Lifestyle'),
    ]

    name = models.CharField(max_length=60, unique=True)
    icon = models.CharField(max_length=60, default='fa-check')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='basic')

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_TYPES = [
        ('flat', 'Flat / Apartment'),
        ('pg', 'PG / Hostel'),
        ('house', 'Independent House'),
        ('villa', 'Villa'),
    ]
    FURNISHING_CHOICES = [
        ('unfurnished', 'Unfurnished'),
        ('semi', 'Semi-furnished'),
        ('fully', 'Fully furnished'),
    ]

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='properties')
    locality = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=18.520400)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=73.856700)

    rent = models.PositiveIntegerField()
    deposit = models.PositiveIntegerField(default=0)
    maintenance = models.PositiveIntegerField(default=0)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='flat')
    bedrooms = models.PositiveSmallIntegerField(default=1)
    bathrooms = models.PositiveSmallIntegerField(default=1)
    area_sqft = models.PositiveIntegerField(default=600)
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='semi')
    available_from = models.DateField(null=True, blank=True)
    lease_term = models.CharField(max_length=60, default='12 months')

    description = models.TextField()
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='properties')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties', null=True, blank=True
    )

    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    no_brokerage = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'home'
            self.slug = f'{base}-{self.id}' if self.id else base
            if Property.objects.filter(slug=self.slug).exists():
                self.slug = f'{base}-{Property.objects.count() + 1}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listings:detail', args=[self.slug])

    def cover_image(self):
        return self.images.first()

    def monthly_total(self):
        return self.rent + self.maintenance

    def rating_average(self):
        values = [r.rating for r in self.reviews.all()]
        return round(sum(values) / len(values), 1) if values else None


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    caption = models.CharField(max_length=120, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.property.title} — image {self.order + 1}'


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} · {self.rating}★ · {self.property.title}'


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('scheduled', 'Tour scheduled'),
        ('closed', 'Closed'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} → {self.property.title}'


class SavedProperty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'property'], name='unique_user_saved_property')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} saved {self.property.title}'
