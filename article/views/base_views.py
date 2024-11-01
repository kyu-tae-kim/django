from ..models import Question, Test
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q


def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 질문 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 작성자 검색
            Q(answer__author__username__icontains=kw)  # 답변 작성자 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'article/question_list.html', context)


def detail(request,question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question,pk=question_id)
    context = {"question" : question}
    return render(request,'article/question_detail.html',context)

def insert(requst):
    for i in range(300):
        q = Question(subject= f'테스트 데이터 : {i}',
                     content = '테스트',
                     create_date = timezone.now())
        q.save()
    return HttpResponse("데이터 입력 완료")

def show(request):
    display_all = Test.objects.all()
    result = ""
    for t in display_all:
        result += "<h1>"+ t.name + "</h1>" + "<br>"
    
    return HttpResponse(result)

def detail(request,question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question,pk=question_id)
    context = {"question" : question}
    return render(request,'article/question_detail.html',context)