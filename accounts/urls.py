from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('',views.index,name='index'),
    path('detail/<int:id>',views.detail,name='detail'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('create/',views.create,name='create'),
    path('update/<int:id>',views.update,name='update'),
    path('login/',views.loginview,name='login'),
    path('register/',views.register,name='register'),
]
