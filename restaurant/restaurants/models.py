from django.db import models


class Restaurant(models.Model):
    """Represents a restaurant."""

    name = models.CharField(max_length=100, primary_key=True)
