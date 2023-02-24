from django.contrib import admin
from .models import User, Address
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, OtpCode


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        ('Main', {'fields': ('email', 'phone_number', 'full_name', 'password', 'avatar')}),
        ('Permissions',
         {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name', 'password1', 'password2', 'avatar')}),
    )
    search_fields = ('email', 'fullname')
    ordering = ('full_name',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
admin.register(Address)(admin.ModelAdmin)
