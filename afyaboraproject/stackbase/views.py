from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Question
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


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

class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'content']
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class QuestionUpdateView(UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['title', 'content']
    
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False

    #def form_valid(self, form):
        #form.instance.user = self.request.user
        #return super().form_valid(form)