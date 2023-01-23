from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from restaurant.models import *
from restaurant.forms import CategoryForm,ProductForm,ModifierGroupForm,ModifierForm




@login_required()
def dashboard(request):
    return render(request,'restaurant/dashboard.html')


#Product Views
class ProductList(LoginRequiredMixin,ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'restaurant/product/products.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm 
    success_url = reverse_lazy('restaurant:products')
    template_name = 'restaurant/product/create-product.html'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm 
    success_url = reverse_lazy('restaurant:products')
    template_name = 'restaurant/product/create-product.html'

class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('restaurant:products')
    template_name = 'restaurant/product/delete-product.html'

#Category Views
class CategoryList(LoginRequiredMixin,ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'restaurant/category/category_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm 
    success_url = reverse_lazy('restaurant:categories')
    template_name = 'restaurant/category/category_form.html'


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm 
    success_url = reverse_lazy('restaurant:categories')
    template_name = 'restaurant/category/category_form.html'


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('restaurant:categories')
    template_name = 'restaurant/category/delete-category.html'


#ModifierGroup Views
class MGList(LoginRequiredMixin,ListView):
    model = ModifierGroup
    context_object_name = 'modifiergroups'
    template_name = 'restaurant/modifiergroup/modifiergroup_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MGCreate(LoginRequiredMixin, CreateView):
    model = ModifierGroup
    form_class = ModifierGroupForm 
    success_url = reverse_lazy('restaurant:modifiergroups')
    template_name = 'restaurant/modifiergroup/modifiergroup_form.html'

class MGUpdate(LoginRequiredMixin, UpdateView):
    model = ModifierGroup
    form_class = ModifierGroupForm 
    success_url = reverse_lazy('restaurant:modifiergroups')
    template_name = 'restaurant/modifiergroup/modifiergroup_form.html'

    

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

    







    


