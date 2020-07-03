from django.shortcuts import render

def services_home_view(request):
	return render(request,'services/services-home.html')
