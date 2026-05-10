from rest_framework import serializers
from .models import Item,Order
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class ItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ["id","user","item_name","item_des","item_price","item_image"]
        
    #Field level validation
    def validate_item_price(self,value):
        if value < 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value
    
    #Object level validation
    def validate(self,data):
        if data['item_name'].lower == data['item_des'].lower():
            raise serializers.ValidationError("Item name and description cannot be the same")
        return data
    

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True,read_only=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ['id','user','created_at','items']