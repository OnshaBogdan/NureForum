from django.urls import path
from .views import *

urlpatterns = [
    path('', category_list, name='category_list_view'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_detail_view'),
    path('topic/<str:slug>/', messages_list, name='topic_detail_view'),
    path('user/<int:id>/', UserDetail.as_view(), name='user_detail_url'),
    path('sign-up/', UserCreate.as_view(), name='user_sign_up_url'),
    path('users/', users_list, name='users_list_url'),
    path('sign-in/', sign_in, name='user_sign_in_url'),
    path('logout/', logout_view, name='logout_url'),

]
