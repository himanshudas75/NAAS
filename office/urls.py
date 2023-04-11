from django.urls import include, path
from office import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ListProductView.as_view(), name='products'),
    path('delivery_list/', views.DeliveryListView.as_view(), name='delivery-list'),
    path('delivery_complete/<int:id>/', views.complete_delivery, name='delivery-complete'),
    path('payment_gateway/<int:id>', views.PaymentGatewayView.as_view(), name='payment-gateway'),
    path('payment/<int:id>/', views.payment, name='payment'),
    path('customer_requests/', views.ListCustomerRequestsView.as_view(), name='customer-requests'),
    path('customer_request_add/', views.AddCustomerRequestView.as_view(), name='customer-request-add'),

    path('manager/', include(([
        path('', views.home, name='home'),
        
        path('product_add/', views.AddProductView.as_view(), name='product-add'),
        path('products/', views.ListProductView.as_view(), name='products'),
        path('product_delete/<int:pk>/', views.DeleteProductView.as_view(), name='product-delete'),

        path('delivery_person_add/', views.AddDeliveryPersonView.as_view(), name='delivery-person-add'),
        path('delivery_persons/', views.ListDeliveryPersonView.as_view(), name='delivery-persons'),
        path('delivery_person_delete/<int:pk>/', views.DeleteDeliveryPersonView.as_view(), name='delivery-person-delete'),

        path('customer_add/', views.AddCustomerView.as_view(), name='customer-add'),
        path('customers/', views.ListCustomerView.as_view(), name='customers'),
        path('customer_delete/<int:pk>/', views.DeleteCustomerView.as_view(), name='customer-delete'),
        
        path('subscriptions/<int:pk>/', views.ListSubscriptionView.as_view(), name='subscriptions'),
        path('subscriptions/<int:id1>/delete/<int:pk>/', views.DeleteSubscriptionView.as_view(), name='subscription-delete'),
        
        path('delivery_list/', views.DeliveryListView.as_view(), name='delivery-list'),
        path('generate_delivery_list/', views.generate_delivery_list, name='generate-delivery-list'),
        path('delete_delivery_list/', views.delete_delivery_list, name='delete-delivery-list'),

        path('calculate_salary/', views.calculate_salary, name='calculate-salary'),
        path('generate_bill/<int:id>/', views.generate_bill, name='generate-bill'),
        path('pause/<int:id>/<int:pause>/', views.pause, name='pause'),

        path('customer_requests/', views.ListCustomerRequestsView.as_view(), name='customer-requests'),
        path('customer_request_complete/<int:id>/', views.complete_customer_request, name='customer-request-complete'),

    ], 'office'), namespace='manager')),

]