from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from .models import CustomUser, EmployeeProfile, Contact
from .forms import CustomUserForm, EmployeeProfileForm
from django.contrib import messages

# Check Role Decorators
def is_admin(user):
    return user.role == 'admin'

def is_employee(user):
    return user.role == 'employee'

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

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            # Redirect both admin and employee to the dashboard
            if self.request.user.role in ['admin', 'employee']:
                return redirect('dashboard')
        return super().form_valid(form)


# Admin and Employee Dashboard
@login_required
def dashboard(request):
    try:
        profile = request.user.employee_profile
    except EmployeeProfile.DoesNotExist:
        profile = None

    users = CustomUser.objects.all() if request.user.role == 'admin' else None

    return render(request, 'dashboard.html', {
        'profile': profile,
        'users': users
    })

# Admin View: Manage Users
@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'user_management/manage_users.html', {'users': users})

# Admin View: Edit User
@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    form = CustomUserForm(instance=user)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    return render(request, 'user_management/edit_user.html', {'form': form})

# Employee View: View Profile
@login_required
@user_passes_test(is_employee)
def view_profile(request):
    profile = get_object_or_404(EmployeeProfile, user=request.user)
    return render(request, 'user_management/view_profile.html', {'profile': profile})
