from django.urls import path

from account.views import CreateAccountView


app_name = 'account'

urlpatterns = [
    path('create/', CreateAccountView.as_view(), name='create'),
]
