from django.db import models

from estaciones.Alcaldias.models import Alcaldia
from estaciones.Tipos_Estacion.models import Tipo_Estacion

class Estacion(models.Model):
    nombre = models.TextField()
    linea = models.CharField(max_length=2)
    est = models.CharField(max_length=2)
    cve_est = models.CharField(max_length=6)
    cve_eod17 = models.CharField(max_length=5)
    tipo = models.ForeignKey(Tipo_Estacion, on_delete=models.CASCADE, null=True)
    alcaldia = models.ForeignKey(Alcaldia, on_delete=models.CASCADE)    
    anio = models.TextField()
    ubicacion = models.TextField()

