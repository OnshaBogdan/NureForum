from django.urls import path
from .views import *

urlpatterns = [
    path('', category_list, name='category_list_view'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_detail_view'),
    path('topic/<str:slug>/', TopicDetail.as_view(), name='topic_detail_view'),

]
