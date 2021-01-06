from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, CategoryItem
from django.shortcuts import redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from .forms import CheckoutFrom


from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core import mail

from django.contrib.auth.mixins import LoginRequiredMixin # buat direct ke sign inlangsung
from django.contrib.auth.decorators import login_required


class HomeView(View):

    def get(self, request):

        categoryItem = CategoryItem.objects.all()
        featuredItem = Item.objects.filter(featured = True)
        print(featuredItem)
        item = Item.objects.all()

        if request.GET.get('category_id'):

            print(request.GET.get('category_id'))


            categoryFilter = Item.objects.filter(category = request.GET.get('category_id'))
            return render(request, 'home.html', { 'category' : categoryItem, 'items': categoryFilter, 'featured' : featuredItem})

        return render(request, 'home.html', {'category' : categoryItem, 'items' : item, 'featured' : featuredItem})


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'



class OrderSummaryView(LoginRequiredMixin, View):

# class OrderSummaryView(View):
    
    def get(self, request):
        try:
            order = Order.objects.get(user =request.user, ordered = False)
            print(order)
            context = {

                'object' : order
            }

            # print(request.user.email)
            return render(request,'order-summary.html', context)
        except ObjectDoesNotExist:
            return redirect('/')


class CheckoutView(View):

    def get(self, request, *args, **kwargs):

        userOrder = Order.objects.get(user =request.user, ordered = False)
        form = CheckoutFrom()
        print(userOrder)
        return render(request, 'checkout.html', {'object' : userOrder, 'form' : form})

    def post(self, request, *args, **kwargs):

        form = CheckoutFrom(request.POST or None)
        userOrder = Order.objects.get(user =request.user, ordered = False)
        # print(request.POST)
        if form.is_valid():
            
            #send mail

            subject = 'Thank You'
            message = render_to_string('email/order_checkout.html', {

                "username" : request.user.username,
                'first_name' : form.cleaned_data.get('first_name'),
                'last_name' : form.cleaned_data.get('last_name'),
                'address' : form.cleaned_data.get('address'),
                'Phone' : form.cleaned_data.get('phone'),
                'Payment_option' : form.cleaned_data.get('payment_option'),
                'object' : userOrder,

            })
            plain_message = ''
            from_email = 'noreply@dstore.com' 
            to = request.user.email
            # print(message)
            mail.send_mail(subject, plain_message, from_email, [to], html_message=message)

            userOrder.delete()

            return redirect('order-complete')

        return redirect('checkout')

        
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_item, created = OrderItem.objects.get_or_create(
    item = item,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user = request.user,  ordered = False)
    if order_qs.exists():
        order = order_qs[0]

        # check order item is in the order

        if order.item.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            print(order_item)
            order_item.save()
            return redirect("order-summary")
            # return redirect("home")

        else:
            order.item.add(order_item)
            return redirect("order-summary")
            # return redirect("home")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.item.add(order_item)
        
    return redirect('order-summary')
    # return redirect("home")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():

            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.item.remove(order_item)
            order_item.delete()
            # messages.info(request, "This item was removed from your cart.")
            return redirect('order-summary')
        else:
            # messages.info(request, "This item was not in your cart")
            return redirect('order-summary')
    else:
        # messages.info(request, "You do not have an active order")
        return redirect('order-summary')


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():

            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity == 1:

                order.item.remove(order_item)
                order_item.delete()
                # messages.info(request, "This item was removed from your cart.")
                return redirect('order-summary')
            else:

                order_item.quantity -=1
                order_item.save()
                # messages.info(request, "This item was removed from your cart.")
                return redirect('order-summary')
        else:
            # messages.info(request, "This item was not in your cart")
            return redirect('order-summary')
    else:
        # messages.info(request, "You do not have an active order")
        return redirect('order-summary')


def OrderComplete(request):

    return render(request, 'order-complete.html')