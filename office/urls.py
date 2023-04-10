from django.urls import include, path
from office.views import office, manager

urlpatterns = [
    path('', office.home, name='home'),
    path('products/', office.ListProductView.as_view(), name='products'),
    
    path('manager/', include(([
        path('', manager.HomeView.as_view(), name='home'),
        path('product_add/', manager.AddProductView.as_view(), name='product-add'),
        path('product_delete/<int:pk>/', manager.DeleteProductView.as_view(), name='product-delete'),
        path('delivery_person_add/', manager.AddDeliveryPerson.as_view(), name='delivery-person-add'),
        path('delivery_persons/', manager.ListDeliveryPersonView.as_view(), name='delivery-persons'),
        path('delivery_person_delete/<int:pk>/', manager.DeleteDeliveryPersonView.as_view(), name='delivery-person-delete'),
        path('profile/', manager.AddProductView.as_view(), name='profile'),
        path('logout', manager.AddProductView.as_view(), name='logout'),
    ], 'office'), namespace='manager')),

]