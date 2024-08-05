from .models import PropertyType

def property_types(request):
    return {
        'property_types': PropertyType.objects.all()
    }
