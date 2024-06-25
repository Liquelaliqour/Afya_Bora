from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Question, Comment
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import CommentForm
from django.urls import reverse, reverse_lazy

# Create your views here.
def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

#CRUD FUNCTIONS
class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']

class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'
    ordering = ['-date_created']

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'content']
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'content']
    
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        return False

class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name = 'question'
    success_url = '/'
    
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        return False
    
class CommentDetailView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'stackkbase/question-detail.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('stackbase:question-detail')