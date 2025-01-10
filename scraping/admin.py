from django.contrib import admin
from .models import Company

@admin.register(Company)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ("Company_Name", "Website", "Created_At")
