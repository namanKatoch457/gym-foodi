from django.shortcuts import render,HttpResponseRedirect,redirect,get_object_or_404
from .models import food,discount,CartItem,UserProfile,Order
from django.urls import reverse
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
import json

def home(request):
    dis_food = discount.objects.all()
    return render(request, 'index.html', {'dis_food':dis_food})

from django.shortcuts import render, HttpResponse
from .models import food, discount

def meal_category(request, meal_type):
    if meal_type == "veg":
        foods = food.objects.filter(food_type="VEG")
        template = 'veg_meal.html'
    elif meal_type == "nonveg":
        foods = food.objects.filter(food_type="NON-VEG")
        template = 'nonveg.html'
    else:
        return HttpResponse("Invalid meal type", status=404)

    return render(request, template, {'foods': foods})

#for cart
@login_required
def view_cart(request):
    cart_items = CartItem.objects.all()
    for item in cart_items:
        item.total_price = item.food.price * item.quantity  
    
    # Calculate the grand total for the entire cart
    total_price = sum(item.total_price for item in cart_items)

    # Pass both `cart_items` and `total_price` to the template
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Add to cart view
@login_required
def add_to_cart(request, food_id):
    food_item = get_object_or_404(food, id=food_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, food=food_item)
    # If the item is already in the cart, increase the quantity
    if not created:
        cart_item.quantity += 1
    cart_item.save()



#for shoing alerts and the back to same page where we used add to cat
    referer_url = request.META.get('HTTP_REFERER', '/')
    
    # Append the query parameter to show the alert
    if '?added_to_cart=' in referer_url:
        referer_url += '&added_to_cart=true'
    else:
        referer_url += '?added_to_cart=true'
    
    return HttpResponseRedirect(referer_url)
@login_required
def remove_from_cart(request, food_id):
    cart_item = CartItem.objects.get(id=food_id)
    cart_item.delete()
    return redirect('view_cart')



#registration page

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            user_profile = UserProfile(user=user, phone_number=form.cleaned_data['phone_number'])
            user_profile.save()

            login(request,user)
            return redirect('home')
    else:
        form  = UserRegistrationForm()

    return render(request, 'register.html',{'form':form})

#login

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('foodi')  # Redirect to the foodi page after successful login
            else:
                # Handle invalid login
                form.add_error(None, "Invalid credentials. Please try again.")
        else:
            form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def checkout(request):
    user = request.user

    # Attempt to get or create the UserProfile
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Retrieve the cart items for the user
    cart_items = CartItem.objects.filter(user=user)

    # Calculate total price for the order
    total_price = sum(item.food.price * item.quantity for item in cart_items)

    # Pass user details and cart items to the template
    context = {
        'user': user,
        'user_profile': user_profile,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)

#place order

@login_required
def place_order(request):
    user = request.user
    cart_items = list(CartItem.objects.filter(user=user))  # Convert to list

    if not cart_items:
        return redirect('empty_cart')  # Redirect if the cart is empty

    # Calculate the total price
    total_price = sum(item.food.price * item.quantity for item in cart_items)

    # Create the order
    order = Order.objects.create(
        user=user,
        phone_number=user.userprofile.phone_number,
        total_price=total_price,
        status='pending'
    )

    # Log the order items before adding to the order
    print(f"Order ID: {order.id}, Items: {cart_items}")

    # Add items to the order using .set() method
    order.items.set(cart_items)

    # Log after adding items
    print(f"Order ID: {order.id}, Items after adding: {order.items.all()}")

    # Clear the cart after placing the order
    CartItem.objects.filter(user=user).delete()

    # Redirect to the order confirmation page
    return redirect('order_confirmation', order_id=order.id)
    


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Get the order items
    items_list = order.items.all()  # This retrieves all items associated with the order
    
    return render(request, 'order_confirmation.html', {'order': order, 'items_list': items_list})




def empty_cart(request):
    return HttpResponse('empty cart')


