# python manage.py shell
# import os; os.system('cls') 화면 정리 (Windows)
from post.models import Post

Post # <class 'post.models.Post'>
Post.objects # <django.db.models.manager.Manager object at 0x0000020A97852FC0>
Post.objects.all() # <QuerySet []>
queryset = Post.objects.all()
str(queryset) # 'SELECT `post_post`.`id`, `post_post`.`title`, `post_post`.`content`, `post_post`.`created_at`, `post_post`.`updated_at` FROM `post_post`'


### post 생성 ###
post = Post.objects.create(title='Hello world', content='🍭🍭🍭')
post # <Post: Hello world>
post.id # 5
post.title # 'Hello world'
post.content # '🍭🍭🍭'
post.created_at # datetime.datetime(2024, 12, 31, 0, 57, 37, 628281, tzinfo=datetime.timezone.utc)
post.updated_at # datetime.datetime(2024, 12, 31, 0, 57, 37, 628281, tzinfo=datetime.timezone.utc)

post2 = Post(title='배고프다', content='춥고 배고프다ㅠ 🤖🤖')
post2.save() # None 반환
post.id
post.title
post.content
post.created_at
post.updated_at

### post 조회 ###
queryset = Post.objects.all()
queryset # <QuerySet [<Post: Hello world>, <Post: Happy New Year 2025>, <Post: I am so happy!>]>

# 쿼리 확인
# 1.queryset.query
queryset.query # <django.db.models.sql.query.Query object at 0x0000020A96634AA0>
str(queryset.query)
# 'SELECT `post_post`.`id`, `post_post`.`title`, `post_post`.`content`, `post_post`.`created_at`, `post_post`.`updated_at` FROM `post_post`'

import sqlparse
print(sqlparse.format(str(queryset.query), reindent=True))
# SELECT `post_post`.`id`,
# `post_post`.`title`,
# `post_post`.`content`,
# `post_post`.`created_at`,
# `post_post`.`updated_at`
# FROM `post_post`

# 2.connection.queries
from django.db import connection

connection.queries # 실행된 모든 쿼리 출력
connection.queries[-1] # 마지막 쿼리

# where 조건검색
# 1. filter
# 2. get
# 3. exclude

# 특정 조건에 맞는 데이터 필터링
# filer/get 차이
Post.objects.filter(title='배고프다') # <QuerySet [<Post: (6, 배고프다)>]>
Post.objects.get(title='배고프다') # <Post: (6, 배고프다)>

# 문자열 필드
Post.objects.filter(title='Hello world') # <QuerySet [<Post: Hello world>]>
Post.objects.filter(title__startswith='Hello') # <QuerySet [<Post: Hello world>]>
Post.objects.filter(title__endswith='!') # <QuerySet [<Post: I am so happy!>]>
Post.objects.filter(content__contains='🍭') # <QuerySet [<Post: Hello world>]>
Post.objects.filter(title__icontains='happy') # 대소문자구분 없음  <QuerySet [<Post: Happy New Year 2025>, <Post: I am so happy!>]>
Post.objects.filter(content__isnull=True) # <QuerySet []>

# 날짜필드
Post.objects.filter(created_at__lte='2025-01-01') # <QuerySet [<Post: Hello world>, <Post: Happy New Year 2025>, <Post: I am so happy!>]>
Post.objects.filter(created_at__gt='2025-01-01')
Post.objects.filter(created_at__gt='2025-07-28 06:00:00')
Post.objects.filter(created_at__year=2026) # <QuerySet [<Post: Hello world>, <Post: Happy New Year 2025>, <Post: I am so happy!>]>

# 여러 조건 AND
Post.objects.filter(title='Hello world', created_at__year=2024) # <QuerySet [<Post: Hello world>]>
Post.objects.filter(title='Hello world').filter(created_at__year=2024) # <QuerySet [<Post: Hello world>]>

# 여러 조건 OR (Q 객체를 | 연산자로 연결)
from django.db.models import Q
Post.objects.filter(Q(title__contains='🍭') | Q(content__contains='🍭')) # <QuerySet [<Post: (1, Hello world123)>, <Post: (4, Hello world123)>]>

# NOT 비교
# - exclude
# - filter(~Q())

# 같은 행의 다른 컬럼 비교시 F객체 사용
from django.db.models import F
Post.objects.exclude(created_at=F('updated_at')) # <QuerySet [<Post: (1, Hello world123)>]>
Post.objects.filter(~Q(created_at=F('updated_at'))) # <QuerySet [<Post: (1, Hello world123)>]>

# 정렬
Post.objects.all().order_by('created_at')
Post.objects.all().order_by('-created_at')
Post.objects.all().order_by('title', 'id')

# 한행 조회 get
# 주로 pk컬럼 조회에 사용. 0행 또는 n행 반환시 오류
Post.objects.get(id=1) # <Post: Hello world>
Post.objects.get(id=100) # post.models.Post.DoesNotExist: Post matching query does not exist.
Post.objects.filter(id=1) # <QuerySet [<Post: Hello world>]>

# 기존 Post객체와 새롭게 질의후 반환받은 객체와 내용(pk)비교
post = Post.objects.get(id=6)
# `__eq__` 내부적으로 호출, 재정의 하지않은 `__**eq__**`는 id함수값을 비교한다.
# Model클라스는 `__**eq__`  pk비교하도록 오버라이드함.**
post == Post.objects.get(id=6) # True
Post.objects.get(id=6) is post # False
id(Post.objects.get(id=6)), id(post) # (2244515882064, 2244490451552)

# values
# - Model.objects.values(*fields)
# - values 메소드는 Django ORM에서 특정 필드만 선택해 쿼리셋을 생성할 때 사용한다.
# - 이를 활용하면 모델 객체 대신 필드 이름과 값으로 구성된 딕셔너리 형태의 쿼리셋을 반환한다.
Post.objects.values('title', 'content') # <QuerySet [{'title': 'Hello world123', 'content': '🍭🍭🍭'}, {'title': 'Happy New Year 2025', 'content': '🤖🤖🤖'}, {'title': 'I am so happy!', 'content': '😊😊😊'}, {'title': 'Hello world123', 'content': '🍭🍭🍭'}]>
Post.objects.values() # 모든 필드를 key-value로 반환
Post.objects.values('title', 'content').distinct() # 중복값 제거

# values + annotate -> group by
from django.db.models.functions import ExtractYear
from django.db.models import Count
Post.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count_by_year=Count('year'))
# <QuerySet [{'year': 2024, 'count_by_year': 3}, {'year': 2025, 'count_by_year': 1}]>


#### post 수정 ####
post = Post.objects.get(id=1)
post.title # 'Hello world'
post.title += '123'
post.title # 'Hello world123'
post.save()


#### post 삭제 ####
post = Post.objects.create(title='Delete me!', content='It was nice to have you!')
post.delete() # (1, {'post.Post': 1})

