from django.urls import path

from .consumers import attackNotify

ws_urlpatterns = [
        path('ws/notify/', attackNotify.as_asgi())
]
