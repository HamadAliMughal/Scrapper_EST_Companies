

# Register your models here.
from django.contrib import admin
from .models import MainTable

@admin.register(MainTable)
class MainTableAdmin(admin.ModelAdmin):
    list_display = ("keyword", "state", "company_name", "website")
