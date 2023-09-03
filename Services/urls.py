from django.urls import path
from . import views as ServiceViews


urlpatterns = [
    path('purchase/', ServiceViews.PurchaseProducts.as_view(), name="purchae-products"),
    path('get-user-orders/', ServiceViews.GetUserOrders.as_view(), name="get-user-orders"),

]