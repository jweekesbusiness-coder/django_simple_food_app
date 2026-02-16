from django.urls import path
from .views import index,create_item,update_item,delete_item,IndexClassView,FoodDetailView,ItemCreateView,ItemUpdateView,ItemDeleteView

#namespacing
app_name='myapp'
urlpatterns = [
    path('',view=IndexClassView.as_view(),name='index'),
    path('item/<int:pk>',view=FoodDetailView.as_view(),name='detail'),
     path('add/',view=ItemCreateView.as_view(),name='item_form'),
     path('update/<int:pk>',view=ItemUpdateView.as_view(), name='update-item'),
     path('delete/<int:pk>',view = ItemDeleteView.as_view(), name='delete_item'),
]
