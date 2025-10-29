from django import forms
from .models import Operation

class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['operation_type', 'uas', 'number_of_drones', 'rpic', 'latitude', 'longitude', 'radius', 'start_datetime', 'end_datetime', 'request_state']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OperationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'] = forms.CharField(initial=user.username, widget=forms.HiddenInput())