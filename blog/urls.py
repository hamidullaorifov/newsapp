from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('',views.index,name='index'),
    path('detail/<slug:post>',views.post_detail,name='post_detail'),
    path('list/<str:category>',views.post_list,name='post_list'),
    path('list',views.post_list,name='posts_list'),
    path('search/',views.search,name='search')
]
