from django import forms
from .models import Procedure

class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = ['operation_type', 'drone_platform', 'number_of_drones']