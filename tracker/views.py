from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Transaction
from .forms import TransactionForm
from django.db.models import Sum
from django.utils import timezone
from .models import Budget
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
@login_required
def dashboard(request):
    user = request.user
    today = timezone.now()

    all_transactions = Transaction.objects.filter(user=user)

    # aggregate() runs SUM in the database; the "or 0" handles a brand-new
    # account with no transactions yet, where the sum would be None
    total_income = all_transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = all_transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses

    this_month = all_transactions.filter(date__year=today.year, date__month=today.month)
    month_income = this_month.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    month_expenses = this_month.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

    # Look up this month's budget, if the user has set one
    budget = Budget.objects.filter(user=user, month=today.month, year=today.year).first()
    budget_amount = budget.amount if budget else 0
    remaining_budget = budget_amount - month_expenses

    recent_transactions = all_transactions[:5]  # already ordered newest-first by the model's Meta

    # Expenses grouped by category, for the pie chart
    category_data = (
        this_month.filter(transaction_type='expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    category_labels = [item['category__name'] for item in category_data]
    category_totals = [float(item['total']) for item in category_data]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'month_income': month_income,
        'month_expenses': month_expenses,
        'budget_amount': budget_amount,
        'remaining_budget': remaining_budget,
        'recent_transactions': recent_transactions,
        'category_labels': category_labels,
        'category_totals': category_totals,
    }
    return render(request, 'tracker/dashboard.html', context)