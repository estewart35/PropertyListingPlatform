from django.contrib import admin
from .models import Listing, ListingImage

# Register your models here.
class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1

class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline]

admin.site.register(Listing, ListingAdmin)