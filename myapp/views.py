from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import  DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import logging 
from django.shortcuts import get_object_or_404
from django.utils import timezone
logger = logging.getLogger(__name__) # Used to log
# Create your views here.
#Middlewares are used to process the request before it reaches the view and process 
# the response before it is sent to the client Browser -> Middleware Stack -> View -> MiddlewareStack -> Response.
#@login_required
#We will cache data for 15 minutes
# @cache_page(60 * 15) #Needed for cache and specifies how long data will be cached for
# Ensures the page is cached separately based on the User-Agent header.
# This is important because mobile and desktop devices may receive different
# versions of the page. Without this, Django could serve the same cached
# version to all users, causing layout or content issues across devices.
# @vary_on_headers("User-Agent") 
def index(request):
    logger.info("Fetching all items from the database") # Logs this messsage when we start fetching items
    logger.info(f"User [{timezone.now().isoformat()}]  {request.user} is requesting item list from {request.META.get('REMOTE_ADDR')}") # Logs the user that is accessing the index page and their IP address
    item_list = Item.objects.all()
    logger.debug(f"Found {item_list.count()} items") #Logs the number of items in our item list
    #Information from the log is put inside of the file that we specified in our settings under Needed for logging
    paginator = Paginator(item_list,5) #Each page can only have 5 items
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj}
    return render(request,"myapp/index.html",context)


def detail(request,pk):
    
    logger.info(f"Fetching item with id {pk} from the database") # Logs this message when we start fetching the item with the specified id
    try:  
        # item = Item.objects.get(id=int(pk))
        item = get_object_or_404(Item,id=pk) # This is a shortcut that does the same thing as the line above but it also handles the case where the item with the specified id does not exist and it will return a 404 error page instead of crashing our application
        logger.debug(f"Found item: {item.item_name}") # Logs the name of the found item
    except Exception as e:
        logger.error(f"Error fetching item with id {pk}: {e}") # Logs any error that occurs during the fetching of the item
        raise
    context = {'item':item}
    return render(request,"myapp/detail.html",context)



def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
        else:
            print(form.errors['item_price'])
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

# Not optimized
def get_objects(request):
    for item in Item.objects.all():
        print(item.item_name)

def get_objects_optimized(request):
    items = Item.objects.only('item_name') # Only gets the Item name this is good for optimization

    for item in items:
        print(item)

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
    
