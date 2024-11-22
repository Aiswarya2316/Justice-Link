from django.urls import path
from . import views
urlpatterns = [
path('',views.login),
path('logout',views.logout),
path('clientreg',views.clientreg),
path('advocatereg',views.advocatereg),
path('clienthome',views.clienthome),
path('advocatehome',views.advocatehome),
path('clientprofile',views.clientprofile),
path('updateclientprofile',views.updateclientprofile),
path('advocateprofile',views.advocateprofile),
path('updateadvocateprofile',views.updateadvocateprofile),
path('viewadvocates',views.viewadvocates),
path('viewclients',views.viewclients),
path('filecase/<int:id>', views.filecase, name='filecase'),
path('viewcases/', views.viewcases, name='viewcases'),






    
]