from django import forms


from .models import PropertyType, Location

class PropertySearchForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False)
    property_type = forms.ModelChoiceField(queryset=PropertyType.objects.all(), required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
