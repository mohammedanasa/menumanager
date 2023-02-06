from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from restaurant.models import *
from restaurant.forms import *
import requests
import base64
import json
from base64 import b64encode
from django.views import View
from urllib.parse import urlencode




@login_required()
def dashboard(request):
    return render(request,'restaurant/dashboard.html')


#Product Views

@login_required
def create_or_update_product(request, pid=None):
    product = get_object_or_404(Product, pid=pid) if pid else None
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            category = form.cleaned_data.get('category')
            product.catprods.set(form.cleaned_data.get('category'))
            product.save()
            messages.success(request, 'Product has been successfully saved')
            return redirect('restaurant:update-product',pid=product.pid)
    else:
        form = ProductForm(instance=product)
    return render(request, 'restaurant/product/create-product.html', {'form': form})

class ProductList(LoginRequiredMixin,ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'restaurant/product/products.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



@login_required
def delete_product(request, pid):
    product = get_object_or_404(Product, pid=pid)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'product has been successfully deleted')

        return redirect('restaurant:products')
    return render(request, 'restaurant/product/delete-product.html', {'product': product})

#Category Views
@login_required
def create_or_update_category(request, cid=None):
    category = get_object_or_404(Category, cid=cid) if cid else None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = request.user
            category.save()
            messages.success(request, 'Category has been successfully saved')
            return redirect('restaurant:update-category',cid=category.cid)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'restaurant/category/category_form.html', {'form': form})

class CategoryList(LoginRequiredMixin,ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'restaurant/category/category_list.html'

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user) 

@login_required
def delete_category(request, cid):
    category = get_object_or_404(Category, cid=cid)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category has been successfully deleted')

        return redirect('restaurant:categories')
    return render(request, 'restaurant/category/delete-category.html', {'category': category})


#ModifierGroup Views
class MGList(LoginRequiredMixin,ListView):
    model = ModifierGroup
    context_object_name = 'modifiergroups'
    template_name = 'restaurant/modifiergroup/modifiergroup_list.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return ModifierGroup.objects.filter(owner=self.request.user)

class MGCreate(LoginRequiredMixin, CreateView):
    model = ModifierGroup
    form_class = ModifierGroupForm 
    success_url = reverse_lazy('restaurant:modifiergroups')
    template_name = 'restaurant/modifiergroup/modifiergroup_form.html'

class MGUpdate(LoginRequiredMixin, UpdateView):
    model = ModifierGroup
    form_class = ModifierGroupForm 
    template_name = 'restaurant/modifiergroup/modifiergroup_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('restaurant:update-mg', kwargs={'slug': self.object.slug})

    

class MGDelete(LoginRequiredMixin, DeleteView):
    model = ModifierGroup
    fields = '__all__'
    success_url = reverse_lazy('restaurant:modifiergroups')
    template_name = 'restaurant/modifiergroup/delete_modifiergroup.html'



#Modifiers Views
class ModifierList(LoginRequiredMixin,ListView):
    model = Modifier
    context_object_name = 'modifiers'
    template_name = 'restaurant/modifier/modifier_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ModifierCreate(LoginRequiredMixin, CreateView):
    model = Modifier
    form_class = ModifierForm 
    success_url = reverse_lazy('restaurant:modifiers')
    template_name = 'restaurant/modifier/modifier_form.html'


class ModifierUpdate(LoginRequiredMixin, UpdateView):
    model = Modifier
    form_class = ModifierForm 
    success_url = reverse_lazy('restaurant:modifiers')
    template_name = 'restaurant/modifier/modifier_form.html'


class ModifierDelete(LoginRequiredMixin, DeleteView):
    model = Modifier
    fields = '__all__'
    success_url = reverse_lazy('restaurant:modifiers')
    template_name = 'restaurant/modifier/delete_modifier.html'


#----------------------------------------RESTAURANT--------------------------------------#

#List all the restaurants
def restaurant_list(request):
    user = request.user
    restaurants = Restaurant.objects.filter(owner=user)
    context = {'restaurants': restaurants}
    return render(request, 'restaurant/restaurant/restaurant-list.html', context)

#Single restaurant view
def get_restaurant(request, lid):
    restaurant = get_object_or_404(Restaurant, lid=lid)
    print(restaurant)
    menus = Menu.objects.filter(restaurant=restaurant)
    print(menus)
    return render(request, 'restaurant/restaurant/menu-list.html', {'restaurant': restaurant,'menus':menus})


#create or update address
def update_restaurant_address(request, lid):
    restaurant = get_object_or_404(Restaurant, lid=lid)
    address = restaurant.address
    form = AddressForm(instance=address)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.owner = request.user
            address.save()
            restaurant.address = address
            restaurant.save()
            return redirect('restaurant:update_address', lid=restaurant.lid)
        else:
            form = AddressForm(instance=address)
    return render(request, 'restaurant/restaurant/address.html', {'form': form})


#-----------------------------------------------------MENU-------------------------------------#

#List All Global Menus
def menu_list_view(request):
    menus = Menu.objects.all()
    return render(request, 'restaurant/menu/menus.html', {'menus': menus})

