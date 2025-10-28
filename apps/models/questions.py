from django.db.models import Model, CharField, ForeignKey, CASCADE


class Question(Model):
    title = CharField(max_length=200)
    true_answer = ForeignKey(
        'Answer',
        CASCADE,
        null=True,
        blank=True,
        related_name='correct_for'
    )

    def __str__(self):
        return self.title


class Answer(Model):
    question = ForeignKey(
        Question,
        on_delete=CASCADE,
        related_name='answers'
    )
    option = CharField(max_length=200)
    text = CharField(max_length=200)

    def __str__(self):
        return f"{self.option}"
