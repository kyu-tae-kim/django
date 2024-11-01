from ..models import Answer, Question
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..forms import AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import  HttpResponseNotAllowed


@login_required(login_url='common:login')
def answer_create(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():       
            answer = form.save (commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('article:detail', question_id = question.id), answer.id))
    else:
        return HttpResponseNotAllowed('Only Post method using possible')
    context = {'question': question, 'form':form}
    return render(request,'article/question_detail.html',context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect('article:detail', question_id = answer.question.id)
    if request.method == "POST": 
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('article:detail', question_id = answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'form':form}
    return render(request, 'article/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect('article:delete', question_id = answer.question.id)
    answer.delete()
    return redirect('{}#answer_{}'.format(
    resolve_url('article:detail', question_id = answer.question.id), answer.id))

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request,"본인이 작성한 글에는 좋아요를 할 수 없습니다.")
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
    resolve_url('article:detail', question_id = answer.question.id), answer.id))
