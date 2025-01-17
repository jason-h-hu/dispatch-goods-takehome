from django.urls import path
from .views import form_view, api_form_view, UserView, UserAPIView, get_qr

urlpatterns = [
    # Used by the views served by Django. See discussion in README
    path('', form_view, name='index'),
    path('users/<uuid:pk>', UserView.as_view(), name='user'),
    
    # Used by the Angular app
    path('api', api_form_view, name='api/index'),
    path('api/<uuid:pk>', UserAPIView.as_view(), name='api/user'),
    
    # Used by both
    path('qr/<uuid:id>.png', get_qr, name='qr'),
]
