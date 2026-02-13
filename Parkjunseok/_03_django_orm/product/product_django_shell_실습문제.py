from product.models import Product, Review, Discount, Category
from datetime import datetime, timedelta
from django.db.models import Count, Avg

# 1. 특정 제품의 이름에 "Phone"이 포함된 제품들을 조회

# 2. 특정 카테고리 이름이 "가전"인 카테고리에 속한 모든 제품을 조회

# 3. 리뷰가 없는 제품들을 조회

# 4. 평점이 4 이상인 리뷰가 달린 제품을 조회

# 5. 특정 할인율(예: 10%)보다 높은 할인을 적용받는 제품을 조회

# 6. 특정 날짜 (2025/02/01) 이후에 시작된 할인 정보를 가진 제품들을 조회

# 7. "패션"이라는 이름이 포함된 카테고리에 속한 모든 제품을 조회

# 8. 3개 이상의 카테고리에 속한 제품을 조회

# 9. 재고가 10이하인 제품들을 조회

# 10. "최상"라는 단어가 설명(description)에 포함된 제품들을 조회

# 11. 이번달에 작성된 리뷰 조회

# 12. 현재 할인중인 제품을 조회

# 13. 리뷰 수가 3개 이상인 제품들을 조회

# 14. 특정 사용자(user_id = 2)가 작성한 모든 리뷰를 조회

# 15. 평균 평점이 4.5 이상인 제품들을 조회

# 16. 특정 카테고리(가전)의 제품들 중 가격이 100,000원 이상인 제품을 조회

# 17. 20% 이상의 할인율을 적용받는 모든 제품을 조회

# 18. 가격이 50,000원 이상이고 재고가 10개 이상인 제품을 조회

# 19. 5점 만점 리뷰가 하나라도 달린 제품을 조회

# 20. 가장 최근 리뷰가 작성된 제품을 조회

# 문제 풀이 

from django.db.models import Count, Avg
from django.utils import timezone
# 앱 이름이 'product'라고 가정합니다. 폴더명에 따라 'from [앱이름].models'로 수정하세요.
from product.models import Product, Category, Review, Discount
from django.utils import timezone

# 1. 특정 제품의 이름에 "Phone"이 포함된 제품들을 조회
product1 = Product.objects.filter(name__icontains="Phone") # [변수에 담기]
Product.objects.filter(name__icontains="Phone")            # [바로 조회]
print(product1)                                            # [담고 나서 확인]

# 2. 특정 카테고리 이름이 "가전"인 카테고리에 속한 모든 제품을 조회
product2 = Product.objects.filter(categories__name="가전")
Product.objects.filter(categories__name="가전")
print(product2)

# 3. 리뷰가 없는 제품들을 조회
product3 = Product.objects.filter(reviews__isnull=True)
Product.objects.filter(reviews__isnull=True)
print(product3)

# 4. 평점이 4 이상인 리뷰가 달린 제품을 조회 (중복 제거)
product4 = Product.objects.filter(reviews__rating__gte=4).distinct()
Product.objects.filter(reviews__rating__gte=4).distinct()
print(product4)

# 5. 특정 할인율(예: 0.10 = 10%)보다 높은 할인을 적용받는 제품을 조회
product5 = Product.objects.filter(discount__discount_percentage__gt=0.10)
Product.objects.filter(discount__discount_percentage__gt=0.10)
print(product5)

# 6. 특정 날짜 (2025/02/01) 이후에 시작된 할인 정보를 가진 제품들을 조회
product6 = Product.objects.filter(discount__start_date__gt='2025-02-01')
Product.objects.filter(discount__start_date__gt='2025-02-01')
print(product6)

# 7. "패션"이라는 이름이 포함된 카테고리에 속한 모든 제품을 조회
product7 = Product.objects.filter(categories__name__icontains="패션")
Product.objects.filter(categories__name__icontains="패션")
print(product7)

# 8. 3개 이상의 카테고리에 속한 제품을 조회 # 패키지 임포트부터 해야 함 
product8 = Product.objects.annotate(c_count=Count('categories')).filter(c_count__gte=3)
Product.objects.annotate(c_count=Count('categories')).filter(c_count__gte=3)
print(product8)

# 9. 재고가 10이하인 제품들을 조회
product9 = Product.objects.filter(stock__lte=10)
Product.objects.filter(stock__lte=10)
print(product9)

# 10. "최상"라는 단어가 설명(description)에 포함된 제품들을 조회
product10 = Product.objects.filter(description__icontains="최상")
Product.objects.filter(description__icontains="최상")
print(product10)

# 11. 이번달(2026년 2월)에 작성된 리뷰 조회
product11 = Review.objects.filter(created_at__year=2026, created_at__month=2)
Review.objects.filter(created_at__year=2026, created_at__month=2)
print(product11)

# 12. 현재 할인중인 제품을 조회 # 패키지 임포트 부터 해야 함 
now = timezone.now()
product12 = Product.objects.filter(discount__start_date__lte=now, discount__end_date__gte=now)
Product.objects.filter(discount__start_date__lte=timezone.now(), discount__end_date__gte=timezone.now())
print(product12)

# 13. 리뷰 수가 3개 이상인 제품들을 조회 # 패키지 임포트 부터 해야 함 
product13 = Product.objects.annotate(r_count=Count('reviews')).filter(r_count__gte=3)
Product.objects.annotate(r_count=Count('reviews')).filter(r_count__gte=3)
print(product13)

# 14. 특정 사용자(user_id = 2)가 작성한 모든 리뷰를 조회
product14 = Review.objects.filter(user_id=2)
Review.objects.filter(user_id=2)
print(product14)

# 15. 평균 평점이 4.5 이상인 제품들을 조회
product15 = Product.objects.annotate(avg_r=Avg('reviews__rating')).filter(avg_r__gte=4.5)
Product.objects.annotate(avg_r=Avg('reviews__rating')).filter(avg_r__gte=4.5)
print(product15)

# 16. 특정 카테고리(가전)의 제품들 중 가격이 100,000원 이상인 제품을 조회
product16 = Product.objects.filter(categories__name="가전", price__gte=100000)
Product.objects.filter(categories__name="가전", price__gte=100000)
print(product16)

# 17. 20%(0.20) 이상의 할인율을 적용받는 모든 제품을 조회
product17 = Product.objects.filter(discount__discount_percentage__gte=0.20)
Product.objects.filter(discount__discount_percentage__gte=0.20)
print(product17)

# 18. 가격이 50,000원 이상이고 재고가 10개 이상인 제품을 조회
product18 = Product.objects.filter(price__gte=50000, stock__gte=10)
Product.objects.filter(price__gte=50000, stock__gte=10)
print(product18)

# 19. 5점 만점 리뷰가 하나라도 달린 제품을 조회
product19 = Product.objects.filter(reviews__rating=5).distinct()
Product.objects.filter(reviews__rating=5).distinct()
print(product19)

# 20. 가장 최근 리뷰가 작성된 제품을 조회
product20 = Product.objects.filter(reviews__isnull=False).order_by('-reviews__created_at')[:1]
Product.objects.filter(reviews__isnull=False).order_by('-reviews__created_at')[:1]
print(product20)