# myapp/forms.py
from django import forms
from .models import MyModel

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['date', 'total_products', 'defect_products', 
                  'passed_products', 'products_returned', 'customer_compliants']
