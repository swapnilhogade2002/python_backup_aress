from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

STATE_CHOICE={
  ('Maharashtra','Maharashtra'),
  ('Goa','Goa'),
}

class Customer(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  name=models.CharField(max_length=200)
  locality=models.CharField(max_length=200)
  city=models.CharField(max_length=200)
  zipcode=models.IntegerField()
  state=models.CharField(choices=STATE_CHOICE,max_length=50)
  
  def __str__(self) -> str:
        return str(self.id)

CATEGORY_CHOICE={
  ('E','Entertaintment'),
  ('T','Thriller'),
  ('R','Romance'),
  ('SF','ScienceFiction'), 
}

class Movies(models.Model):
  titlee=models.CharField(max_length=100)
  selling_price=models.FloatField()
  discounted_price=models.FloatField()
  description=models.TextField()
  brand=models.CharField(max_length=100)
  category=models.CharField(choices=CATEGORY_CHOICE, max_length=50)
  product_image=models.ImageField(upload_to='productimg')
  
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

    
  
  