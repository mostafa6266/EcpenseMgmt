from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Category , Expense
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from userpreferences.models import UserPrefernce
import datetime
import json
# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user) 
        data = expenses.values()    
        return JsonResponse(list(data), safe=False)
        

@login_required(login_url='/authenitcation/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    try:
        currency = UserPrefernce.objects.get(user=request.user).currency
    except UserPrefernce.DoesNotExist:
        currency = None  # Replace with your default currency

    context = {
        'categories': categories,
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
            'categories' : categories,
            'values':request.POST,
        }
    if request.method == 'GET':
        
        return render(request , 'expenses/add_expenses.html' , context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']
        
        
        if not amount:
            messages.error(request , 'Amount is requitrd')
            return render(request , 'expenses/add_expenses.html' , context)
        if not description:
            messages.error(request , 'description is requitrd')
            return render(request , 'expenses/add_expenses.html' , context)
        if not date:
            messages.error(request , 'date is requitrd')
            return render(request , 'expenses/add_expenses.html' , context)
        Expense.objects.create(amount = amount , owner = request.user , date = date , description = description , category = category)
        
        messages.success(request , 'Expense saved successfully')
        
        return redirect ('expenses')
    
    
def expense_edit(request , id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories,
    }
    if request.method == 'GET':
        return render (request , 'expenses/expense-edit.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']
        
        
        if not amount:
            messages.error(request , 'Amount is requitrd')
            return render(request , 'expenses/expense-edit.html' , context)
        if not description:
            messages.error(request , 'description is requitrd')
            return render(request , 'expenses/expense-edit.html' , context)
        if not date:
            messages.error(request , 'date is requitrd')
            return render(request , 'expenses/expense-edit.html' , context)
        expense.amount = amount
        expense.owner = request.user 
        expense.date = date 
        expense.description = description 
        expense.category = category
        expense.save()
        messages.success(request , 'Expense Updated successfully')
        
        return redirect ('expenses')
    
    
def expense_delet(request , id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request , 'Expense Removed successfully')
    return redirect ('expenses')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

    
def stats_view(request):
    return render(request, 'expenses/stats.html')