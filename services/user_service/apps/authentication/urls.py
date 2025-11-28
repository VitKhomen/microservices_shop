from django.urls import path

from .views import login_view, refresh_token


urlpatterns = [
    path('login/', login_view, name='login'),
    path('refresh/', refresh_token, name='refresh'),
]
