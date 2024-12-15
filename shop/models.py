from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args= [self.slug])
    

    class Meta: 
        ordering = ['name',]
        indexes = [
            models.Index(fields=['name']),
        ]

        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
        
        

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id,self.slug])

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id','slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    name = models.CharField(max_length=30)
    product = models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=False)
    rating = models.IntegerField(choices=[
        (1,'Terrible'),
        (2,'poor'),
        (3,'Average'),
        (4,'Good'),
        (5,'Excellent'),
    ],default=5,
    validators=[MaxValueValidator(5),MinValueValidator(1)])

    class Meta:
        ordering = ['-created']


class SiteReviewModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=False)
    rating = models.IntegerField(choices=[
        (1,'Terrible'),
        (2,'poor'),
        (3,'Average'),
        (4,'Good'),
        (5,'Excellent'),
    ],default=5,
    validators=[MaxValueValidator(5),MinValueValidator(1)])

    class Meta:
        ordering = ['-created']
