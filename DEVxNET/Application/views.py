from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from .models import CustomUser, EmployeeProfile, Contact
from .forms import CustomUserForm, EmployeeProfileForm
from django.contrib import messages
from django.urls import reverse_lazy

# Check Role Decorators
def is_manager(user):
    return user.is_authenticated and user.is_manager()

def is_admin(user):
    return user.is_authenticated and user.is_admin()

def is_employee(user):
    return user.is_authenticated and user,is_employee()

def index(request):
    if request.method == 'POST':
        fname = request.POST.get('firstName')
        lname = request.POST.get('lastName')
        email = request.POST.get('Email')
        subject = request.POST.get('Subject')
        message = request.POST.get('Message')
        
        # Using Django ORM to save data
        Contact.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('thankyou')  
        
    return render(request, 'index.html')

def showProject(request):
    return render(request, 'showproject.html')

def thankyou(request):
    messages.success(request, 'We Got your message..')
    return render(request, 'thankyou.html')

def startPage(request):
    return render(request, 'startPage.html')

def customer_list(request):
    contacts = Contact.objects.all()  
    return render(request, 'contact.html', {'contacts': contacts})

def delete_customer(request, id):
    contact = Contact.objects.get(id=id)  
    if request.method == 'POST':
        contact.delete()  
        messages.success(request, "Contact deleted successfully.")  
        return redirect('customer_list')  
    return HttpResponse(status=405)  




class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Override to redirect users based on their role."""
        response = super().form_valid(form)  
        
        user = self.request.user
        if user.role == 'admin':
            return redirect('manage_users')  
        elif user.role == 'manager':
            return redirect('dashboard')  
        elif user.role == 'employee':
            return redirect('view_profile')  

        return response  
def logout_view(request):
    if request.user.is_authenticated:
        request.session.flush()
        messages.success(request, "You have been logged out successfully.")
    return redirect('login')

# Admin and Employee Dashboard
@login_required
def dashboard(request):
    return render(request, 'base.html')

def overall(request):
    return render(request, 'overall.html')

# Admin View: Manage Users
@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'user_management/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    form = CustomUserForm(instance=user)
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'{user.username} account updated successfully.')
            return redirect('manage_users')
    
    return render(request, 'user_management/edit_user.html', {'form': form, 'user': user})


# Employee View: View Profile
@login_required
@user_passes_test(is_employee)
def view_profile(request):
    profile = get_object_or_404(EmployeeProfile, user=request.user)
    return render(request, 'user_management/view_profile.html', {'profile': profile})


@user_passes_test(is_admin)
def manage_managers(request):
    managers = CustomUser.objects.filter(role='manager')
    return render(request, 'admin/manage_managers.html', {'managers': managers})

@user_passes_test(is_manager)
def manage_employees(request):
    employees = CustomUser.objects.filter(role='employee')
    return render(request, 'manager/manage_employees.html', {'employees': employees})

@user_passes_test(is_manager)
def create_employee(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee account created successfully.')
            return redirect('manage_employees')
    else:
        form = CustomUserForm()

    return render(request, 'manager/create_employee.html', {'form': form})

@user_passes_test(is_manager)
def delete_employee(request, user_id):
    employee = get_object_or_404(CustomUser, id=user_id, role='employee')
    employee.delete()
    messages.success(request, f'Employee {employee.username} deleted successfully.')
    return redirect('manage_employees')