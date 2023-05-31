from django.db import models
from store.models import Store,Variation
from accounts.models import Account
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class Cart_Items(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Store,on_delete=models.CASCADE,null=True)
    cart    = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    item_variation = models.ManyToManyField(Variation,blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product
    
    def sub_total(self):
        return (self.product.price*self.quantity)