from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_basket(request):
    """ A view that renders the basket contents page """

    return render(request, 'basket/basket.html')

def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the shopping basket """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    color = None
    if 'product_color' in request.POST:
        color = request.POST['product_color']
    basket = request.session.get('basket', {})

    if color:
        if item_id in list(basket.keys()):
            if color in basket[item_id]['items_by_color'].keys():
                basket[item_id]['items_by_color'][color] += quantity
                messages.success(request, f'Updated color {color.upper()} {product.name} quantity to {basket[item_id]["items_by_color"][color]}')
            else:
                basket[item_id]['items_by_color'][color] = quantity
                messages.success(request, f'Added color {color.upper()} {product.name} to your basket')
        else:
            basket[item_id] = {'items_by_color': {color: quantity}}
            messages.success(request, f'Added color {color.upper()} {product.name} to your basket')
    else:
        if item_id in list(basket.keys()):
            basket[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {basket[item_id]}')
        else:
            basket[item_id] = quantity
            messages.success(request, f'Added {product.name} to your basket')

    request.session['basket'] = basket
    return redirect(redirect_url)
    

def adjust_basket(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    color = None
    if 'product_color' in request.POST:
        color = request.POST['product_color']
    basket = request.session.get('basket', {})

    if color:
        if quantity > 0:
            basket[item_id]['items_by_color'][color] = quantity
            messages.success(request, f'Updated color {color.upper()} {product.name} quantity to {basket[item_id]["items_by_color"][color]}')
        else:
            del basket[item_id]['items_by_color'][color]
            if not basket[item_id]['items_by_color']:
                basket.pop(item_id)
            messages.success(request, f'Removed color {color.upper()} {product.name} from your basket')
    else:
        if quantity > 0:
            basket[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {basket[item_id]}')
        else:
            basket.pop(item_id)
            messages.success(request, f'Removed {product.name} from your basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, item_id):
    """Remove the item from the shopping basket"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        color = None
        if 'product_color' in request.POST:
            color = request.POST['product_color']
        basket = request.session.get('basket', {})

        if color:
            del basket[item_id]['items_by_color'][color]
            if not basket[item_id]['items_by_color']:
                basket.pop(item_id)
            messages.success(request, f'Removed color {color.upper()} {product.name} from your basket')
        else:
            basket.pop(item_id)
            messages.success(request, f'Removed {product.name} from your basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)