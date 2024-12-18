from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .forms import TransactionForm

# Home Page
def index(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user)
        return render(request, 'income_expense/index.html', {'transactions': transactions})
    return render(request, 'income_expense/welcome.html')

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'income_expense/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'income_expense/login.html')

# User Logout
def user_logout(request):
    logout(request)
    return redirect('index')

# Add Transaction
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('index')
    else:
        form = TransactionForm()
    return render(request, 'income_expense/add_transaction.html', {'form': form})

# Edit Transaction
@login_required
def edit_transaction(request, pk):
    transaction = Transaction.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'income_expense/edit_transaction.html', {'form': form})

# Delete Transaction
@login_required
def delete_transaction(request, pk):
    transaction = Transaction.objects.get(pk=pk, user=request.user)
    transaction.delete()
    return redirect('index')

# Summary View
@login_required
def summary(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    total_expense = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    balance = total_income - total_expense
    return render(request, 'income_expense/summary.html', {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
    })