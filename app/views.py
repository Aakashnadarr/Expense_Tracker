from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from app.models import *
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def register(request):
   if request.method == 'POST':
       first_name = request.POST.get('first_name')
       last_name = request.POST.get('last_name')
       email = request.POST.get('email')
       username = request.POST.get('username')
       password = request.POST.get('password')
       user_object= User.objects.filter(
           Q(username=username) | Q(email=email)
       )
       
       if user_object.exists():
           messages.error(request, 'Error:Username or Email already exists')
           return redirect('/register/')
       user_object = User.objects.create_user(
           first_name=first_name,
           last_name=last_name,
           email=email,
           username=username,
           
       )
       user_object.set_password(password)
       user_object.save()
       messages.success(request, 'Success:Account created successfully')
       return redirect('/login/')
   else:
       return render(request, 'register.html')   
def login_page(request):
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_object = User.objects.filter(
                username=username,
            ) 
            if not user_object.exists():
                messages.error(request, 'Error:Username does not exist')
                return redirect('/login/')
            user_object = authenticate(
                username=username,
                password=password
            )
            if not user_object:
                messages.error(request, 'Error:Invalid credentials')
                return redirect('/login/')
            
            login(request, user_object)
            messages.success(request, 'Success:Logged in successfully')
            return redirect('/')
        else:
            return render(request, 'login.html')
def logout_page(request):
    logout(request)
    messages.success(request, 'Success:Logged out successfully')
    return redirect('/login/')

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print(request.POST)
        amount = request.POST.get('amount')
        # if amount is None:
            # messages.info(request, 'Amount is required')
            # return redirect('/')
        description = request.POST.get('description')
        if description.strip() == '':
            messages.info(request, 'Description is required')
            return redirect('/')
         
        

        Transaction.objects.create(amount=amount, description=description, created_by=request.user)
        messages.success(request, 'Transaction created successfully')
        # created_by = request.user
        return redirect('/')
    context={
        'transactions': Transaction.objects.filter(created_by=request.user),
        'income': Transaction.objects.filter(amount__gte=0, created_by=request.user).aggregate(income=Sum('amount'))['income'] or 0,
        'expense': Transaction.objects.filter(amount__lte=0, created_by=request.user).aggregate(expense=Sum('amount'))['expense'] or 0,
        'balance': Transaction.objects.filter(created_by=request.user).aggregate(balance=Sum('amount'))['balance'] or 0
    }
    return render(request, 'index.html',context)
@login_required(login_url='/login/')
def deletetransaction(request,uuid):
    Transaction.objects.get(id=uuid).delete()
    return redirect('/')

