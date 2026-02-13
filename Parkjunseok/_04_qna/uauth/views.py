from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .models import UserForm, UserDetail

def logout(request):
    # django auth앱의 logout 함수 호출
    auth_logout(request)
    return redirect('index')


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=True) # commit=False User모델 변환하되 DB저장하지 않음
            # User 모델 저장

            # 추가정보 처리 
            user_detail = UserDetail(user=user, 
                                     birthday=form.cleaned_data.get('birthday'),
                                     profile=form.cleaned_data.get('profile'))
            user_detail.save() # UserDetail 모델 저장
            print(f'회원가입 완료: {user_detail}')

            # 회원가입후 로그인 처리 
            # validation이후 cleaned_data에서 데이터 추출
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # 사용자 인증
            user = authenticate(username=username, password=raw_password)
            # 로그인처리
            auth_login(request, user)
            return redirect('index')
    
    else: 
        form = UserForm()
    
    return render(request, 'uauth/signup.html', {'form': form})