from django.shortcuts import render, redirect
from .models import Question, Answer, QuestionForm
from django.http import Http404
from django.core.paginator import Paginator

def index(request):
    # 질목 목록 db에서 조회
    # questions = Question.objects.all()

    # 페이징처리 
    # questions = Question.objects.order_by('-created_at')
    questions = Question.objects.prefetch_related('answer_set').order_by('-created_at')
    page = request.GET.get('page', '1') # 기본페이지 1
    paginator = Paginator(questions, 10) # 페이지당 컨텐츠 수
    page_obj = paginator.get_page(page)
    return render(request, 'qna/index.html', {'page_obj': page_obj})

def question_detail(request, question_id):
    print(f'{question_id = }')
    try: 
        question = Question.objects.get(id=question_id)
        print(f'{question = }')
        return render(request, 'qna/question_detail.html', {'question': question})
    except Question.DoesNotExist:
        raise Http404('해당 질문은 존재하지 않습니다.')
    
def answer_create(request, question_id):
    content =request.POST.get('content')
    print(f'{question_id = }')
    print(f'{content = }')

    # 1. question객체 조회
    question = Question.objects.get(id=question_id)
    # 2. answer객체 생성
    answer = Answer.objects.create(question=question, content=content)
    print(f'{question_id}번 질문에 {answer.id}번 답변이 생성되었습니다.')

    # POST 요청후에는 리다이렉트를 통해서 URL을 변경해줘야 새로고침이슈를 막을 수 있다.
    return redirect('qna:question_detail', question_id=question_id)

def answer_delete(request, answer_id):
    question_id = request.GET.get('question_id')

    answer = Answer.objects.get(id=answer_id)
    answer.delete()
    return redirect('qna:question_detail', question_id=question_id)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save() # DB에 저장
            print(f'{question = }')
            return redirect('qna:question_detail', question_id=question.id)
    else: 
        form = QuestionForm()

    return render(request, 'qna/question_form.html', {'form': form})