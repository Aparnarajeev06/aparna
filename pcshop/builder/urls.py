from django.urls import path
from . import views

app_name = 'builder'

urlpatterns = [
    path('', views.pc_builder_view, name='configurator'),
    path('select/<slug:category_slug>/', views.select_part_view, name='select_part'),
    path('add/<int:product_id>/', views.add_part_to_build_view, name='add_part'),
    path('remove/<str:part_type>/', views.remove_part_from_build_view, name='remove_part'),
    path('add-to-cart/', views.add_build_to_cart_view, name='add_to_cart'),
    path('ai-recommendation/', views.ai_recommendation_view, name='ai_recommendation'),
]
