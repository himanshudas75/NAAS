from django.urls import include, path
from office.views import office, manager

urlpatterns = [
    path('', office.home, name='home'),
    
    path('manager/', include(([
        path('', manager.HomeView.as_view()),
        path('add_product/', manager.AddProductView.as_view()),
    ], 'office'), namespace='manager')),

]