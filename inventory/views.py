from django.shortcuts import render,redirect, HttpResponse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login, logout
from .forms import CreateUserForm, CustomerCreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Models from django.contrib.auth.models import User
from django.db import transaction
from .models import Product,Category,Supplier,Customer,Order, CustomUser
import logging
from django.db.models import Sum

from django.contrib.auth import get_user_model
from django.db.models.functions import ExtractMonth
from django.db.models import Count
import json
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)
# Create your views here.

@login_required(login_url='/')
def home(request):
    return render(request, 'home/home.html')

@login_required(login_url='/')
def customer(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 15)  # Show 10 users per page

    page_obj = paginator.get_page(1)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'customer/customer.html', context)

def customerrecord(request, page):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 15)  # Show 10 users per page

    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'customer/customerrecord.html', context)

def order(request, id):
    if request.method == 'POST':
        quantity = request.POST['buy']

        product = Product.objects.get(id=id)
        product_name = product.name
        price = product.price
        total_price = price * int(quantity)
        stock = product.stock_quantity


        new_stock = stock - int(quantity)

        product.stock_quantity = new_stock
        product.save()

        order = Order(
            customer = request.user,
            product = product_name,
            total_price = total_price
        )

        order.save()

        return redirect('/customer')

def index(request):
    #Logic for registration
    if request.method == 'POST':
        form = CustomerCreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Successfully Registered "+ user)

            return redirect('/')
        
        else:
             for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
                    return redirect('/')

    #if neither a request is performed then by default render the login page
    form = CustomerCreateUserForm()
    body = {'form':form, }
    return render(request, 'login/index.html', body)


def user_login(request):

    #if form is submitted get credentials, authenticate it and find whether it matches a record, if not send error
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.usertype == 'customer':
                return redirect('/customer')
            
            elif user.usertype == 'admin':
                return redirect('/home')
            
            else:
                messages.error(request, 'Invalid USERTYPE')
                return redirect('/')
        
        else:
            messages.error(request, 'Invalid USERNAME or PASSWORD')
            return redirect('/')
        
def signout(request):
    logout(request)
    return redirect('/')





# Rendering dynamic html
@login_required(login_url='/')
def dashboard(request):
    total_price = Order.objects.aggregate(total=Sum('total_price'))
    user_count = CustomUser.objects.count()
    category_count = Category.objects.count()
    products_count = Product.objects.count()

    categories = Category.objects.all()

    category_labels = [category.name for category in categories]
    product_counts = [Product.objects.filter(category=category).count() for category in categories]


    User = get_user_model()
    user_counts_by_month = User.objects.annotate(month=ExtractMonth('date_joined')).values('month').annotate(count=Count('id'))
    data = [0] * 12

    for entry in user_counts_by_month:
        month_number = entry['month']
        count = entry['count']
        data[month_number - 1] = count 

    sales_data = Order.objects.filter(order_date__year=datetime.now().year).values('order_date__month').annotate(total_sales=Sum('total_price'))
    sales_by_month = [0] * 12  

    for entry in sales_data:
        month = entry['order_date__month']
        sales_by_month[month - 1] = entry['total_sales']


    context = {
        'usercount':user_count,
        'categorycount':category_count,
        'productscount':products_count,
        'total_price':total_price['total'],




        'category_labels': category_labels,
        'product_counts': product_counts,


        'data': data,
    }
    return render(request, 'Dashboard/Dashboard.html',context)


# user views
@login_required(login_url='/')
def users(request):
    user_list = CustomUser.objects.all()
    paginator = Paginator(user_list, 15)  # Show 10 users per page

    page_obj = paginator.get_page(1)

    form = CreateUserForm()
    context = {
        'page_obj': page_obj,
        'form':form,
    }

    
    return render(request, 'Users/User.html', context)


def adduser(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Successfully Registered "+ user)

            return redirect('/home')
        
        else:
             for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
                    return redirect('/home')

def deleteuser(request, id):
    user = CustomUser.objects.get(id=id)
    user.delete()

    return redirect('/home')

def records(request, page):
    user_list = CustomUser.objects.all()
    paginator = Paginator(user_list, 15)  # Show 10 users per page


    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'Users/records.html', context)

# end of user views


# product views
@login_required(login_url='/')
def products(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 15)  # Show 10 users per page

    page_obj = paginator.get_page(1)
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'suppliers':suppliers,

    }
    return render(request, 'Products/products.html', context)

def productsrecord(request, page):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 15)  # Show 10 users per page

    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'Products/productrecords.html', context)

