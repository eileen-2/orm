from django.contrib import admin
from django.urls import path
from main.views import index, a, b, c, whale, whaleride

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('a/', a),
    path('b/', b),
    path('c/', c),
    path('whale/', whale),
    path('whaleride/', whaleride),
]
