
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from django.shortcuts import reverse
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse_lazy






class User(models.Model):

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)#CASCADE=when ever a user is deleted it will delete the reationship with the other
    name = models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    #profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)

    
    

    def __str__(self):
        return self.user.username

class Chat(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=200)
    slug= models.SlugField(null=True)
    
class Messages(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text =models.CharField(max_length=500)
    date_sent = models.DateTimeField(auto_now_add=True, null=True)



ADDRESS_CHOICES =(
    ('B', 'Billing'),
    ('S', 'Shipping')
)




class Product(models.Model):
    CATEGORY = (
            ('Indoor Decorations', 'Indoor Decorations'),
            ('Outdoor Decorations', 'Outdoor Decoration'),
    )

    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    slug= models.SlugField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places= 2)
    image = models.ImageField(default='default.jpg', upload_to='static/images')
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name_plural = "Products"



    def get_absolute_url(self):
        return reverse('myswapapp:product_detail', kwargs={ 'slug': self.slug})

    def get_basket_url(self):
        return reverse('myswappapp:basket', kwargs={'slug': self.slug})
    
    def get_add_product_in_basket_url(self):
        return reverse('myswapapp:add_product_in_basket', kwargs={'slug': self.slug})

    def get_remove_product_from_basket_url(self):
        return reverse('myswapapp:remove_product_from_basket', kwargs={'slug': self.slug})

    def get_remove_single_product_from_basket_url(self):
        return reverse('myswapapp:remove_single_product_from_basket',kwargs={'slug': self.slug})


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    
    def get_total_product_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    

    def __str__(self):
        return self.user.username
 
    def get_total_product_price(self):
        return self.product.price

    
        



class Profile(models.Model):
    user = models.CharField(max_length=200, null=True)
    Uid=models.AutoField(primary_key=True)
    location = models.CharField(max_length=100, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pic')
    slug= models.SlugField(null=True)

   
    def __str__(self):
        return f'{self.user} Profile'

    def get_absolute_url(self):
        return reverse('myswapapp: profile_swapper.html', kwargs={ 'slug': self.slug})
    
    def save(self):
        super().save()

        img= Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    street_address = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=50)
    address_type = models.CharField(max_length=1, choices= ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username 


class Basket(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)



