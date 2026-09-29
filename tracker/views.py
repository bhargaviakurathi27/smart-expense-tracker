from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Transaction
from .forms import TransactionForm
def home(request):
    # Finds templates/tracker/home.html and returns it as a web page
    return render(request, 'tracker/home.html')
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in immediately after signup
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def transaction_list(request):
    # Only this user's transactions — never all transactions
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'tracker/transactions.html', {'transactions': transactions})


@login_required
def transaction_add(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)  # don't save yet
            transaction.user = request.user         # attach the logged-in user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'tracker/transaction_form.html', {'form': form, 'title': 'Add Transaction'})


@login_required
def transaction_edit(request, pk):
    # get_object_or_404 with user=request.user means a user editing someone
    # else's transaction ID gets a 404, not someone else's data
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'tracker/transaction_form.html', {'form': form, 'title': 'Edit Transaction'})


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted.')
        return redirect('transaction_list')
    return render(request, 'tracker/transaction_confirm_delete.html', {'transaction': transaction})