#Create Menu Globally
def menu_create_view(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.owner = request.user
            menu.save()
            form.save_m2m()
            return redirect('menu_update', menuid=menu.menuid)
    else:
        form = MenuForm()
    return render(request, 'restaurant/menu/menu-form.html', {'form': form})

#Update Menu Globally
def menu_update_view(request, menuid):
    menu = get_object_or_404(Menu, menuid=menuid)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('restaurant:menu_update', menuid=menu.menuid)
    else:
        form = MenuForm(instance=menu)
    return render(request, 'restaurant/menu/menu-form.html', {'form': form})






#--------------------------------------------------TEST---------------------------------------------#
#WooCommerce Test - SUCCESS
def fetch_products(request):

    '''# Make a GET request to the WooCommerce API to retrieve a list of products
    url = 'https://wa.biancouk.com/wp-json/wc/v3/products'

    # API credentials
    consumer_key = "ck_aca584ab9f02508a1ecfefe9020f7fa83e1ad079".encode("utf-8")
    consumer_secret = "cs_147ff37c0c4b41dae34d7cb749bd4d3af73dce69".encode("utf-8")'''

    # Make a GET request to the WooCommerce API to retrieve a list of products
    url = 'https://biancouk.co/wp-json/wc/v3/products'

    # API credentials
    consumer_key = "ck_3e0cc714929b9ce86ddc683fb8283d2c44e7b134".encode("utf-8")
    consumer_secret = "cs_7531e791f346a099bc1f97b465d71a9f6639eeea".encode("utf-8")

    
    # API request headers
    headers = {
        "Authorization": "Basic " + base64.b64encode(consumer_key + b":" + consumer_secret).decode("utf-8"),
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    products = response.json()

    # Check if the request was successful
    if response.status_code == 200:
        # Display the product data
        products = response.json()
        print(json.dumps(products, indent=4))

    else:
        # Display an error message
        print("Failed to retrieve product data. Response code:", response.status_code)
        
    # Render the list of products in a template
    return render(request, 'restaurant/woo.html', {'products': products})



#Display all the products & categories for the ACTIVE MENU under one location
def restaurant_menus(request, lid):
    restaurant = get_object_or_404(Restaurant, pk=lid)
    print(restaurant)
    menu = Menu.objects.get(restaurant=restaurant, is_active=True)
    print(menu)
    categories = Category.objects.filter(menu=menu)
    print(categories)
    categories_data = []
    for category in categories:
        products = Product.objects.filter(catprods=category)
        category_data = {
            'id': category.cid,
            'name': category.name,
            'products': [
                {
                    'id': product.pid,
                    'name': product.name,
                    'price': product.price,
                } for product in products
            ]
        }
        categories_data.append(category_data)
        print(categories_data)
    context = {'categories_data': categories_data}
    
    return render(request, 'restaurant/store/demo.html', context )

#Create menu for a single location
def create_menu_location(request, lid):
    restaurant = get_object_or_404(Restaurant, lid=lid)
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.owner = request.user
            menu.save()
            form.save_m2m()
            restaurant.menu.add(menu)
            return redirect('restaurant:restaurant', lid=restaurant.lid)
    else:
        form = MenuForm()
    return render(request, 'restaurant/restaurant/menu/menu-form.html', {'form': form})

#Update the menu for a single restaurant
def update_menu(request, lid, menuid):
    restaurant = get_object_or_404(Restaurant, lid=lid)
    menu = get_object_or_404(Menu, menuid=menuid)

    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.owner = request.user
            menu.save()
            form.save_m2m()
            messages.success(request, 'Menu has been successfully saved')

            return redirect('restaurant:restaurant', lid=restaurant.lid)
    else:
        form = MenuForm(instance=menu)

    return render(request, 'restaurant/restaurant/menu/menu-form.html', {'form': form})


#Single menu products and categories
def menu_detail(request, menuid):
    menu = get_object_or_404(Menu, pk=menuid)
    categories = Category.objects.filter(menu=menu)
    categories_data = []
    for category in categories:
        products = Product.objects.filter(catprods=category)
        category_data = {
            'id': category.cid,
            'name': category.name,
            'products': [
                {
                    'id': product.pid,
                    'name': product.name,
                    'price': product.price,
                } for product in products
            ]
        }
        categories_data.append(category_data)
    context = {'categories_data': categories_data}
    return render(request, 'restaurant/store/demo.html', context)


#TESTING ORDER RECIEVE WEBHOOK TEST SUCCESS
from django.http import JsonResponse
@csrf_exempt
def webhook_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        # Extract the relevant information from the data
        customer_name = data.get("customer", {}).get("name")
        customer_email = data.get("customer", {}).get("email")
        delivery_address = data.get("deliveryAddress", {}).get("street")
        payment_amount = data.get("payment", {}).get("amount")
        items = data.get("items", [])
        order_id = data.get("channelOrderId")
        pickup_time = data.get("pickupTime")
        # Store the order data in a dictionary
        order_data = {
            "customer_name": customer_name,
            "order_id": order_id
        }

        # Print the order information
        print("Order ID: ", order_id)
        print("Customer Name: ", customer_name)
        print("Customer Email: ", customer_email)
        print("Delivery Address: ", delivery_address)
        print("Payment Amount: ", payment_amount)
        print("Pickup Time: ", pickup_time)
        print("Items: ")
        for item in items:
            item_name = item.get("name")
            item_price = item.get("price")
            item_quantity = item.get("quantity")
            print("\t", item_name, "-", item_quantity, "x", item_price)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request method'})









