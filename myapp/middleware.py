import time
from django.http import HttpResponseForbidden
#Custom middleware

class LogRequestMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        #processes before
        print(f"[Middleware] Request Path: {request.path}")
        response= self.get_response(request) # Calls the next Middleware Stack that occurs after the view is processed

        #process after view
        print(f"[Middleware] Response Status: {response.status_code}")
        return response
    
#Middleware that returns how long a response takes
class TimerMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response= self.get_response(request) # Calls the next Middleware Stack that occurs after the view is processed
        duration = time.time() - start
        print(f"[Middleware] request took {duration:.2f} seconds")
        return response
    
#Middleware to block certain IP addresseses from making request
class BlockIPMiddleware:
    BLOCKED_IPS = ['']
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip  = request.META.get("REMOTE_ADDR") # Gets the IP address of the client
        if ip in self.BLOCKED_IPS:
            return HttpResponseForbidden("Your IP is blocked")
        return self.get_response(request)