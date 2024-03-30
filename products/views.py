from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models import Avg


from .models import Product, Category, ProductReview

from .forms import ProductForm, ProductReviewForm, ProduceForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)


    if request.method == 'POST':
        product_review_form = ProductReviewForm(data=request.POST)
        if product_review_form.is_valid():
            # Create Review object but don't save to database yet
            new_review = product_review_form.save(commit=False)
            # Assign the current review to the product
            new_review.product_id = product
            # Save the review to the database
            new_review.save()
            product_review_form = ProductReviewForm()
            messages.success(request, 'Successfully posted your review.')

            if 'last_item' in request.session:
                del request.session['last_item']

    else:
        product_review_form = ProductReviewForm()

    product_reviews = ProductReview.objects.filter(product_id_id=product_id)

    if product_reviews:
        average_score = round(product_reviews.all().aggregate(
                        Avg('rating_score'))['rating_score__avg'], 1)
        average_score_percentage = average_score/9*100
    else:
        average_score = "-"
        average_score_percentage = 0

    context = {
        'product': product,
        'product_reviews': product_reviews,
        'product_review_form': product_review_form,
        'average_score': average_score,
        'average_score_percentage': average_score_percentage,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def delete_review(request, review_pk):
    """
    Delete a review posted by the user
    """
    review = get_object_or_404(ProductReview, pk=review_pk)
    product_id = review.product_id.pk
    review.delete()

    if 'last_item' in request.session:
        del request.session['last_item']

    messages.success(request,
                     'Succesfully deleted your review.')
    return redirect(product_detail, product_id)


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProduceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProduceForm()
        
    template = 'products/add_produce.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProduceForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_produce.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


def delete_product(request, product_id):
    """ Delete a product from the store """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))