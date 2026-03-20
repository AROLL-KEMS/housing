from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('SEEKER', 'Property Seeker'),
        ('OWNER', 'Property Owner'),
    )

    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES
    )

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    id_card = models.ImageField(
        upload_to='id_cards/'
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    
    verification_date = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"
    
class SeekerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seeker_profile'
    )

    preferred_location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    otp = models.CharField(max_length=6, null=True, blank=True)
    
    otp_created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Seeker: {self.user.username}"
    
class OwnerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='owner_profile'
    )

    business_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Owner: {self.user.username}"