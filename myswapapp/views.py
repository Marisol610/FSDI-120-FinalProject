from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms import inlineformset_factory
from django.contrib import admin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Product, User, Order, Chat, Messages, Profile, OrderProduct, Address, Basket
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView
from .forms import PaymentForm, ProfilePageForm, OrderForm, CreateUserForm, RegistrationForm, PasswordChangeForm, PasswordResetForm, LoginForm, UserForm
from django.utils import timezone
from django.urls import reverse_lazy

from . import views





def welcome(request):
    return render(request,'myswapapp/welcome.html')


class HomeView(ListView):
    model = Product
    template_name = 'myswapapp/home.html'



def login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'myswapapp/login.html', context)



def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='user')
			user.groups.add(group)
			
			User.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('myswapapp/login.html')
		
	context = {'form':form}
	return render(request, 'myswapapp/register.html', context)    
   



def products(request):
        products: Product.objects.all()
        return render(request, "myswapapp/home.html", {'products': products})



class ProductDetailView(View):
    def get(self, request, slug):
        product =Product.objects.get(slug=slug)
        return render(request, 'myswapapp/product_detail.html',{'product': product})





    
def swapper_profile(request, pk):
    
    user =User.objects.get(id=pk)
    
    context ={'user':user }
    return render(request, 'myswapapp/swapper_profile.html', context)



def swapperPage(request):
    
	orders = request.user.user.order_set.all()

	total_orders = orders.count()
	
	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders}
	return render(request, 'myswapapp/swapper.html', context)




def profileSettings(request):
	user = request.user
	form = UserForm(instance=user)

	if request.method == 'POST':
		form = UserForm(request.POST, request.FILES,instance=user)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'myswapapp/profile_settings.html', context)





def add_product_in_basket(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product =Product.objects.get(id=product_id)
    Basket(user=user, product=product).save()
    return redirect('myswapapp/add_product_in_basket.html')



def show_basket(request):
    if request.user.is_authenticated:
        user = request.user
        basket = Basket.objects.filter(user=user)
        amount = 0.0
        total_amount = 0.0
        basket_product = [p for p in Basket.objects.all() if p.user == user]
        #print(basket_product)
        if products in basket_product:
            total =(products.quantity * products.product.price)
            totalamount = total.order
        return render(request, 'myswapapp/add_product_in_basket.html', {'basket':basket, 'totalamount':totalamount})
        



def basket(request):
    if request.user.is_authenticated:
        user = request.user.user
        order, created = Order.objects.get_or_create(
            user= request.user, 
            ordered=False, 
            product=product)
        products = order.orderproduct_set.all()
    else:
        products =[]
        order = {'get_basket_total':0, 'get_basket_products':0}

    context = {'products':products, 'order': order}
    return render(request, 'myswapapp/basket.html', context)








def createOrder(request, pk):
    user = User.objects.get(id=pk)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {'form': form}
    return render(request, 'myswapapp/order_form.html', context)



def updateOrder(request, pk):
    order =Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form": form}
    return render(request, 'myswapapp/order_form.html', context) 



def deleteOrder(request, pk):
    order =Order.objects.get(id-pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'product': order}
    return render(request, 'myswapapp/delete_order.html', context)


#class OrderSummaryView(View):
 #   def get(self, *args, **kwargs):

  #      try:
   #         order = Order.objects.get(user=self.request.user, ordered=False)
    #        context = {
     #           'order': order
      #      }
       #     return render(self.request, 'myswapapp/order_summary.html', context)
       # except ObjectDoesNotExist:
        #    messages.success(self.request, "You dont have an active order")
         #   return redirect('myswapapp/home.html')



class CheckoutView(View):
   def get(self, *args, **kwargs):
        form = PaymentForm()
        context = {
            'form': form
        }
        return render(self.request, "myswapapp/order_summary.html", context)
        
        def post(self, *args, **kwargs):
            form = PaymentForm(self.request.POST or None)
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                if form.is_valid():
                    street_address = form.cleaned_data.get('street_address')
                    state = form.cleaned_data.get('state')
                    zipcode = form.cleaned_data.get('zipcode')
                    
                    payment_option = form.cleaned_data.get('payment_option')
                    billing_address = Address(
                        user=self.request.user,
                        street_address = street_address,
                        state = state,
                        zipcode = zipcode,
                        address_type = 'B')

                    
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()
                                    
                    return redirect('myswapapp/order_summary.html')
                messages.warning(self.request, "Failed Checkout")
                return redirect('myswapapp/order_summary.html')
            except ObjectDoesNotExist:
                messages.error(self.request, "You do not have an active order")
                return redirect("myswapapp/home.html")

def updateProduct(request):
    return JsonResponse("This product was added to your Swapp order", safe=False)               

            

class PaymentView(View):
    def get(self, *args, **kwargs):
        form = PaymentForm()
        context = {
            'form' : form
        }

        return render(self.request, 'myswapapp/payment.html', context)

    def post(self, *args, **kwargs):
        form = PaymentForm(self.request.POST or None)
        if form.is_valid():
            print('The form is valid')
            return redirect('myswapapp/home.html')




def logout(request):
    logout(request)
    return redirect('myswapapp/login.html')



def orderConfirmation(request):
    return render(request,'myswapapp/order_confirmation.html')

