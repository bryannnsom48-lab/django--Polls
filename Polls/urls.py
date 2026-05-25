from django.urls import path
from . import views

app_name = "Polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name = "index"),
    path("<int:pk>/detail/", views.DetailView.as_view(), name = "detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name = "results"),  
    path("<int:question_id>/vote/", views.vote, name = "votes"),
    path("<int:question_id>/close/", views.close_Poll, name="close_Poll"),
    path("<int:question_id>/open/", views.open_Poll, name="open_Poll"),
    path("register/", views.SignUp, name = "SignUp"),
    
]
#central routing map for your web application