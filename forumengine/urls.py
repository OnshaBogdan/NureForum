from django.urls import path
from .views import *

urlpatterns = [
    path('', category_list, name='category_list_view'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_detail_view'),
    path('topic/create/', create_topic, name='create_topic_url'),
    path('topic/<str:slug>/', TopicDetail.as_view(), name='topic_detail_view'),
    path('user/<int:id>/', UserDetail.as_view(), name='user_detail_url'),
    path('sign-up/', UserCreate.as_view(), name='user_sign_up_url'),
    path('users/', users_list, name='users_list_url'),
    path('sign-in/', sign_in, name='user_sign_in_url'),
    path('logout/', logout_view, name='logout_url'),
    path('msg/create/', create_message, name='create_message_url'),
    path('msg/update/<int:message_id>/', MessageUpdate.as_view(), name='message_update_url'),
    path('msg/vote/', VoteMessage.as_view(), name='vote_message_url'),
    path('msg/best/', BestMessages.as_view(), name='best_messages_url'),

]
