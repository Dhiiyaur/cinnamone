from django.db import models
from django.conf import settings
from django.shortcuts import reverse
# Create your models here.

class CategoryItem(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Item(models.Model):

    title = models.CharField(max_length= 100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null= True)
    category = models.ForeignKey(CategoryItem, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='static/img/product', blank = True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField()
    

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('product', kwargs={
    #         'slug' : self.slug
    #     })

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={
        'slug' : self.slug
    })

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={
        'slug' : self.slug
    }) 


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete = models.CASCADE,blank=True, null= True)
    ordered = models.BooleanField(default= False)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    # tracking order
    quantity  = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_price(self):
        return self.quantity * self.item.price

    def get_total_discont_price(self):
        return self.quantity * self.item.discount_price


    def final_price(self):

        if self.item.discount_price:
            return self.get_total_discont_price()
        else:
            return self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete = models.CASCADE)

    item = models.ManyToManyField(OrderItem)
    start_date = models.DateField(auto_now_add= True)
    ordered_date = models.DateField()
    ordered = models.BooleanField(default= False)

    def __str__(self):
        return self.user.username

    def total_price(self):

        total = 0
        for item in self.item.all():
            total += item.final_price()

        return total