from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filters import OrderFilter

# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()


    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    
    context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'myFilter':myFilter, 'delivered':delivered, 'pending':pending }
    return render(request,'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html', {'products':products})

def customers(request, pk):
    customers = Customer.objects.get(pk=pk)
   
    orders = customers.order_set.all()
    order_count = orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customers':customers, 
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter
        }
    return render(request,'accounts/customers.html', context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)
    customers = Customer.objects.get(pk=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customers)
    
    if request.method == 'POST':
        
        formset = OrderFormSet(request.POST, instance=customers)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):

    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context =  {'forms':form}
    return render(request, 'accounts/update_ordr_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)