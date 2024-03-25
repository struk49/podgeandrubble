from django.shortcuts import render, redirect, reverse
from django.contrib import messages


from .forms import OrderForm


def checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There's nothing in your basket at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51O2vtYG3G7lKiCY6QooiFjcPA8pBvZ6Cx11nvKwOiiDEWkJD1KLQsSo71x4Kj98PlpyNiIHlGZrODT92xkzBUgxQ00LLjpnqvw',
        'client_secret': 'test clients ecret',
    }

    return render(request, template, context)