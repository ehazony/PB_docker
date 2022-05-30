from django.urls import path

from . import views
from .views import Profile

urlpatterns = [
    path('profile/', Profile.as_view()),

]