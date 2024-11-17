from django.urls import path
from . import views

# ===============================
# Main Pages (Public)
# ===============================
urlpatterns = [
    # Index Page
    path('', views.index, name='index'),
    # Project Page
    path('showproject/', views.showProject, name='showproject'), 
    # Thank You Page
    path('thankyou/', views.thankyou, name='thankyou'),
    # Start Page
    path('start/', views.startPage, name='startPage'),

# ===============================
# Contact Management (Admin Only)
# ===============================
    # Customer List (Admin)
    path('contact/', views.customer_list, name='customer_list'),
    # Delete Contact (Admin)
    path('contact/delete/<int:id>/', views.delete_customer, name='delete_customer'),

# ===============================
# Authentication and Dashboard
# ===============================
    # Login Page
    path('login/', views.CustomLoginView.as_view(), name='login'),
    # Logout Page
    path('logout/', views.logout_view, name='logout'),
    # Admin and Employee Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # Overall Page (Admin/Employee)
    path('overall/', views.overall, name='overall'),

# ===============================
# User Management (Admin Only)
# ===============================
    # Admin: Manage Users
    path('manage_users/', views.manage_users, name='manage_users'),
    # Admin: Edit User
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    # Admin: Manage Managers
    path('manage_managers/', views.manage_managers, name='manage_managers'),

# ===============================
# Employee Management (Manager Only)
# ===============================
    # Manager: Manage Employees
    path('manage_employees/', views.manage_employees, name='manage_employees'),
    # Manager: Create Employee
    path('create_employee/', views.create_employee, name='create_employee'),
    # Manager: Delete Employee
    path('delete_employee/<int:user_id>/', views.delete_employee, name='delete_employee'),

# ===============================
# Employee Profile (Employee Only)
# ===============================
    # Employee: View Profile
    path('view_profile/', views.view_profile, name='view_profile'),
]
