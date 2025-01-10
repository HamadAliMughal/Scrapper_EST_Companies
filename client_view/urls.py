# client_view/urls.py

from django.urls import path
from . import views

app_name = 'client_view'  # This defines the namespace for this app's URLs

urlpatterns = [
    path('', views.view_data, name='view_data'),
    path('update_visited/<int:record_id>/', views.update_visited, name='update_visited'),
]
