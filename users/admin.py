from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomUserCreationForm
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_active_datetime')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = UserAdmin.fieldsets + (
        ('Activity Info', {'fields': ('last_active_datetime',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('email',)}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-last_active_datetime',)