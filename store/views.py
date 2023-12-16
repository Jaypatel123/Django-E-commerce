from django.shortcuts import render
import requests
from . models import Category, Product
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def fetch_and_display_product(request):
    api_url = "https://fakestoreapi.com/products"
    # api_url = 'https://fakestoreapi.com/products/1'
    response = requests.get(api_url)

    if response.status_code == 200:
        products_data = response.json()
        # Save the fetched data to the database
        for product_data in products_data:
            Product.objects.create(
                title=product_data['title'],
                price=product_data['price'],
                description=product_data['description'],
                category=product_data['category'],
                image=product_data['image'],
                rate=product_data['rating']['rate'],
                count=product_data['rating']['count']
            )
        all_products = Product.objects.all()
        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(all_products, 10)
        try:
            paginated_products = paginator.page(page)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = paginator.page(paginator.num_pages)
        # Render a template with the fetched data
        return render(request, 'store/store.html', {'paginated_products': paginated_products})

    # Handle errors appropriately
    return render(request, 'store/store.html')

# def store(request):
#     all_products = Product.objects.all()
#     context = {'my_products':all_products}
#     return render(request, 'store/store.html', context)

def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/list-category.html', {'category':category, 'products':products})

def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {'product': product}
    return render(request, 'store/product-info.html', context)







