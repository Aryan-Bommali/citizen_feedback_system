from django.urls import path
from . import views

urlpatterns = [
     path('', views.landing, name='landing'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    path('profile/', views.profile_page, name='profile'),

    path('feedback/<int:pk>/', views.feedback_detail, name='feedback_detail'),

    path('update-feedback-status/<int:feedback_id>/', views.update_feedback_status, name='update_feedback_status'),
    path('feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),

]
