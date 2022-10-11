from django.urls import path, include

from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'offer', MortgageViewSet)

urlpatterns = [
    path('api/', include(router.urls)), # http://0.0.0.0:8000/api/offer/
]
# http://localhost:8000/api/offer/?price=10000000&deposit=10&term=20