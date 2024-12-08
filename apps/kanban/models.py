from django.db import models
from django.conf import settings

class Board(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='boards')

    def __str__(self):
        return self.name

class Column(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, related_name='columns', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    column = models.ForeignKey(Column, related_name='cards', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title