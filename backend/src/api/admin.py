from api.models import Claim, Pet, PetInsurance, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "email",
            "role",
            "is_staff",
            "is_active",
            "password1",
            "password2",
        )

    def clean(self):
        cleaned_data = super().clean()
        # Log errors to the console to see what's happening in the background
        if self.errors:
            print(f"DEBUG ADMIN ERRORS: {self.errors.as_json()}")
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("email", "role", "is_active", "is_staff")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("role",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions")


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "owner", "birth_date")
    list_filter = ("species",)
    search_fields = ("name", "owner__email")


@admin.register(PetInsurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pet",
        "owner",
        "status",
        "coverage_start",
        "coverage_end",
    )
    list_filter = ("status",)
    search_fields = ("pet__name", "owner__email")


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "insurance",
        "amount",
        "status",
        "invoice_date",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("insurance__pet__name", "insurance__owner__email")
