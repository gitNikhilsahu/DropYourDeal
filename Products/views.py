from django.shortcuts import render

def products_home_view(request):
	return render(request,'products/products-home.html')
