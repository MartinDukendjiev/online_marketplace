from django.contrib import admin
from .models import MarketplaceUser, Rating, Comment


class MarketplaceUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'average_rating']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'receiver', 'value']
    list_filter = ['value']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'seller_profile', 'timestamp']
    search_fields = ['user__username', 'seller_profile__username']


admin.site.register(MarketplaceUser, MarketplaceUserAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Comment, CommentAdmin)
