from django import forms
from .models import Item
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name',"item_des",'item_price','item_image']
        #Used to add placeholders in our form
        widgets = {
            'item_name': forms.TextInput(attrs={"placeholder": "e.g. Margherita Pizza",
                                                "required": True}),
            'item_des': forms.TextInput(attrs={"placeholder": "e.g. Fresh and cheesy","required": True}),
            'item_price': forms.NumberInput(attrs={"placeholder": "e.g. 100","required": True}),
            'item_image': forms.URLInput(attrs={"placeholder": "e.g. link to image","required": False})
        }
        
        def form_valid(self,form):
            form.instance.user = self.request.user
            return super().form_valid(form)
        
    #Makes sure the price entered in the form is valid
    def clean_item_price(self):
        price = self.cleaned_data['item_price']
        if price <0:
            raise forms.ValidationError("Price cannot be negative")
        return price
    
    #form validation here
    def clean(self):
        cleaned = super().clean() # Gets all the dataa from our form
        name = cleaned.get("item_name")
        desc = cleaned.get("item_des")
        if name and desc and name.lower() in desc.lower():
            raise forms.ValidationError("Description cannot contain the item name")
        return cleaned