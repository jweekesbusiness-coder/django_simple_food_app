from django.urls import path,include
from .views import (item_list_api,item_detail_api,index,create_item,update_item,
                    delete_item,FoodDetailView,ItemCreateView,ItemUpdateView,ItemDeleteView,detail
                    ,ItemListAPIView,ItemDetailAPIView,ItemListCreateAPI,ItemRetrieveUpdateDestroyAPIView,
                    ItemViewSet,OrderViewSet)
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter #USed for rest framework viewsets
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#namespacing

router = DefaultRouter()
router.register("items",ItemViewSet,basename="item")
router.register("orders",OrderViewSet,basename="order")
app_name='myapp'
urlpatterns = [
    #URL Patterns of API
  #  path('items-json/',view=item_list_json, name="item_list_json"),
    # path('api/items/',view=item_list_api,name='item-list-api'), #Function based API view
    # path('api/items/<int:pk>',view=item_detail_api,name='item-detail-api'), # Function base Api view
    # path("api/items/", view=ItemListCreateAPI.as_view(),name="item-list-api"), #Class base views
    # path("api/items/<int:pk>", view=ItemRetrieveUpdateDestroyAPIView.as_view(),name="item-detail-api"), # Class base views
    path("api/",include(router.urls)),
    #JWT Token authentication urls
    path("api/token/",TokenObtainPairView.as_view(),name="token_obtain_pair"), #To get this token you must provide the username and password . You will get an access token and a refresh token. The access token is used to authenticate API requests, while the refresh token can be used to obtain a new access token when the old one expires.
    path('api/token/refresh/',TokenRefreshView.as_view,name='token_refresh'),
    #URL pathons for Django app
    # path('', cache_page(60 * 15)(index),name='index'), Caches the index view for 15 minutes
    path('',view=index, name='index'),
    path('item/<int:pk>',view=detail,name='detail'),
     path('add/',view=create_item,name='item_form'),
     path('update/<int:pk>',view=ItemUpdateView.as_view(), name='update-item'),
     path('delete/<int:pk>',view = ItemDeleteView.as_view(), name='delete_item'),
]
