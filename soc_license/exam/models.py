from django.db import models

from core.models import Lang


class Level(models.Model):
    description = models.CharField(max_length=20, primary_key=True)


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    @staticmethod
    def random(used, lang, level):
        question = Question.objects.exclude(id__in=used).filter(level=level).order_by("?").first()
        try:
            text = question.locale_question(lang=lang)
            locale_answers = list()
            for answer in Answer.objects.filter(question=question).order_by("?"):
                locale_answers.append(answer.locale_answer(lang=lang))
        except models.ObjectDoesNotExist:
            return {
                'stage': 'question',
                'status': 'error',
                'message': 'no question found'
            }
        result = {
            'stage': 'question',
            'question': text['id'],
            'text': text['text'],
            'level': question.level.description,
            'answers': list()
        }
        for answer in locale_answers:
            print(answer)
            result['answers'].append({
                'text': answer["text"],
                'id': answer["id"]
            })
        return result

    def locale_question(self, lang):
        question = QuestionText.objects.get(question=self, lang=lang)
        return {
            'text': question.text,
            'id': self.id
        }

    @staticmethod
    def answer(question, answer, lang):
        try:
            answer_model = Answer.objects.get(id=answer)
            question_model = Question.objects.get(id=question)
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
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    count = models.PositiveIntegerField(default=0)

    def locale_answer(self, lang):
        answer = AnswerText.objects.get(answer=self, lang=lang)
        return {
            'text': answer.text,
            'id': self.id
        }


class AnswerText(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

