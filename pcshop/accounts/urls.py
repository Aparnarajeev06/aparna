from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('address/add/', views.add_address_view, name='add_address'),
    path('address/<int:address_id>/delete/', views.delete_address_view, name='delete_address'),
    path('address/<int:address_id>/default/', views.make_default_address_view, name='make_default_address'),
]
