from decimal import Decimal
from django.conf import settings

def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0

    if total < settings.FREE_DELIVERY_THRESHOLD:

        # Check if the standard delivery is more than the minimum delivery cost
        if ((total / Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)) <
                Decimal(settings.MINIMUM_DELIVERY_CHARGE) and total > 0):
            delivery = Decimal(settings.MINIMUM_DELIVERY_CHARGE)
        else:
            delivery = total / Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total
    
    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context