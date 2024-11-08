import uuid
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, View
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from order.models import CartItem, Cart
from django.shortcuts import render, get_object_or_404
from store.models import Product


class CartListView(ListView):
    model = CartItem
    template_name = 'order/cart.html'
    context_object_name = 'cart_items'

    def get_cart(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            return cart

        session_id = self.request.session.get('cart_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            self.request.session['cart_session_id'] = session_id

        cart, _ = Cart.objects.get_or_create(session_id=session_id)
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.request.user
        cart_items = self.get_queryset()
        subtotal = sum(item.get_total() for item in cart_items)
        shipping = 3  # You might want to make this configurable

        context.update({
            'subtotal': subtotal,
            'shipping': shipping,
            'total': subtotal + shipping,
            'page_title': _('Shopping Cart'),
            'cart_labels': {
                'product': _('Product'),
                'price': _('Price'),
                'quantity': _('Quantity'),
                'total': _('Total'),
                'subtotal': _('Subtotal'),
                'shipping': _('Shipping'),
                'grand_total': _('Grand Total'),
                'empty_cart': _('Your cart is empty'),
                'continue_shopping': _('Continue Shopping'),
                'proceed_to_checkout': _('Proceed to Checkout')
            }
        })
        return context

    def get_queryset(self):
        cart = self.get_cart()
        return cart.items.all() if cart else []


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        try:
            # Get or create cart based on user's authentication status
            if request.user.is_authenticated:
                cart, _ = Cart.objects.get_or_create(user=request.user)
            else:
                session_id = request.session.get('cart_session_id')
                if not session_id:
                    session_id = str(uuid.uuid4())
                    request.session['cart_session_id'] = session_id
                cart, _ = Cart.objects.get_or_create(session_id=session_id)

            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if quantity > 0:
                if not created:
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, _('%(product)s added to cart successfully') % {'product': product.name})
            else:
                if not created:
                    cart_item.delete()
                    messages.info(request, _('%(product)s removed from cart') % {'product': product.name})

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'cart_count': cart.items.count(),
                    'message': _('Cart updated successfully')
                })

            return HttpResponseRedirect(request.POST.get('current_url', '/'))

        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': _('Error updating cart')
                }, status=400)
            messages.error(request, _('Error updating cart'))
            return HttpResponseRedirect(request.POST.get('current_url', '/'))


class CheckoutView(CartListView):
    template_name = 'order/checkout.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': _('Checkout'),
            'checkout_labels': {
                'payment_method': _('Payment Method'),
                'first_name': _('First Name'),
                'last_name': _('Last Name'),
                'email': _('Email'),
                'phone': _('Phone'),
                'address': _('Address'),
                'same_as_billing': _('Same as billing address'),
                'place_order': _('Place Order'),
                'order_summary': _('Order Summary')
            }
        })
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to proceed with checkout')
            return HttpResponseRedirect(self.login_url)

        # If user was anonymous, transfer their cart items to their authenticated cart
        session_id = request.session.get('cart_session_id')
        if session_id:
            anonymous_cart = Cart.objects.filter(session_id=session_id).first()
            if anonymous_cart:
                user_cart, _ = Cart.objects.get_or_create(user=request.user)
                # Transfer items from anonymous cart to user's cart
                for item in anonymous_cart.items.all():
                    existing_item = user_cart.items.filter(product=item.product).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.save()
                    else:
                        item.cart = user_cart
                        item.save()
                anonymous_cart.delete()
                del request.session['cart_session_id']
                messages.success(request, _('Your cart has been transferred to your account'))

        return super().get(request, *args, **kwargs)