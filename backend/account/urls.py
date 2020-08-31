from django.urls import path

from account.views import CreateAccountView, CreateTokenView


app_name = 'account'

urlpatterns = [
    path('create/', CreateAccountView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token')
]
