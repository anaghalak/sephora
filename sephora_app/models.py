from django.db import models
class UserRegister(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True)



class Product(models.Model):
    user = models.ForeignKey(
        UserRegister,
        on_delete=models.CASCADE,
        related_name='products'
    )
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name 