from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from todo.views import register
from todo.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
]