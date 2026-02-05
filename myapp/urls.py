from django.urls import path
from .views import index,detail,create_item,update_item,delete_item

#namespacing
app_name='myapp'
urlpatterns = [
    path('',view=index,name='index'),
    path('item/<str:id>',view=detail,name='detail'),
     path('add/',view=create_item,name='item_form'),
     path('update/<str:id>',view=update_item, name='update-item'),
     path('delete/<int:id>',view = delete_item, name='delete_item')
]
