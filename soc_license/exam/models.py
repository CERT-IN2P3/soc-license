from django.db import models

from core.models import Lang


class Level(models.Model):
    description = models.CharField(max_length=20, primary_key=True)


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    @staticmethod
    def random(used, lang):
        question = Question.objects.exclude(description__in=used).order_by("?").first()
        try:
            text = QuestionText.objects.get(question=question, lang=lang)
            answers = Answer.objects.filter(question=question, lang=lang)
        except models.ObjectDoesNotExist:
            return {
                'stage': 'question',
                'status': 'error',
                'message': 'no question found'
            }
        result = {
            'stage': 'question',
            'question': question.description,
            'text': text.text,
            'answers': list()
        }
        for answer in answers:
            result['answers'].append({
                'text': answer.text,
                'id': answer.id
            })
        return result

    @staticmethod
    def answer(question, answer, lang):
        try:
            answer_model = Answer.objects.get(id=answer)
            question_model = Question.objects.get(description=question)
            question_text = QuestionText.objects.get(question=question_model, lang=lang)
        except models.ObjectDoesNotExist:
            return {
                'stage': 'answer',
                'status': 'error',
                'message': 'missing info'
            }
        if answer_model.question != question_model:
            return {
                'stage': 'answer',
                'status': 'error',
                'message': 'answer {} is not a valid answer for question {}'.format(
                    answer,
                    question
                )
            }
        return {
            'stage': 'answer',
            'status': 'success',
            'point': answer_model.point,
            'explanation': question_text.explanation
        }


class QuestionText(models.Model):
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    explanation = models.CharField(max_length=500, default="")
    tips = models.CharField(max_length=500, default="")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    point = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

