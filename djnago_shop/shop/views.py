from django.shortcuts import render, redirect
from .models import Product
from loguru import logger
# Create your views here.


def index(request):
    """роут главной страницы"""
    products = Product.objects.all()[:3]
    return render(request, "index.html", {"products": products})


def catalog(request):
    """роут катлога """
    sort = request.GET.get('sort', 'date')
    if sort == "price":
        products = Product.objects.all().order_by("price")
    else:
        products = Product.objects.all().order_by("created_at")

    return render(request, "shop.html", {"products": products})


def delete(request, id):
    """роут удаления товара по id"""
    product = Product.objects.get(pk=id)

    product.delete()

    return redirect("/catalog")


def delete_by_art(request):
    """роут удаления товара по артикулу"""
    product = Product.objects.filter(arcticule=request.POST.get("art")).first()
    if product:
        product.delete()

    return redirect("/catalog")


def detail(request, id):
    """роут детальной страницы товара"""
    product = Product.objects.get(pk=id)

    return render(request, "shop-single.html", {"product": product})
