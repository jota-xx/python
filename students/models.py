from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Perfil(User):
    """user = models.OneToOneField(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)"""
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Fecha de Nac.',)
    direccion = models.TextField(blank=True)
