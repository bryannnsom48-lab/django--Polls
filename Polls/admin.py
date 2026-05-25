from django.contrib import admin


# Register your models here.
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    
class QuestionAdminClass(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields":["question_text"]}),("Date Information", {"fields": ["pub_date"], "classes": ["collapse"]})
    ]

    list_filter = ["pub_date"]
        
    search_fields = ["question_text"]
    
    list_display = ["question_text", "pub_date", "was_published_recently"]
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "question_text":
            field.widget.attrs["placeholder"] = "Create New Question"
        # elif field.name == "choice_text": 
        #     field.widget.attrs["placeholder"] = "Enter Choice"
        return field
    
    inlines = [ChoiceInline]
    
admin.site.register(Question, QuestionAdminClass)
    

