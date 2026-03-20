from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SeekerProfile, OwnerProfile

# 1. Define Inlines so profiles appear inside the User page
class SeekerProfileInline(admin.StackedInline):
    model = SeekerProfile
    can_delete = False
    verbose_name_plural = 'Seeker Profile'

class OwnerProfileInline(admin.StackedInline):
    model = OwnerProfile
    can_delete = False
    verbose_name_plural = 'Owner Profile'

# 2. Extend the base UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Display these columns in the list view
    list_display = ('username', 'email', 'role', 'is_verified', 'is_staff', 'created_at')
    
    # Add filters on the right sidebar
    list_filter = ('role', 'is_verified', 'is_staff', 'is_superuser')
    
    # Fields to show when editing a User
    # We add your custom fields (role, phone, id_card, etc.) to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile Info', {
            'fields': (
                'role', 
                'phone_number', 
                'address', 
                'profile_picture', 
                'id_card', 
                'is_verified', 
                'verification_date'
            )
        }),
    )

    # This logic ensures the correct Inline shows up based on the user's role
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        
        inlines = []
        if obj.role == 'SEEKER':
            inlines = [SeekerProfileInline]
        elif obj.role == 'OWNER':
            inlines = [OwnerProfileInline]
        
        return [inline(self.model, self.admin_site) for inline in inlines]

# 3. Optional: Register profiles separately if you want to access them directly
@admin.register(SeekerProfile)
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_location', 'otp_created_at')
    search_fields = ('user__username', 'user__email')

@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name')
    search_fields = ('user__username', 'business_name')