from django.urls import include, path
from office.views import office, manager

urlpatterns = [
    path('', office.home, name='home'),
    
    path('manager/', include(([
        path('', manager.HomeView.as_view(), name='home'),
        path('add_product/', manager.AddProductView.as_view(), name='add-product'),
        path('add_delivery_person/', manager.AddDeliveryPerson.as_view(), name='add-delivery-person'),
        path('profile/', manager.AddProductView.as_view(), name='profile'),
        path('logout', manager.AddProductView.as_view(), name='logout'),
    ], 'office'), namespace='manager')),

]