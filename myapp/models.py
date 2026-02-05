from django.db import models

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_des = models.CharField()
    item_price = models.IntegerField()
    item_image = models.CharField(max_length=500,default='https://www.ikea.com/us/en/images/products/upplaga-plate-white__0714553_pe730123_s5.jpg?f=s')

    def __str__(self):
        return self.item_name