from django.urls import path
from . import views

urlpatterns=[
    path('myform/',views.myform_view,name='myform'),
    path('myform2/',views.myform_view2,name='myform2'), 
    path('get_users/',views.get_users_view,name='get_users'), 
    path('get_hashtags/',views.get_hashtags_view,name='get_hashtags'), 
    path('classify_messages/',views.classify_messages_view,name='classify_messages'), 
]