from django.urls import path
from .views import register, activate_account, create_advertisement, advertisement_list, create_response

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<str:confirmation_code>/', activate_account, name='activate_account'),
    path('create_advertisement/', create_advertisement, name='create_advertisement'),
    path('advertisement_list/', advertisement_list, name='advertisement_list'),
    path('create_response/<int:advertisement_id>/', create_response, name='create_response'),
]
