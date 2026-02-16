from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import  DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

# Create your views here.

@login_required
def index(request):
    item_list = Item.objects.all()
    context = {'items':item_list}
    return render(request,"myapp/index.html",context)


# def detail(request,id):
#     item = Item.objects.get(id=int(id))
#     context = {'item':item}
#     return render(request,"myapp/detail.html",context)



def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
        print("Post request is triggered")
        
    
    context = {'form':form}
    return render(request,'myapp/item-form.html',context) 



def update_item(request,pk):
    item  = Item.objects.get(id=pk)
    if item == None:
        return   redirect('myapp:index')

    if item.user != request.user:
        return HttpResponse("You are not the owner of this item. You cannot edit it.")
    
    itemForm = ItemForm(request.POST or None,instance=item)
    if request.method == 'POST':
        if itemForm.is_valid():
            itemForm.save()
            return   redirect('myapp:index')
    
    context = {'form': itemForm,
                'Type': 'Update'}
    return render(request,'myapp/item-form.html',context)


def delete_item(request,pk):
    item = Item.objects.get(id=pk)
    if request.method =="POST":
      item.delete()
      return redirect('myapp:index')
    return render(request,'myapp/item-delete.html',{})

#   CLASS BASED VIEWS

#Class Based  DeleteView
class ItemDeleteView(DeleteView):
    #this view looks for this template - modelname_confirm_delete.html
    model = Item
    success_url = reverse_lazy("myapp:index")

#cLASS Based Update View
class ItemUpdateView(UpdateView):
    model = Item
    fields = ['item_name',"item_des",'item_price','item_image']
    template_name_suffix =  "_update_form" #Now this view will look for a form that is modelname_update_form.html

     #Will allow only the owner of the item to update it
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

#Class Base Create View
class ItemCreateView(CreateView):
    #Looks for a modelname_form.html in your templates automatically
    model = Item
    fields = ['item_name',"item_des",'item_price','item_image']

#Class Based DetailView
class FoodDetailView(DetailView):
    model = Item
    template_name = 'myapp/detail.html'
    context_object_name = 'item'


#Class Based Index View
class IndexClassView(ListView):
    model = Item
    template_name = 'myapp/index.html'
    context_object_name = 'items'
    
