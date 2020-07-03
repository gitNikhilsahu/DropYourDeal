from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('',views.home_view),
    path('service/', include('Services.urls')),
    path('product/', include('Products.urls')),
    path('pricing/',views.pricing_view),
    path('contact/',views.contact_view),
    path('about',views.about_view),

    path('account/',include('Account.urls')),
    path('admin/',admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
