from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default =1)
    item_name = models.CharField(max_length=200)
    item_des = models.CharField()
    item_price = models.IntegerField()
    item_image = models.CharField(max_length=500,default='https://www.ikea.com/us/en/images/products/upplaga-plate-white__0714553_pe730123_s5.jpg?f=s')

    #This will be the redirect link of the CreateView or UpdateView class that uses this model
    def get_absolute_url(self):
        return reverse("myapp:detail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return self.item_name