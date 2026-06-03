from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.support_home_view, name='home'),
    path('ticket/create/', views.create_ticket_view, name='create_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    path('rma/create/<int:order_item_id>/', views.create_rma_view, name='create_rma'),
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),
]
