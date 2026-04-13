from django.db import models

HOME_TYPE_CHOICES = [
    ('House', 'House'),
    ('Condo', 'Condo'),
    ('Townhouse', 'Townhouse'),
    ('Land', 'Land'),
]

CITY_CHOICES = [
    ('Omaha', 'Omaha'),
    ('Lincoln', 'Lincoln'),
    ('Bellevue', 'Bellevue'),
    ('Council Bluffs', 'Council Bluffs'),
]

STATE_CHOICES = [
    ('NE', 'Nebraska'),
    ('IA', 'Iowa'),
]

STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Sold', 'Sold'),
]

class Property(models.Model):
    address = models.CharField(max_length=255)
    home_type = models.CharField(max_length=50, choices=HOME_TYPE_CHOICES)
    city = models.CharField(max_length=100, choices=CITY_CHOICES)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    neighborhood = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    visibility = models.BooleanField(default=True)
    description = models.TextField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    garage = models.PositiveIntegerField()
    year_built = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_photos/')

    def __str__(self):
        return f"Image for {self.property.address}"
