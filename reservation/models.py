from django.db import models
from accounts.models import *

class Property(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    location = models.CharField(max_length=200)

    bedrooms = models.IntegerField()

    bathrooms = models.IntegerField()

    area = models.IntegerField(help_text="Size in square meters")

    image = models.ImageField(upload_to="property_images/")

    created_at = models.DateTimeField(auto_now_add=True)


class Reservation(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    seeker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    visit_date = models.DateField()

    visit_time = models.TimeField()

    message = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.property.title} - {self.seeker.username}"

class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="property_images/"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"