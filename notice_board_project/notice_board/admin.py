from django.contrib import admin
from .models import CustomUser, Category, Advertisement, Response

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Response)
