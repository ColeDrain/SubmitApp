from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question, Solution
from .forms import SubmitForm, QuestionUploadForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.list import MultipleObjectMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import login, authenticate

# Create your views here.

@login_required
def home(request):
    question = Question.objects.filter(upload_date=datetime.now().date())

    if question:
        question = question[0]
        solutions = Solution.objects.filter(question=question)
        page = request.GET.get('page', 1)
        paginator = Paginator(solutions, 1)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except:
            page_obj = paginator.page(paginator.num_pages)
    else:
        question = []
        page_obj = []

    return render(request, 'SubmitApp/home.html', {'question': question, 'page_obj': page_obj,})

def about(request):
    return render(request, 'SubmitApp/about.html')

@login_required
def submit_form(request):
    question = Question.objects.filter(upload_date=datetime.now().date())
    if question:
        question = question[0]
        if request.method == 'POST':
            form = SubmitForm(request.POST, request.FILES)
            if form.is_valid():
                solution = form.save(commit=False)
                solution.author = request.user
                solution.save()
                return redirect('home')
        else:
            form = SubmitForm()
    else:
        question = []
        form = []

    return render(request, 'SubmitApp/answer.html', {'question':question, 'form':form})   

@login_required
def question_upload(request):
    if request.user.is_staff:
        question = Question.objects.filter(upload_date=datetime.now().date())

        if not question:
            if request.method == 'POST':
                form = QuestionUploadForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('home')
            else:
                form = QuestionUploadForm()
        else:
            form = []

        return render(request, 'SubmitApp/question_upload.html', {'form':form})
    else:
        return render(request, 'SubmitApp/forbidden.html')

@login_required
def update(request, id):
    if request.user.is_staff:
        question = Question.objects.get(id=id)
        qid = question.id
        today_list = Question.objects.filter(upload_date=datetime.now().date())
        # Check if list is empty
        if today_list:
            today_question = today_list[0]
            tid = today_question.id
            # Restrict update to only today's question..
            if tid==qid:
                form = QuestionUploadForm(request.POST or None, instance=question)
                if form.is_valid():
                    form.save()
                    return redirect('home')
            else:
                return render(request, 'SubmitApp/forbidden.html')
        else:
            return render(request, 'SubmitApp/forbidden.html')
            
        return render(request, 'SubmitApp/question_update.html', {'form':form})
    else:
        return render(request, 'SubmitApp/forbidden.html')

@login_required
def admin_page(request):
    if request.user.is_staff:
        questions = Question.objects.order_by('upload_date')
        question = Question.objects.filter(upload_date=datetime.now().date())

        if question:
            question = question[0]

        page = request.GET.get('page', 1)
        paginator = Paginator(questions, 1)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, 'SubmitApp/admin_welcome_page.html', {'question':question, 'questions':questions, 'page_obj': page_obj,})
    else:
        return render(request, 'SubmitApp/forbidden.html')

@login_required
def question_detail(request, id):
    question = Question.objects.get(id=id)
    qid = question.id
    # Get today's question id
    today_list = Question.objects.filter(upload_date=datetime.now().date())
    if today_list:
        today_question = today_list[0]
        tid = today_question.id

    if question:
        solutions = Solution.objects.filter(question=question)
        page = request.GET.get('page', 1)
        paginator = Paginator(solutions, 1)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except:
            page_obj = paginator.page(paginator.num_pages)
    else:
        question = []
        page_obj = []

    return render(request, 'SubmitApp/question_detail.html', {'question': question, 'page_obj': page_obj, 'qid':qid, 'tid':tid})