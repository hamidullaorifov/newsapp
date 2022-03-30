from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [

    path('',views.index,name='index'),
    path('search/',views.search,name='search'),
    path('detail/<slug:post>',views.post_detail,name='post_detail'),
    path('list',views.post_list,name='posts_list'),
    path('<str:category>/',views.index,name='index'),
    
]
