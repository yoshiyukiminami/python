from django.db import models


class PinCollection(models.Model):
    """
    googlemaps pin のレコード
    """
    place_id = models.CharField(null=True, blank=True, max_length=200)
    name = models.CharField(max_length=200)
    latlng = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
