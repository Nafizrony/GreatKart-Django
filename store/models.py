from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Store(models.Model):
    product_name   = models.CharField(max_length=250)
    slug           = models.SlugField(max_length=120,unique=True)
    description    = models.TextField()
    price          = models.IntegerField()
    product_images  = models.ImageField(upload_to='photos/product_images',blank=True,null=True)
    stock          = models.IntegerField()
    is_available   = models.BooleanField(default=True)
    category       = models.ForeignKey(Category,on_delete=models.CASCADE)
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse("product_details", args=[self.category.slug,self.slug])
    
class Variation_manager(models.Manager):
    def color(self):
        return super(Variation_manager,self).filter(variation_type='color',is_active=True)
    
    def size(self):
        return super(Variation_manager,self).filter(variation_type='size',is_active=True)

variation_value_type = (('color','color'),('size','size'))
class Variation(models.Model):
    product = models.ForeignKey(Store,on_delete=models.CASCADE)
    variation_type = models.CharField(max_length=100,choices=variation_value_type)
    variation_value = models.CharField(max_length=100,blank=True)
    is_active = models.BooleanField(default=True)
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)

    objects = Variation_manager()

    def __str__(self):
        return self.variation_value

