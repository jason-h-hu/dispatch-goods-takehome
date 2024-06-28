from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/<uuid:id>', views.get_user, name='users'),
    path('qr/<uuid:id>.png', views.get_qr, name='qr'),
]
