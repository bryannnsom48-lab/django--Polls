from .models import Question, Choice, Vote
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import F
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db import transaction # 1. Import transaction utilities


# Create your views here.

class IndexView(generic.ListView):
    
    def test_func(self):
        """
        displays the index view if the user email is as specified
        """
        
        # email = self.request.user.email
        # pattern = r"^[A-Z]+.*@.*\.com$"
        # return bool(re.match(pattern,email))
    
        
    template_name = "Polls/index.html"
    context_object_name = "latest_pub_question_list"
    #Note that the ListView authomatically produce a paginator class
    paginate_by = 5
    paginate_orphans = 4
   
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future) that also have at least one choice.
        """
        return Question.objects.filter(
            pub_date__lte = timezone.now()).exclude(choice = None).order_by("-pub_date")[:11]
        # choice gets each question, then goes to the database and check the choices if for 
        # each choice, what question_id does it correspond to
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_paginated = True #specify if the object has been paginated or not
        context["elided_range"] = context["page_obj"].paginator.get_elided_page_range(number = context["page_obj"].number, on_each_side = 3, on_ends = 2)
        context["total_members"] = User.objects.count()
        return context
    
    
from django.views import generic
from .models import Question, Vote # Make sure to import your Vote tracking model

class DetailView(generic.DetailView):
    model = Question
    template_name = "Polls/detail.html"

    def get_context_data(self, **kwargs):
        # Call the base execution first to capture your default question objects
        context = super().get_context_data(**kwargs)
        
        # Track if the active account session has already submitted an entry
        existing_vote = None
        if self.request.user.is_authenticated:
            existing_vote = Vote.objects.filter(
                user=self.request.user, 
                question=self.get_object()
            ).first()
            
        # Ship the verification variable up to your unboxed template system
        context["existing_vote"] = existing_vote
        return context

   
class ResultsView(generic.DetailView):
    model = Question
    template_name = "Polls/results.html"
    
    def get_queryset(self):
        """
        Returns the results of the the votes on the questions whose publication date is in the past
        """
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by("-pub_date")
        
@login_required()
@transaction.atomic # 2. Enforce atomic consistency
def vote(request, question_id):
    question = get_object_or_404(Question, id = question_id)
    if question.is_closed:
        return redirect("Polls:detail", question_id)
    
    # 1. CHECK IF THE USER HAS ALREADY VOTED ON THIS SPECIFIC QUESTION
    if Vote.objects.filter(user = request.user, question = question).exists():
        #User is cheating! Safely kick them over to the results template instead
        return redirect("Polls:results", question.id)
    try:
        choice_made = question.choice_set.get(id = request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        context = {
            "question":question,
            "choice_absent":"Kindly choose an Option"
        }
        return render(request, "Polls/detail.html", context)
    else:
        #2. LOG THE AUDIT ENTRY SECURELY FIRST
        Vote.objects.create(user = request.user, question = question, choice = choice_made)
        choice_made.votes = F("votes") + 1
        choice_made.save()
        return redirect("Polls:results", question_id)

@permission_required("Polls.close_question")
def close_Poll(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    
    if request.method == "POST":
        question.is_closed = True
        question.save()
        return redirect("Polls:detail", question_id)
    
    #displays confirmation page if request method is get
    return render(request, "Polls/confirm_close.html", {"question":question})

#View specifying what happens when permitted user choses to reopen the Poll
@permission_required("Polls.close_question")
def open_Poll(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    
    if request.method == "POST":
        question.is_closed = False
        question.save()
        return redirect("Polls:detail", question_id)
    
    #displays confirmation page if request method is get
    return render(request, "Polls/confirm_open.html", {"question":question})


def SignUp(request):
    #If the user is already signed in, don't let them register again
    if request.user.is_authenticated:
        return redirect("Polls:index")
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #Saves the new user securely to the database
            login(request, user) #Automatically logs the user in after registration
            return redirect("Polls:index")
    else:
        form = UserCreationForm()
            
    return render(request, "registration/register.html", {"form": form})
    