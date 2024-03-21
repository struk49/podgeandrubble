from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product



def view_basket(request):
    """ A view that renders the basket contents page """

    return render(request, 'basket/basket.html')

def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the shopping basket """

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
            else:
                basket[item_id]['items_by_color'][color] = quantity
        else:
            basket[item_id] = {'items_by_color': {color: quantity}}
    else:
        if item_id in list(basket.keys()):
            bag[item_id] += quantity
        else:
            basket[item_id] = quantity

    request.session['basket'] = basket
    return redirect(redirect_url)
    

def adjust_basket(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    color = None
    if 'product_color' in request.POST:
        color = request.POST['product_color']
    basket = request.session.get('basket', {})

    if color:
        if quantity > 0:
            basket[item_id]['items_by_color'][color] = quantity
        else:
            del basket[item_id]['items_by_color'][color]
            if not basket[item_id]['items_by_color']:
                basket.pop(item_id)
    else:
        if quantity > 0:
            basket[item_id] = quantity
        else:
            basket.pop(item_id)

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, item_id):
    """Remove the item from the shopping basket"""

    try:
        color = None
        if 'product_size' in request.POST:
            color = request.POST['product_color']
        basket = request.session.get('basket', {})

        if color:
            del bag
            sket[item_id]['items_by_color'][color]
            if not basket[item_id]['items_by_color']:
                basket.pop(item_id)
        else:
            basket.pop(item_id)

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)