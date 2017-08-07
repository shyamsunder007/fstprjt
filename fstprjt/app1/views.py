from django.http import HttpResponse
from .models import Question
from django.template import loader

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# Create your views here.
from django.views import generic

from .models import Choice, Question
from django.utils import timezone
class IndexView(generic.ListView):
	template_name='app1/index.html'
	context_object_name='latest_question_list'
	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]
class DetailView(generic.DetailView):
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'app1/results.html'
# Create your views here.
def index(request):
	latest_question_list=Question.objects.order_by('-pub_date')[:5]
	context={ 'latest_question_list':latest_question_list,}
	return render(request,'app1/index.html',context)
def detail(request,question_id):
	question=get_object_or_404(Question,pk=question_id)
	return render(request,'app1/detail.html', {'question':question})
def results(request,question_id):
	question=get_object_or_404(Question,pk=question_id)
	return render(request,'app1/results.html',{'question':question})

def vote(request,question_id):		
	question=get_object_or_404(Question,pk=question_id)
	try:
		selected_choice=question.choice_set.get(pk=request.POST['choice'])
	except (KeyError,Choice.DoesNotExist):
		return render(request,'app1/detail.html',{'question':question,
			'error_message':"You didn't select a choice.",})
	else:
		selected_choice.votes+=1
		selected_choice.save()
		return HttpResponseRedirect(reverse('app1:results',args=(question.id,)))

