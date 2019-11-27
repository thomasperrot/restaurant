from django.contrib import admin

from .models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    fields = ["name"]


admin.site.register(Restaurant, RestaurantAdmin)
