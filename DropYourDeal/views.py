from django.shortcuts import render

def home_view(request):
	return render(request,'dropyourdeal/home.html')

def pricing_view(request):
	return render(request,'dropyourdeal/pricing.html')

def contact_view(request):
	return render(request,'dropyourdeal/contact.html')

def about_view(request):
	return render(request,'dropyourdeal/about.html')