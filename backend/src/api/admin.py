from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from models.user import User
from models.pet import Pet
from models.insurance import PetInsurance
from models.claim import Claim

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'owner', 'birth_date')
    list_filter = ('species',)
    search_fields = ('name', 'owner__email')

@admin.register(PetInsurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'owner', 'status', 'coverage_start', 'coverage_end')
    list_filter = ('status',)
    search_fields = ('pet__name', 'owner__email')

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('id', 'insurance', 'amount', 'status', 'invoice_date', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('insurance__pet__name', 'insurance__owner__email')
