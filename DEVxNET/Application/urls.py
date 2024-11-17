from django.urls import path
from .views import CustomLoginView, manage_users, edit_user, view_profile, dashboard, index, thankyou, showProject, startPage, customer_list, delete_customer 

urlpatterns = [
    path('', index, name='index'),
    path('/thankyou', thankyou, name='thankyou'),
    path('/showproject', showProject, name='showProject'),
    path('/startPage', startPage, name='startPage'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('manage-users/', manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('profile/', view_profile, name='view_profile'),
     path('customers/', customer_list, name='customer_list'),  
    path('delete_customer/<int:id>/', delete_customer, name='delete_customer'),  
]
