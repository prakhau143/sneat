from django.urls import path
from . import views

app_name = 'sneat_app'

urlpatterns = [
    # Unified Authentication
    path('', views.unified_login, name='unified_login'),
    path('login/', views.unified_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # User Dashboards
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('merchant/dashboard/', views.merchant_dashboard, name='merchant_dashboard'),
    
    # Super Admin URLs
    path('super-admin/dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    
    # Merchant Management
    path('super-admin/merchants/', views.merchant_list, name='merchant_list'),
    path('super-admin/merchants/add/', views.merchant_add, name='merchant_add'),
    path('super-admin/merchants/<int:merchant_id>/edit/', views.merchant_edit, name='merchant_edit'),
    path('super-admin/merchants/<int:merchant_id>/delete/', views.merchant_delete, name='merchant_delete'),
    path('super-admin/merchants/<int:merchant_id>/toggle-status/', views.merchant_toggle_status, name='merchant_toggle_status'),
    
    # Transaction Management
    path('super-admin/transactions/', views.transaction_list, name='transaction_list'),
    path('super-admin/transactions/add/', views.transaction_add, name='transaction_add'),
    
    # Reports and Settings
    path('super-admin/reports/', views.reports, name='reports'),
    path('super-admin/settings/profile/', views.settings_profile, name='settings_profile'),
    
    # Legacy redirects
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cards/', views.dashboard, name='cards'),
    path('forms/', views.dashboard, name='forms'),
    path('tables/', views.dashboard, name='tables'),
    path('ui/', views.dashboard, name='ui'),
    path('pages/', views.dashboard, name='pages'),
    path('layouts/', views.dashboard, name='layouts'),
]
