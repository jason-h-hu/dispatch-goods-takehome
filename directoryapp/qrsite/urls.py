from django.urls import path
from .views import form_view, UserView, get_qr

urlpatterns = [
    path('', form_view, name='index'),
    path('users/<uuid:pk>', UserView.as_view(), name='user'),
    path('qr/<uuid:id>.png', get_qr, name='qr'),
]
