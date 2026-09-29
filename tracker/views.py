from django.shortcuts import render

def home(request):
    # Finds templates/tracker/home.html and returns it as a web page
    return render(request, 'tracker/home.html')