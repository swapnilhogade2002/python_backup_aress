from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

STATE_CHOICE={
  ('Maharashtra','Maharashtra'),
  ('Goa','Goa'),
}

ROLL_CHOICES = [
    ('user', 'User'),
    ('theater', 'Theater'),
]


class Customer(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  name=models.CharField(max_length=200)
  locality=models.CharField(max_length=200)
  city=models.CharField(max_length=200)
  zipcode=models.IntegerField()
  state=models.CharField(choices=STATE_CHOICE,max_length=50)
  roll = models.CharField(choices=ROLL_CHOICES, max_length=10, default="user")
  
  def __str__(self) -> str:
        return str(self.id)

CATEGORY_CHOICE={
  ('E','Entertaintment'),
  ('T','Thriller'),
  ('R','Romance'),
  ('SF','ScienceFiction'), 
}

SHOW_TIME_CHOICES = [
        ('9 AM -1 PM', '9:00 AM - 1:00 PM'),
        ('1 PM -4 PM', '1:00 PM - 4:00 PM'),
        ('4 PM -7 PM', '4:00 PM - 7:00 PM'),
        ('7 PM -10 PM', '7:00 PM - 10:00 PM'),
    ]

class Movies(models.Model):
  titlee=models.CharField(max_length=100)
  selling_price=models.FloatField()
  discounted_price=models.FloatField()
  description=models.TextField()
  brand=models.CharField(max_length=100)
  category=models.CharField(choices=CATEGORY_CHOICE, max_length=50)
  product_image=models.ImageField(upload_to='productimg')
  theater_name = models.CharField(max_length=100, default='Default Theater')
  show_time = models.CharField(choices=SHOW_TIME_CHOICES, max_length=100, default='9-1')
  address = models.CharField(max_length=255, blank=True, null=True)  
  added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_movies', default=1)
  def __str__(self) -> str:
        return str(self.id)
  
  
class Cart(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  product=models.ForeignKey(Movies,to_field='id',on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)
  
  def __str__(self) -> str:
        return str(self.id)      

STATUS_CHOICE={
  ('Booked','Booked'),
  ('Cancel','Cancel'),
}

class OrderPlaced(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
  product=models.ForeignKey(Movies,on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)
  ordered_date=models.DateTimeField(auto_now_add=True)
  status=models.CharField(max_length=50,choices=STATUS_CHOICE,default='Pending')
  
  def __str__(self) -> str:
        return str(self.id) 
      

class TheaterTicketBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    seat = models.CharField(max_length=100, default='0')  

    def __str__(self) -> str:
        return str(self.id) 


  
  