from django.db import models
from django.contrib.auth.models import User

class food(models.Model):
    type_of_food = [
    ("VEG", "VEGETARIAN"),
    ("NON-VEG", "NON-VEGETARIAN"),   
]
    food_catagory = [
    ("WL", "WEIGHT-LOSS"),
    ("WG", "WEIGHT-GAIN"),   
]
    
    food_name = models.CharField(max_length=30)
    food_type = models.CharField(max_length=7, choices=type_of_food)
    catagory = models.CharField(max_length=2, choices=food_catagory)
    photo = models.ImageField(upload_to='photos/')
    discription = models.TextField()
    price = models.IntegerField(null=False, default=100)

    def __str__(self):
        return f'{self.food_name} and {self.food_type} price is {self.price}'
    
class discount(models.Model):
    original_food = models.ForeignKey(food, on_delete=models.CASCADE)  
    discount_percentage = models.FloatField(default=40.00)
    discounted_price = models.FloatField(editable=False, null=False)

    def save(self, *args, **kwargs):
        
        self.discounted_price = self.original_food.price * (1 - (self.discount_percentage / 100))
        super().save(*args, **kwargs)  
    def __str__(self):
        return f'Discounted {self.original_food.food_name}: Now at {self.discounted_price}'


#this is cart model 

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.food.food_name} for {self.user.username}'
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f'Profile for {self.user.username}'
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    items = models.ManyToManyField('CartItem', related_name='orders')  # Track cart items
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        self.total_price = sum(
            item.food.price * item.quantity for item in self.items.all()
        )
        self.save()

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"






    




