from ..models import Question
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms import QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='common:login')
def question_create(request) :
    if request.method == 'POST': # 요청이 Post 방식인지 확인
        # 요청이 Post 방식인건 "저장하기" 버튼을 눌렀을때만
        form = QuestionForm(request.POST) # QuestionForm에 입력 값 넣기 
        if form.is_valid(): # 해당 form의 형식이 맞는지 검사
            # 입력받은 subhect 와 content를 모델에 저장
            # 모델에 저장은 하는데 해당 모델의 commit은 하지않음 
            # 아직 create_date라는 속성값이 정의 되지 않았기 떄문에
            # commit을 하면 에러가 발생함
            question = form.save(commit=False)
            question.author = request.user
            # 현재 시각으로 create_date 저장
            question.create_date = timezone.now()
            # model에서 필요한 모든 값이 저장 되었음으로 
            # commit 완료
            question.save()
            
            ## 데이터의 저장이 끝나면 이제 기본 페이지로 이동
            return redirect('article:index')
    else:
        form = QuestionForm()
    form = QuestionForm()
    return render(request, 'article/question_form.html', {'form': form})

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect('article:detail', question_id=question.id)
    if request.method == 'POST': 
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('article:detail', question_id = question.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'article/question_form.html', {'form': form})

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect('article:delete', question_id = question.id)
    question.delete()
    return redirect('article:index')

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request,"본인이 작성한 글에는 좋아요를 할 수 없습니다.")
    else:
        question.voter.add(request.user)
    return redirect('article:detail', question_id=question.id)