from django import template
from shop.models import Product
register = template.Library()

@register.simple_tag
def getSingleImg(product_id):
    product = Product.objects.get(id=product_id)
    if(product.images.first()):
        return product.images.first().image.url
    return ''

@register.filter
def rangeOf(value):
    return range(value)

@register.filter
def fiveProductReview(product:Product):
    reviews_count = product.reviews.all().count()
    if reviews_count>5:
        reviews = product.reviews.all()[:5]
    else:
        reviews = product.reviews.all()
    return reviews