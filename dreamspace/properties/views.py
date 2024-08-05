# properties/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, PropertyType, Cart, CartItem, Payment
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, PropertySearchForm
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def base_view(request):
    property_types = PropertyType.objects.all()
    return render(request, 'base.html', {'property_types': property_types})

def home(request):
    property_types = PropertyType.objects.all()
    return render(request, 'home.html', {'property_types': property_types})

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property_list.html', {'properties': properties})

def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'property_detail.html', {'property': property})

def property_list_by_type(request, property_type_id):
    property_type = get_object_or_404(PropertyType, id=property_type_id)
    properties = Property.objects.filter(property_type=property_type)
    return render(request, 'property_list.html', {'properties': properties, 'property_type': property_type})

def about(request):
    return render(request, 'about.html')

def search_results(request):
    form = PropertySearchForm(request.GET)
    properties = []
    if request.GET and form.is_valid():
        location = form.cleaned_data.get('location')
        property_type = form.cleaned_data.get('property_type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        properties = Property.objects.all()

        if location:
            properties = properties.filter(location=location)
        if property_type:
            properties = properties.filter(property_type=property_type)
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)

    return render(request, 'search_results.html', {'form': form, 'properties': properties})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send an email (you need to configure email settings in settings.py)
            send_mail(
                f'Message from {name} via Contact Form',
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')

@login_required
def add_to_cart(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    CartItem.objects.get_or_create(cart=cart, property=property)
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.cart.user == request.user:
        item.delete()
    return redirect('cart_detail')

@login_required
def create_order(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    order_amount = int((property.price/10000) * 100)  # Convert price to paise
    order_currency = 'INR'
    order_receipt = f'order_rcptid_{property_id}'
    notes = {'Property ID': property_id}

    try:
        payment = client.order.create({
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt,
            'notes': notes
        })

        payment_record = Payment.objects.create(
            user=request.user,
            property=property,
            order_id=payment['id'],
            amount=order_amount,
            status='created'
        )

        context = {
            'order_id': payment['id'],
            'order_amount': order_amount,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'property_id': property_id,
        }

        return render(request, 'payment.html', context)

    except Exception as e:
        # Handle the error gracefully
        return HttpResponseBadRequest(f'Payment creation failed: {str(e)}')


@login_required
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            payment = Payment.objects.get(order_id=data['razorpay_order_id'])
            payment.payment_id = data['razorpay_payment_id']
            payment.signature = data['razorpay_signature']
            payment.status = 'successful'
            payment.save()

            # Additional logic for successful payment, e.g., blocking the property
            property = payment.property
            property.is_blocked = True
            property.save()

            return redirect('payment_success_page')
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest('Signature verification failed')
    return HttpResponseBadRequest('Invalid request')

def payment_success_page(request):
    return render(request, 'payment_success.html')
