from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView, View
from django.urls import reverse_lazy
from django.db.models import F
from django.db import transaction

from store.models import Product
from .models import CartItem


class OrderCartView(LoginRequiredMixin, TemplateView):
    """
    View for displaying the shopping cart.
    Requires user authentication.
    """
    template_name = 'order/cart.html'

    def get_context_data(self, **kwargs):
        """
        Adds cart and total price information to the context.
        Optimizes calculations by using the database for totals.
        """
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})

        # Calculate totals using list comprehension for better performance
        cart_totals = [
            float(item['price']) * item['quantity']
            for item in cart.values()
        ]

        # Add computed values to context
        context.update({
            'cart': cart,
            'total_price_of_products': sum(cart_totals)
        })

        return context


class AddToCartView(LoginRequiredMixin, View):
    """
    View for adding products to the shopping cart.
    Uses atomic transactions to ensure data consistency.
    """

    def post(self, request, product_id):
        """
        Handles POST requests to add a product to cart.
        Uses atomic transaction to ensure stock and cart operations are in sync.
        """
        with transaction.atomic():
            # Get product with select_for_update to prevent race conditions
            product = get_object_or_404(
                Product.objects.select_for_update(),
                id=product_id
            )

            if product.quantity <= 0:
                messages.error(
                    request,
                    'Product is out of stock. Please choose another product.'
                )
                return redirect('category_products')

            # Get or initialize cart from session
            cart = request.session.get('cart', {})
            product_key = str(product_id)

            # Update cart in session
            if product_key in cart:
                cart[product_key]['quantity'] += 1
            else:
                cart[product_key] = {
                    'name': product.name,
                    'price': str(product.price),
                    'quantity': 1,
                    'image': str(product.image)
                }

            # Update CartItem and Product using F() expressions
            cart_item, _ = CartItem.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={'quantity': 0}
            )
            CartItem.objects.filter(id=cart_item.id).update(
                quantity=F('quantity') + 1
            )

            # Update product quantity
            Product.objects.filter(id=product_id).update(
                quantity=F('quantity') - 1
            )

            # Save cart to session
            request.session['cart'] = cart

            return redirect('order_cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    """
    View for removing products from the shopping cart.
    Uses atomic transactions to ensure data consistency.
    """

    def post(self, request, product_id):
        """
        Handles POST requests to remove a product from cart.
        Uses atomic transaction to ensure stock and cart operations are in sync.
        """
        with transaction.atomic():
            product = get_object_or_404(
                Product.objects.select_for_update(),
                id=product_id
            )
            cart = request.session.get('cart', {})
            product_key = str(product_id)

            if product_key not in cart:
                messages.error(request, "This item is not in your cart.")
                return redirect('order_cart')

            # Handle quantity reduction
            if cart[product_key]['quantity'] > 1:
                cart[product_key]['quantity'] -= 1
                CartItem.objects.filter(
                    product=product,
                    user=request.user
                ).update(quantity=F('quantity') - 1)
                messages.success(
                    request,
                    f"Reduced quantity of {product.name} in your cart."
                )
            else:
                # Remove item completely
                del cart[product_key]
                CartItem.objects.filter(
                    product=product,
                    user=request.user
                ).delete()
                messages.success(
                    request,
                    f"{product.name} has been removed from your cart."
                )

            # Update product quantity
            Product.objects.filter(id=product_id).update(
                quantity=F('quantity') + 1
            )

            request.session['cart'] = cart
            return redirect('order_cart')


class CheckoutView(LoginRequiredMixin, TemplateView):
    """
    View for displaying the checkout page.
    Requires user authentication.
    """
    template_name = 'order/checkout.html'

    def get_context_data(self, **kwargs):
        """
        Adds cart and total price information to the context.
        Uses optimized calculations for cart totals.
        """
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})

        # Calculate totals using list comprehension for better performance
        cart_totals = [
            float(item['price']) * item['quantity']
            for item in cart.values()
        ]

        # Add computed values to context
        context.update({
            'cart': cart,
            'total_price_of_products': sum(cart_totals)
        })

        return context