@require_http_methods(["GET", "POST"])
def addproduct(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        sku = request.POST.get('sku')
        category_name = request.POST.get('category')
        supplier_name = request.POST.get('supplier') 
        stock_quantity = request.POST.get('stock')
        reorder_level = request.POST.get('reorder')
        added_by = request.user

        try:
            # Fetch Category and Supplier instances
            category = Category.objects.get(name=category_name)
            supplier = Supplier.objects.get(name=supplier_name)

            # Ensure request.user is a valid CustomUser instance
            if not isinstance(request.user, CustomUser):
                return HttpResponse('User not authenticated properly', status=400)

            # Create Product instance and save
            product = Product(
                name=name,
                price=price,
                sku=sku,
                category=category,
                supplier=supplier,
                stock_quantity=stock_quantity,
                reorder_level=reorder_level,
                created_by = added_by
            )
            product.save()

            return redirect('/home')

        except Category.DoesNotExist:
            return HttpResponse('Category does not exist', status=400)

        except Supplier.DoesNotExist:
            return HttpResponse('Supplier does not exist', status=400)



def deleteproduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()

    return redirect('/home')

def editproduct(request, id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    context = {
        'product':product,
        'categories': categories,
        'suppliers':suppliers,

    }


    return render(request, 'Products/editproduct.html', context)


def updateproduct(request, id):
    name = request.POST.get('name')
    price = request.POST.get('price')
    sku = request.POST.get('sku')
    category_name = request.POST.get('category')
    supplier_name = request.POST.get('supplier') 
    stock_quantity = request.POST.get('stock')
    reorder_level = request.POST.get('reorder')

    category = Category.objects.get(name=category_name)
    supplier = Supplier.objects.get(name=supplier_name)



    product = Product.objects.get(id=id)
    product.name = name
    product.price = price
    product.sku = sku
    product.category = category
    product.supplier = supplier
    product.stock_quantity = stock_quantity
    product.reorder_level = reorder_level

    product.save()

    return redirect('/home')


# end of product views

# start of category
@login_required(login_url='/')
def categories(request):

    category_list = Category.objects.all()
    paginator = Paginator(category_list, 15)  # Show 10 users per page

    page_obj = paginator.get_page(1)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'Categories/categories.html', context)

def categoryrecord(request, page):

    category_list = Category.objects.all()
    paginator = Paginator(category_list, 15)  # Show 10 users per page

    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'Categories/categoryrecord.html', context)

def addcategory(request):

    if request.method == 'POST':
        
        name = request.POST['name']
        description = request.POST['description']

        category = Category(name = name, description = description)
        category.save()

        return redirect('/home')

def deletecategory(request, id):

    category = Category.objects.get(id=id)

    category.delete()

    return redirect('/home')


# end of category

# start of suppliers
@login_required(login_url='/')
def suppliers(request):
    
    supplier_list = Supplier.objects.all()
    paginator = Paginator(supplier_list, 15)  # Show 10 users per page

    page_obj = paginator.get_page(1)
    context = {
        'page_obj': page_obj,
    }


    return render(request, 'Suppliers/suppliers.html', context)

def suppliersrecord(request, page):
        
    supplier_list = Supplier.objects.all()
    paginator = Paginator(supplier_list, 15)  # Show 10 users per page

    page_obj = paginator.get_page(1)
    context = {
        'page_obj': page_obj,
    }


    return render(request, 'Suppliers/suppliersrecord.html', context)

def addsuppliers(request):
    if request.method == 'POST':
        
        name = request.POST['name']
        contact_name = request.POST['contactname']
        phone = request.POST['phonenumber']
        email = request.POST['email']
        address = request.POST['address']

        supplier = Supplier(name = name, contact_name = contact_name, phone = phone, email = email, address = address)
        supplier.save()

        return redirect('/home')

def deletesuppliers(request, id):
    supplier = Supplier.objects.get(id=id)
    supplier.delete()

    return redirect('/home')

def editsuppliers(request, id):
    supplier = Supplier.objects.get(id=id)
    context = {
        'supplier':supplier,
    }


    return render(request, 'Suppliers/editsuppliers.html', context)

def updatesuppliers(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        contact_name = request.POST['contactname']
        phone = request.POST['phonenumber']
        email = request.POST['email']
        address = request.POST['address']

        supplier = Supplier.objects.get(id=id)
        supplier.name = name
        supplier.contact_name = contact_name
        supplier.phone = phone
        supplier.email = email
        supplier.address = address

        supplier.save()
        return redirect('/home')

# end of suppliers
@login_required(login_url='/')
def orders(request):
    return render(request, 'Orders/orders.html')