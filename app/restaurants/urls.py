from rest_framework import routers

from . import viewsets


router = routers.SimpleRouter(trailing_slash=False)
router.register(r"restaurants", viewsets.RestaurantViewSet)
urlpatterns = router.urls
