from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', login_required(views.process_scraper), name='process_scraper'),
    path('', login_required(views.start_scraping), name='start_scraping'),
]
