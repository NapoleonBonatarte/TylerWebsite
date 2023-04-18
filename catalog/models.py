from django.db import models
    
class Element(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=2)
    atomic_number = models.IntegerField()
    atomic_weight = models.DecimalField(max_digits=12,decimal_places=8,default=0.00)

    def __str__(self):
        return self.name
    
    def get_symbol(self):
        return self.symbol
    
    def get_atomic_number(self):
        return self.atomic_number
    
    def get_atomic_weight(self):
        return self.atomic_weight