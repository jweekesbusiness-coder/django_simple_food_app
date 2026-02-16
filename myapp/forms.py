from django import forms
from .models import Item
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name',"item_des",'item_price','item_image']
        def form_valid(self,form):
            form.instance.user = self.request.user
            return super().form_valid(form)