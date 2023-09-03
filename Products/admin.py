from django.contrib import admin
from . import models as ProductsModels

# Register your models here.

admin.site.register(ProductsModels.Product)
admin.site.register(ProductsModels.Images)
admin.site.register(ProductsModels.Review)
admin.site.register(ProductsModels.CartItem)
admin.site.register(ProductsModels.Category)
