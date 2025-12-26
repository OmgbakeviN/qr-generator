from django.urls import path
from .views import home, result, robots_txt

app_name = "qr"

urlpatterns = [
    path("",home,name="home"),
    path("result/<uuid:pk>",result,name="result"),
    path("robots.txt", robots_txt, name="robots_txt"),
]