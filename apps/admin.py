from django.contrib import admin

from .models import User
from .models.questions import Answer, Question


class QuestionAnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','title','true_answer']
    inlines = [QuestionAnswerInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "true_answer":
            if request.resolver_match.kwargs.get('object_id'):
                question_id = request.resolver_match.kwargs['object_id']
                kwargs["queryset"] = Answer.objects.filter(question_id=question_id)
            else:
                kwargs["queryset"] = Answer.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Answer)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ['question','option','text']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone','first_name','last_name','email']

