from django.urls import path
from .views import index,create_item,update_item,delete_item,FoodDetailView,ItemCreateView,ItemUpdateView,ItemDeleteView,detail
from django.views.decorators.cache import cache_page
#namespacing
app_name='myapp'
urlpatterns = [
    # path('', cache_page(60 * 15)(index),name='index'), Caches the index view for 15 minutes
    path('',view=index, name='index'),
    path('item/<int:pk>',view=detail,name='detail'),
     path('add/',view=create_item,name='item_form'),
     path('update/<int:pk>',view=ItemUpdateView.as_view(), name='update-item'),
     path('delete/<int:pk>',view = ItemDeleteView.as_view(), name='delete_item'),
]
