from django.urls import path
from .views import *

urlpatterns = [
    path('', category_list, name='category_list_view'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_detail_view'),
    path('topic/<str:slug>/', messages_list, name='topic_detail_view'),
    path('user/<int:id>/', UserDetail.as_view(), name='user_detail_url'),
    path('users/', users_list, name='users_list_url'),

]
