from django.urls import path
from . import views


urlpatterns = [
    # Index Page
    path('', views.index, name='index'),
    # Project Page
    path('showproject/', views.showProject, name='showProject'), 
    # Thank You Page
    path('thankyou/', views.thankyou, name='thankyou'),
    # Start Page
    path('start/', views.startPage, name='startPage'),
    
    # Customer List 
    path('contact/', views.customer_list, name='customer_list'),
    # Delete Contact 
    path('contact/delete/<int:id>/', views.delete_customer, name='delete_customer'),


    # Login Page
    path('login/', views.login_user, name='login'),
    # Logout Page
    path('logout/', views.logout_user, name='logout'),
    # Admin and Employee Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # Overall Page (Admin/Employee)
    path('overall/', views.overall, name='overall'),


    path('create-teamleader/', views.create_teamleader, name='create_teamleader'),
    path('create-employee/', views.create_employee, name='create_employee'),
    
    path('modify-teamleader/<int:user_id>/', views.modify_teamleader, name='modify_teamleader'),
    path('delete-teamleader/<int:user_id>/', views.delete_teamleader, name='delete_teamleader'), 
    
    path('modify-employee/', views.modify_employee, name='modify_employee'),
    path('delete-employee/<int:user_id>/', views.delete_employee, name='delete_employee'),    

]
