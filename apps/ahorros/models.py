from django.db import models
from django.contrib.auth.models import User #Modelo de usuario que trae por defecto

class SafeBox(models.Model): #Aca al hacer que herede de models hacemos que Django al hacer las migracione lo covierta en una tabla de DB
    usuario = models.OneToOneField(User, on_delete= models.CASCADE) #Una columna es usuario que usamos el de django, y al ser OneToOne significa que la caja fuerte puede pertenecer a un solo usuario no a varios
    # Es como decir que una caja fuerte solo apunta a un usuario?
    billetera = models.DecimalField(max_digits=12,decimal_places=2,default=0) #otra columna va a ser la billetera

    def __str__(self):
        return f'Caja fuerte de: {self.usuario.username}' #Esto retorna un string con su contenido
    
class Alcancia(models.Model):
    name = models.CharField(max_length=150) # Aca poner el nombre de la alcancia y la moneda MEP PESOS etc, es resposabilidad del usuario
    fecha_creacion = models.DateField(auto_now_add=True) # se pone automaticamene la fecha 
    fecha_objetivo = models.DateField(null=True,blank=True)
    monto_actual = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    monto_objetivo = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    safe_box = models.ForeignKey(SafeBox,on_delete= models.CASCADE) # varias alcancias pueden apuntar a una caja fuerte pero si esa se borra se borran todas las alcancias
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return f'{self.name} --> ${self.monto_actual} /// ${self.monto_objetivo}'

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto','Gasto'),
        ('ahorrar', 'Ahorrar'),
    ]

    DESTINO_CHOICES = [
        ('billetera','Billetera'),
        ('alcancia','Alcancia'),
    ]

    fecha = models.DateField()
    descripcion = models.CharField(max_length= 200)
    tipo = models.CharField(max_length= 7, choices = TIPO_CHOICES) 
    destino = models.CharField(max_length=10, choices = DESTINO_CHOICES, blank= True, null= True) # Vacio en caso de gasto
    usuario = models.ForeignKey(User, on_delete= models.CASCADE)
    monto = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    alcancia = models.ForeignKey(Alcancia, on_delete=models.SET_NULL, null=True, blank=True) # Si se borra la alcancia queda nula pero los mov siguen existiendo 

    def __str__(self):
        tipo_texto = "Ingreso" if self.tipo == 'ingreso' else "Gasto"
        destino_texto = f" → {self.get_destino_display()}" if self.destino else ""
        return f"{self.fecha} - {tipo_texto}{destino_texto}: {self.descripcion} - ${self.monto}"