from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login_user, name='login'),
    path('api/profile/', views.get_user_profile, name='profile'),
    
    # Admin endpoints (for approval workflow)
    path('api/pending-users/', views.get_pending_users, name='pending_users'),
    path('api/approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    
    # Protected endpoint example
    path('api/protected/', views.protected_endpoint, name='protected'),
    
    # Information submission and approval endpoints
    path('api/submit-info/', views.submit_info, name='submit_info'),
    path('api/pending-info/', views.get_pending_info, name='pending_info'),
    path('api/active-info/', views.get_active_info, name='active_info'),
    path('api/approve-info/<int:info_id>/', views.approve_info, name='approve_info'),
    path('api/reject-info/<int:info_id>/', views.reject_info, name='reject_info'),
    path('api/my-submissions/', views.get_my_submissions, name='my_submissions'),
]