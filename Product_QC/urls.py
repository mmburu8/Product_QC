# myproject/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product_kpi/', include('product_kpi.urls')),
]
