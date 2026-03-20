from django import forms
from .models import *


class ReservationForm(forms.ModelForm):

    class Meta:

        model = Reservation

        fields = [
            "visit_date",
            "visit_time",
            "message"
        ]

        widgets = {

            "visit_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "visit_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            )
        }

#========================#
class PropertyForm(forms.ModelForm):

    class Meta:

        model = Property

        fields = [
            "title",
            "location",
            "price",
            "bedrooms",
            "area",
            "image",
            "bathrooms",
            "description",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Property title"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Property location"
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Price"
                }
            ),

            "area": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Area in m²"
                }
            ),

            "bedrooms": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "image": forms.FileInput(attrs={
                "class": "form-control"
            }),

            "bathrooms": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe the property..."
                }
            ),
        }

        def clean_price(self):

            price = self.cleaned_data.get("price")

            if price <= 0:
                raise forms.ValidationError(
                    "Price must be greater than zero."
                )

            return price

#=============================================#
class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "phone_number",
            "address",
            "profile_picture",
        ]

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "readonly": "readonly"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "profile_picture": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }