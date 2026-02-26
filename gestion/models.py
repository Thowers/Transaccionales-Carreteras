from django.db import models
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    LIMITES = {'LOCAL': 3, 'REGIONAL': 3, 'NACIONAL': 2, 'AUTOPISTA': 2}
    
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Carretera(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"

    def clean(self):
        if not self.pk:
            conteo = Carretera.objects.filter(categoria=self.categoria).count()
            limite = Categoria.LIMITES.get(self.categoria.nombre.upper(), 99)
            if conteo >= limite:
                raise ValidationError(f"Límite alcanzado: {self.categoria.nombre} solo permite {limite} rutas.")

class Poblacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Tramo(models.Model):
    carretera = models.ForeignKey(Carretera, on_delete=models.CASCADE, related_name='tramos')
    km_inicio = models.FloatField()
    km_fin = models.FloatField()
    pueblo_inicio = models.ForeignKey(Poblacion, on_delete=models.PROTECT, related_name='inicio_tramos')
    pueblo_fin = models.ForeignKey(Poblacion, on_delete=models.PROTECT, related_name='fin_tramos')
    
    TIPO_FINAL_CHOICES = [('F', 'Físico'), ('C', 'Confluencia'), ('N', 'Ninguno')]
    tipo_final = models.CharField(max_length=1, choices=TIPO_FINAL_CHOICES, default='N')
    confluye_con = models.ForeignKey(Carretera, on_delete=models.SET_NULL, null=True, blank=True, related_name='recibe_confluencia')

    def __str__(self):
        return f"Tramo {self.carretera.nombre}: {self.km_inicio}km - {self.km_fin}km"