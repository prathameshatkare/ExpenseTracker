from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm
from .models import Expense
import datetime
from django.db.models import Sum

def index(request):
    if request.method == "POST":
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense_form.save()
            return redirect('index')  # Prevents form resubmission on refresh
    
    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    today = datetime.date.today()
    
    # Time-based expense calculations
    time_frames = {
        "yearly": today - datetime.timedelta(days=365),
        "monthly": today - datetime.timedelta(days=30),
        "weekly": today - datetime.timedelta(days=7),
    }

    filtered_sums = {
        key: Expense.objects.filter(date__gt=value).aggregate(Sum('amount'))['amount__sum'] or 0
        for key, value in time_frames.items()
    }

    daily_sums = Expense.objects.values('date').annotate(sum=Sum('amount')).order_by('date')
    categorical_sums = Expense.objects.values('category').annotate(sum=Sum('amount')).order_by('category')

    expense_form = ExpenseForm()
    return render(request, 'myapp/index.html', {
        'expense_form': expense_form,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'yearly_sum': filtered_sums['yearly'],
        'monthly_sum': filtered_sums['monthly'],
        'weekly_sum': filtered_sums['weekly'],
        'daily_sums': daily_sums,
        'categorical_sums': categorical_sums
    })

def edit(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    return render(request, 'myapp/edit.html', {'expense_form': ExpenseForm(instance=expense)})

def delete(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == 'POST' and 'delete' in request.POST:
        expense.delete()
    return redirect('index')

from django.db.models import Sum
from django.contrib.humanize.templatetags.humanize import intcomma

total_expenses = Expense.objects.aggregate(Sum('amount'))

print(total_expenses)  # Debugging
print(intcomma(total_expenses['amount__sum']))  # Debugging
