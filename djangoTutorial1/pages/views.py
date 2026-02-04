from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms 
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View 
from django.urls import reverse

# Create your views here.
class HomePageView(TemplateView):
 template_name = 'pages/home.html'
class AboutPageView(TemplateView):
 template_name = 'pages/about.html'

 def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "This is an about page ...",
        "author": "Developed by: Your Name",
    })
    return context
 

class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contact - Online Store"
        context["subtitle"] = "Contact information"
        context["email"] = "pepitomartines@gmail.com"
        context["phone"] = "+57 313 123 4567"
        context["address"] = "742 Evergreen Street, Springfield, USA"
        return context
    
class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 456.78},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 123.45},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 67.89},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 23.45}
    ]


class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            index = int(id) - 1

            # validar rango
            if index < 0 or index >= len(Product.products):
                return HttpResponseRedirect(reverse('home'))

            product = Product.products[index]

        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {}
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)
    
    


class ProductForm(forms.Form): 
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero"
            )

        return price
 
 
class ProductCreateView(View): 
    template_name = 'products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request):
        form = ProductForm(request.POST)

        if form.is_valid():

            new_product = {
                "id": str(len(Product.products) + 1),
                "name": form.cleaned_data["name"],
                "description": "No description",
                "price": form.cleaned_data["price"]
            }

            Product.products.append(new_product)

            return render(request,"products/success.html",{"message": "Product created"})

        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form

        return render(request, self.template_name, viewData)