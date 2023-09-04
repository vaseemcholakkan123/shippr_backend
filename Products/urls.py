from django.urls import path
from . import views as ProductViews


urlpatterns = [
    path('action/<int:pk>',ProductViews.ProductActionVendor.as_view() ,name='product-action'),
    path('action/',ProductViews.ProductActionVendor.as_view() ,name='product-action'),
    path('get-categories/', ProductViews.GetCategories.as_view(), name="retrieve-categories"),
    path('get-vendor-products/',ProductViews.RetrieveVendorProducts.as_view(), name="get-vendor-products" ),
    path('get-user-products/', ProductViews.GetProductForUser.as_view(), name='get-product-for-user'),
    path('get-user-cart/', ProductViews.GetUserCart.as_view(), name='get-user-cart'),
    path('add-remove-cart/<prod_id>/', ProductViews.AddOrRemoveCart.as_view(), name="add-remove-cart"),
    path('get-product/<int:pk>/', ProductViews.ProductDetailView.as_view(), name="product-detail"),
    path('add-category/', ProductViews.AddCategory.as_view(), name="add-category")
]