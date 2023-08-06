from django.contrib import admin

from .models import RateLimit


@admin.register(RateLimit)
class RateLimitAdmin(admin.ModelAdmin):
    list_display = (
        "system",
        "user",
        "api_method",
        "limit",
        "window",
    )
    fields = (
        "system",
        "user",
        "api_method",
        "limit",
        "window",
    )
    search_fields = (
        "system",
        "user",
        "api_method",
    )
