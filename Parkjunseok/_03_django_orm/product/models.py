from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True) # 폼입력시 공란 허용 
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) # 등록시만 현재시각 입력
    updated_at = models.DateTimeField(auto_now=True) # 등록/수정 현재시각 입력

    def __str__(self):
        return self.name

# 1:1관계 
class Discount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='discount')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text='Discount Percentage: (e.g 0.10 for 10%)')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.discount_percentage}% off for {self.product.name}'
    
# 1:N관계
class Review(models.Model):
    # Review: product 참조
    # Product: reviews 참조 (related_name값)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews') 
    user_id = models.PositiveIntegerField(blank=True, null=True) # null=True db테이블 컬럼 null 허용
    rating = models.PositiveIntegerField(default=1, help_text='Rating from 1 to 5')
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.user_id}'

# N:M관계 
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField(Product, related_name='categories')

    def __str__(self):
        return self.name
