from django.contrib import admin
from order.models import Cart


@admin.register(Cart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
    # search_fields = ('user__username',)