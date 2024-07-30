from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt
from . utils import cookieCart, cartData

# Create your views here.

def store(request):

	Data = cookieCart(request)
	cartItems = Data['cartItems']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = len(items)

	else:
		Data = cookieCart(request)
		cartItems = Data['cartItems']
		order = Data['order']
		items = Data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = len(items)

	else:
		Data = cookieCart(request)
		cartItems = Data['cartItems']
		order = Data['order']
		items = Data['items']


	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

@csrf_exempt
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	userId = data['userId']

	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	print(customer)
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('item was added', safe=False)