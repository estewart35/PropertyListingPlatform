from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Listing(models.Model):
    PROPERTY_TYPES = [
        ('AP', 'Apartment'),
        ('HS', 'House'),
        ('ST', 'Studio'),
        ('CN', 'Condo'),
    ]
    STATUS_CHOICES = [
        ('A', 'Available'),
        ('P', 'Pending'),
        ('C', 'Closed'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    favorited_by = models.ManyToManyField(User, related_name='favorite_listings', blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=2, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"
    

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="listing_images/")

    def __str__(self):
        return f"Image for {self.listing.title} - {self.listing.location}"