import datetime
from django.utils import timezone
from django.test import TestCase
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse


# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_using_future_question(self):
        """
        was_published_recently returns False for questions in the future
        """
        future_question = Question(pub_date = ((timezone.now()) + (datetime.timedelta(days=30))))
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_using_old_question(self):
        """
        was_published_recently returns True for questions whose publication date is one day older
        """
        old_question = Question(pub_date = ((timezone.now()) - (datetime.timedelta(days=1, seconds=1))))
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_published_recently_using_recent_question(self):
        """
        was_published_recently returns True for questions whose publication date is inbetween the last 1 day(24 hours)"""
        recent_question = Question(pub_date = ((timezone.now()) - (datetime.timedelta(hours=23, minutes=59, seconds=59))))
        self.assertIs(recent_question.was_published_recently(), True)
    
def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the given number of 'days' offset to now (negative for questions published in the past, positve for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text = question_text, pub_date = time)
    
class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        If no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse("Polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No questions available")
        self.assertQuerySetEqual(
            response.context["latest_pub_question_list"], []
        )
        
    def test_past_question(self):
        """
        Question with a pub_date in the past are displayed on the index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        question.choice_set.create(choice_text = "choice1", votes = 0)
        response = self.client.get(reverse("Polls:index"))    
        self.assertQuerySetEqual(
           response.context["latest_pub_question_list"], [question],
        )    
    def test_future_question(self):
        """
        Question with pub_date in the future aren't displayed on the index page.
        """
        question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("Polls:index"))
        self.assertContains(response, "No questions available")
        self.assertQuerySetEqual(
            response.context["latest_pub_question_list"], []
        )
    
    def test_future_question_and_past_question(self):
        """
        Even if both future and past questions exist, only past questions are displayed
        """
        question = create_question(question_text="Past question", days=-30)
        question.choice_set.create(choice_text = "choice1", votes = 0)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("Polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_pub_question_list"], [question],
        )
    
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions with publication dates in the past
        """
        question1 = create_question(question_text="Past question1", days=-30)
        question2 = create_question(question_text="Past question2", days=-10)
        question1.choice_set.create(choice_text = "choice1", votes = 0)
        question2.choice_set.create(choice_text = "choice1", votes = 0)
        response = self.client.get(reverse("Polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_pub_question_list"], [question2, question1],
        )
      
    def test_question_with_choice(self):
        """
        Index view display questions with atleast a choice
        """
        question = create_question("Question with choices", days=-5)
        question.choice_set.create(choice_text= "choice1", votes = 0)
        response = self.client.get(reverse("Polls:index"))
        self.assertContains(response, question.question_text)
        self.assertQuerySetEqual(response.context["latest_pub_question_list"], [question])
        
    def test_question_with_no_choice(self):
        """
        Index view fails to diplay questions with no available choices
        """
        create_question("Question with no choice", days=-5)
        response = self.client.get(reverse("Polls:index"))
        self.assertQuerySetEqual(response.context["latest_pub_question_list"], [])
        
class QuestionDetailViewTest(TestCase):
    def test_details_for_PastXFuture_question(self):
        """
        Detail view of a question with pub_date in the past should be displayed (with legent = question_text) but Detail view for  question with pub_date in the future should not be found
        """
        now = timezone.now()
        question = create_question(question_text="Past question", days=-1)
        response = self.client.get(reverse("Polls:detail", args=(question.id,)))
        if question.pub_date < now:
            self.assertContains(response, question.question_text)
        else:
            self.assertEqual(response.status_code, 404)
            
class QuestionResultsIndexViewTests(TestCase):
    def test_results_for_PastXFuture_question(self):
        """
        Result view returns results for questions with publication date in the past but returns Not found for questions with publication date in the future
        """
        question = create_question(question_text="Past question", days=-2)
        response = self.client.get(reverse("Polls:results", args=(question.id,)))
        if question.pub_date < timezone.now():
            self.assertContains(response, question.question_text)
        else:
            self.assertContains(response.status_code, 404)
            
      
        
        
        
        
        
    
        