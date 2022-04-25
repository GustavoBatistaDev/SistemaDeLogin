from django.urls import path
from . import views


urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('pageinitial/', views.page_initial, name='page_initial'),
    path('logout/', views.logout, name="logout")
]