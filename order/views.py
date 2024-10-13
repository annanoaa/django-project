from django.http import HttpResponse, JsonResponse


# Home page for orders
def order_home(request):
    return HttpResponse("Welcome to the Order System! You can check your order status by visiting the status page.")


# Mock order status view
def order_status(request):
    # Get 'order_id' from query parameters (e.g., ?order_id=123)
    order_id = request.GET.get('order_id')

    if order_id:
        # Mock response for the order status
        return JsonResponse({
            'order_id': order_id,
            'status': 'Shipped' if int(order_id) % 2 == 0 else 'Processing',
            'message': f"Order {order_id} is being processed." if int(
                order_id) % 2 != 0 else f"Order {order_id} has been shipped."
        })
    else:
        return JsonResponse({
            'error': "Please provide an order_id."
        }, status=400)

