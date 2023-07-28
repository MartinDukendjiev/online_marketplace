from django.contrib import admin
from .models import MarketplaceUser, Rating, Comment


# Custom admin class for MarketplaceUser
class MarketplaceUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'average_rating']  # Display these fields in the list view
    search_fields = ['username', 'email']  # Add search fields for username and email
    list_filter = ['is_staff', 'is_superuser']  # Add filters for is_staff and is_superuser fields


# Custom admin class for Rating
class RatingAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'receiver', 'value']  # Display these fields in the list view
    list_filter = ['value']  # Add filter for the 'value' field


# Custom admin class for Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'seller_profile', 'timestamp']  # Display these fields in the list view
    search_fields = ['user__username', 'seller_profile__username']  # Add search fields for user and seller_profile


# Register the models with the custom admin classes
admin.site.register(MarketplaceUser, MarketplaceUserAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Comment, CommentAdmin)
