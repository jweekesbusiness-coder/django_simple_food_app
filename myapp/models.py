from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .managers import ItemManager
from django.utils import timezone



#Django best practices - keep models small and focused, 
# Create your models here.
class Item(models.Model):
    #Composite Index 
    class Meta:
        indexes = [
            models.Index(fields=['user','item_price'])
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,default =1)
    item_name = models.CharField(max_length=200,db_index=True) #Indexing a field
    item_des = models.CharField()
    item_price = models.DecimalField(max_digits=6,decimal_places=2,db_index=True) #Indexing a field
    item_image = models.ImageField(upload_to="item_images/",blank=True,null=True,unique=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False) #Used for creating a soft delete flag
    deleted_at = models.DateTimeField(null=True,blank=True) #Used to store the time of deletion for soft deleted items
    #Connecting our custom manager to our Item model
    objects = ItemManager()
    all_objects = models.Manager()

    #This will be the redirect link of the CreateView or UpdateView class that uses this model
    def get_absolute_url(self):
        return reverse("myapp:detail", kwargs={"pk": self.pk})
    
 
    def __str__(self):
        return self.item_name + ":" + str(self.item_price)

    #Overiding the delete method to create a soft delete
    def delete(self, using=None, keep_parents =False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.category_name
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item,related_name='orders')
    total_price = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    # def save(self,*args, **kwargs):
    #     self.total_price = 0
    #     for item in self.items.all():
    #         self.total_price += item.item_price
    #     self.save()

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"   