"""
URL configuration for _04_qna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/qna/', permanent=False), name='index'),
    path('qna/', include('qna.urls')),
    path('uauth/', include('uauth.urls')),
]

# 업로드한 파일 경로 설정 
# - django는 원래 정적파일을 서비스하지 않음. 개발환경에만 처리하도록 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
