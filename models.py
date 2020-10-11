from django.db import models
import math

# Create your models here.

STATUS_CHOICES = (
    ("Processing", "Processing"),
    ("Delivered", "Delivered"),
    ("Canceled", "Canceled"),
    )


class Users(models.Model):
    user_id = models.AutoField(primary_key=True, blank=True)
    username = models.CharField(max_length=10)
    email = models.EmailField(max_length=10)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    password = models.CharField(max_length=15)
    address = models.CharField(max_length=30)
    address2 = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    zipcode = models.IntegerField()
    phone = models.IntegerField()

    def __str__(self):
        return str(self.username)


class Category(models.Model):
    category_id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class SubCategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.category) + '---' + str(self.name)


class Discount(models.Model):
    code = models.AutoField(primary_key=True)
    discount = models.FloatField(default=500)

    def __str__(self):
       return str(self.discount)


class Items(models.Model):
    item_id = models.AutoField(primary_key=True, blank=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(upload_to='static/Image', blank=True)
    description = models.CharField(max_length=500, default='None')

    def __str__(self):
        return str(self.title)


class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    cart_id = models.AutoField(primary_key=True)
    itemname = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(default="M", max_length=10)
    price = models.FloatField()
    image = models.ImageField()
    discount = models.FloatField(default=0)

    @property
    def total_cost(self):
        dis = self.price - ((self.price * self.discount)/100)
        return self.quantity * math.ceil(dis)

    def __str__(self):
        return str(self.itemname)


class Blog(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    caption = models.TextField()
    image = models.ImageField(upload_to='static/Image', blank=True)
    date = models.DateField(auto_now_add=True)


class Contact(models.Model):
    user = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default='Processing', max_length=20)
    delivery = models.CharField(max_length=20)
    payment = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    discount = models.FloatField(default=0)



    def __str__(self):
        return str(self.user)

class Different_Address(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_id = models.IntegerField(default=0)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    zipcode = models.IntegerField()

    def __str__(self):
        return str(self.user)


class Paytm(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_id = models.IntegerField(default=0)
    number = models.IntegerField()


class Card(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_id = models.IntegerField(default=0)
    name = models.CharField(max_length=25)
    card_no = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()

