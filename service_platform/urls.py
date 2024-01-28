from django.urls import path
from . import views
from django.conf.urls.static import static
from .views import service, add_to_cart, view_cart



urlpatterns = [
    path('', views.index, name='index'), #index page
    # path('', views.home, name='home'), #index page
    path('about/',views.about,name = 'about'),
    path('contact/',views.contact,name = 'contact'),
    path('service/', views.service, name='service'),
    path('fixsolution/', views.fixsolution, name='fixsolution'),
    path('product/', views.product, name='product'),
    path('book/',views.book,name = 'book'),
    path('register/', views.register, name='register'), 
    path('login/', views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    # path("logout",views.logout_view,name = "logout")
    path('add_to_cart/<int:service_id>/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('detectit/',views.detectit,name = 'detectit'),
    path('ai/',views.ai,name = 'ai'),
]

