from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from.import views

urlpatterns = [
     path('admin/', admin.site.urls),
    # path('', include('advocates.urls')),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('advocatelist', views.advocate_list, name='advocate_list'),
    path('book/<int:advocate_id>/', views.book_advocate, name='book_advocate'),
    path('', views.register, name='register'),
]
