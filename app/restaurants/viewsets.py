from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from . import models, serializers


class RestaurantViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """A viewset for viewing, creating and deleting restaurants.
    """

    serializer_class = serializers.RestaurantSerializer
    queryset = models.Restaurant.objects.all()

    @action(detail=False, methods=["GET"], url_path="random")
    def get_random(self, request: Request, pk: str = None) -> Response:
        restaurant = models.Restaurant.objects.order_by('?').first()
        if not restaurant:
            raise NotFound(detail="No restaurant inserted yet.", code=404)
        serializer = self.serializer_class(restaurant)
        return Response(serializer.data)
