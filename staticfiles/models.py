from django.db import models

# Create your models here.
class MyModel(models.Model):
    date = models.DateField()
    total_products = models.IntegerField()
    defect_products = models.IntegerField()
    passed_products = models.IntegerField()
    products_returned = models.IntegerField()
    customer_compliants = models.IntegerField()
    
    def __str__(self):
        return self.name