from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='list'),
    path('live-search/', views.live_search_view, name='live_search'),
    path('<slug:slug>/', views.product_detail_view, name='detail'),
    path('<int:product_id>/add-review/', views.add_review_view, name='add_review'),
    path('<int:product_id>/toggle-wishlist/', views.toggle_wishlist_view, name='toggle_wishlist'),
]
