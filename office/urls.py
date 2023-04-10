from django.urls import include, path
from office.views import office

urlpatterns = [
    path('', office.home, name='home')
]