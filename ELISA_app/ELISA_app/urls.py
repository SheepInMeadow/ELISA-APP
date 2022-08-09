"""
DO NOT EDIT, INHERITS FROM CORE, ADMIN
"""

from django.contrib import admin
from django.urls import path, include
from ELISA_core import urls #ignore underline, pycharm fault

urlpatterns = [
    path('', include('ELISA_core.urls')),
    path('admin/', admin.site.urls),
]
