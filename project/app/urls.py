from django.urls import path
from . import views
urlpatterns = [
path('',views.login),
path('logout',views.logout),
path('clientreg',views.clientreg),
path('clienthome',views.clienthome),
path('advocatehome',views.advocatehome),

    
]