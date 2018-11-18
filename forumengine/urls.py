from django.urls import path
from .views import *

urlpatterns = [
    path('', category_list, name='category_list_view'),
    path('<str:slug>/', CategoryDetail.as_view(), name='category_detail_view'),

]