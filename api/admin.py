from django.contrib import admin
from .models import Role, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'patronimic', 'role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')


admin.site.register(Role)
admin.site.register(User)
