from .views import *
from django.urls import path

app_label = 'Scrapper'

urlpatterns = [
    # S
    path('products/<str:brand_name>/', ProductListView.as_view(), name='product-list-by-brand'),
]
