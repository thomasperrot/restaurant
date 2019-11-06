from rest_framework import serializers

from . import models


class RestaurantSerializer(serializers.ModelSerializer):
    """A serializer for Restaurant objects."""

    class Meta:
        model = models.Restaurant
        fields = ("name",)

    def validate_name(self, value: str) -> str:
        if value == "random":
            raise serializers.ValidationError("restaurant name can not be 'random'.")
        return value
