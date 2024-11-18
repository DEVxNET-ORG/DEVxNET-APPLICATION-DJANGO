from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser,Contact
from .forms import CustomUserCreationForm

# Role Check Decorators
def is_head(user):
    return user.role == 'Head'

def is_teamleader(user):
    return user.role == 'TeamLeader'

# General Views
def index(request):
    if request.method == 'POST':
        Contact.objects.create(
            first_name=request.POST.get('firstName'),
            last_name=request.POST.get('lastName'),
            email=request.POST.get('Email'),
            subject=request.POST.get('Subject'),
            message=request.POST.get('Message')
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('thankyou')  
    return render(request, 'index.html')

def showProject(request):
    return render(request, 'Pages/showproject.html')

def thankyou(request):
    return render(request, 'Pages/thankyou.html')

def startPage(request):
    return render(request, 'Pages/startPage.html')

@login_required
def customer_list(request):
    contacts = Contact.objects.all()
    return render(request, 'components/contact.html', {'contacts': contacts})

@require_POST
@login_required
def delete_customer(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    messages.success(request, "Contact deleted successfully.")
    return redirect('customer_list')

# Custom Login View
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid credentials'})
    return render(request, 'auth/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

# Admin and Employee Dashboard
@login_required
def dashboard(request):
    if request.user.role == 'Head' or request.user.role == 'TeamLeader' or request.user.role == 'Employee':
        return render(request, 'components/base.html')

@login_required
def overall(request):
    return render(request, 'components/overall.html')

@login_required
@user_passes_test(is_head)
def create_teamleader(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'TeamLeader'
            user.save()
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'components/Management/create_teamleader.html', {'form': form})

@login_required
@user_passes_test(is_head)
def modify_teamleader(request, user_id):
    teamleader = get_object_or_404(CustomUser, id=user_id, role='TeamLeader')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=teamleader)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm(instance=teamleader)
    return render(request, 'components/Management/modify_user.html', {'form': form, 'title': 'Modify TeamLeader'})

@login_required
@user_passes_test(is_head)
def teamleader_list(request):
    teamleaders = CustomUser.objects.filter(role='TeamLeader')
    return render(request, 'components/Management/teamleader_list.html', {'teamleaders': teamleaders})

@login_required
@user_passes_test(is_head)
def delete_teamleader(request, user_id):
    teamleader = get_object_or_404(CustomUser, id=user_id, role='TeamLeader')
    teamleader.delete()
    return redirect('dashboard')

@login_required
@user_passes_test(is_teamleader)
def create_employee(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Employee'
            user.save()
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'components/Management/create_user.html', {'form': form})

@login_required
@user_passes_test(is_teamleader)
def modify_employee(request, user_id):
    employee = get_object_or_404(CustomUser, id=user_id, role='Employee')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm(instance=employee)
    return render(request, 'components/Management/modify_user.html', {'form': form, 'title': 'Modify Employee'})

@login_required
@user_passes_test(is_teamleader)
def delete_employee(request, user_id):
    employee = get_object_or_404(CustomUser, id=user_id, role='Employee')
    employee.delete()
    return redirect('dashboard')
