from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote

# Create your views here.

fixFlaw4 = False #Set this to True in order to fix the fourth problem.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#@login_required #This fixes the second flaw.
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if (fixFlaw4):
            choice = get_object_or_404(Choice, pk=question_id)
            if Vote.objects.filter(choice=choice,voter=request.user).exists():
                return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You have already voted on this question.",
            })
            selected_choice.votes += 1
            selected_choice.save()
            Vote.objects.create(voter=request.user, choice=choice)
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
            #shows results