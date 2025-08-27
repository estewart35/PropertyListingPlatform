from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('listings/', views.all_listings, name='all_listings'),
    path('listings/new/', views.new_listing, name='new_listing'),
    path('listings/edit/<int:id>/', views.edit_listing, name='edit_listing'),
    path('listings/delete/<int:id>/', views.delete_listing, name='delete_listing'),
    path('listings/<int:id>/', views.listing_details, name='listing_details'),
    path('your-listings/', views.your_listings, name='your_listings'),
    path('favorite/<int:id>/', views.favorite, name='favorite'),
    path('favorites/', views.favorite_listings, name='favorite_listings'),
]