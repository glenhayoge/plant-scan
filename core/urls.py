from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from identifier.views import PlantViewSet 

router = routers.DefaultRouter()
router.register(r'plants', PlantViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]