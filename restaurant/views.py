from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
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

@login_required
def create_or_update_product(request, pid=None):
    product = get_object_or_404(Product, pid=pid) if pid else None
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            form.save_m2m()
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

    







    


