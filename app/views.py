from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from app.models import *
from django.db.models import Sum

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
        
        
        Transaction.objects.create(amount=amount, description=description)
        messages.success(request, 'Transaction created successfully')
        return redirect('/')
    context={
        'transactions': Transaction.objects.all(),
        'income': Transaction.objects.filter(amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0,
        'expense': Transaction.objects.filter(amount__lte=0).aggregate(expense=Sum('amount'))['expense'] or 0,
        'balance': Transaction.objects.aggregate(balance=Sum('amount'))['balance'] or 0
    }          
    return render(request, 'index.html',context)

def deletetransaction(request,uuid):
    Transaction.objects.get(id=uuid).delete()
    return redirect('/')

