from django.urls import path
from . import views


urlpatterns = [
	path('search_google/', views.search_google)
]