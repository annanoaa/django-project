import uuid
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View
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
        context['subtotal'] = subtotal
        context['shipping'] = 3
        context['total'] = subtotal + 3
        return context

    def get_queryset(self):
        cart = self.get_cart()
        return cart.items.all() if cart else []

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Get or create cart based on users authentication status
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
        else:
            if not created:
                cart_item.delete()

        return HttpResponseRedirect(request.POST.get('current_url', '/'))

class CheckoutView(CartListView):
    template_name = 'order/checkout.html'

    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        # If users was anonymous, transfer their cart items to their authenticated cart
        session_id = request.session.get('cart_session_id')
        if session_id:
            anonymous_cart = Cart.objects.filter(session_id=session_id).first()
            if anonymous_cart:
                user_cart, _ = Cart.objects.get_or_create(user=request.user)
                # Transfer items from anonymous cart to users cart
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

        return super().get(request, *args, **kwargs)
