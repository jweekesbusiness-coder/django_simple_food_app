from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    item_list = Item.objects.all()
    context = {'items':item_list}
    return render(request,"myapp/index.html",context)

def detail(request,id):
    item = Item.objects.get(id=int(id))
    context = {'item':item}
    return render(request,"myapp/detail.html",context)


def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
        print("Post request is triggered")
        
    
    context = {'form':form}
    return render(request,'myapp/item-form.html',context)


def update_item(request,id):
    item  = Item.objects.get(id=id)
    if item == None:
        return   redirect('myapp:index')
    
    itemForm = ItemForm(request.POST or None,instance=item)
    if request.method == 'POST':
        if itemForm.is_valid():
            itemForm.save()
            return   redirect('myapp:index')
    
    context = {'form': itemForm,
                'Type': 'Update'}
    return render(request,'myapp/item-form.html',context)


def delete_item(request,id):
    item = Item.objects.get(id=id)
    if request.method =="POST":
      item.delete()
      return redirect('myapp:index')
    return render(request,'myapp/item-delete.html',{})