from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from soc_license.settings import SOC_LICENSE

from django.http import JsonResponse

from exam.models import Question
from exam.utils import valid_init, valid_answer

from diploma.diploma import DiplomaCtrl

import json


@csrf_exempt
def init(request):
    result = {
        'status': 'error',
        'stage': 'init',
        'message': 'error to handle uri://fqdn/exams/init/ with method {method}'.format(
            method=request.method
        )
    }
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'score' in request.session:
            result = {
                'status': 'error',
                'stage': 'message',
                'message': 'session error: a valid session is still active'
            }
        elif not valid_init(data):
            result = {
                'status': 'error',
                'stage': 'init',
                'message': 'session error: wrong init format {data}'.format(data=data)
            }
        else:
            request.session['firstname'] = data['firstname']
            request.session['lastname'] = data['lastname']
            request.session['lang'] = data['lang']
            request.session['score'] = 0
            request.session['questions'] = list()
            result = {
                'stage': 'question',
                'status': 'success',
                'basic': SOC_LICENSE['threshold']['basic'],
                'advanced': SOC_LICENSE['threshold']['advanced'],
                'expert': SOC_LICENSE['threshold']['expert'],
                'message': 'session started for {firstname} {lastname}'.format(
                    firstname=data['firstname'],
                    lastname=data['lastname']
                )
            }
    elif request.method == 'DELETE':
        if 'score' not in request.session:
            result = {
                'status': 'error',
                'stage': 'init',
                'message': 'session error: no valid session found to be closed'
            }
        else:
            firstname = request.session['firstname']
            lastname = request.session['lastname']
            request.session.flush()
            result = {
                'stage': 'init',
                'status': 'success',
                'message': 'session stop for {firstname} {lastname}'.format(
                    firstname=firstname,
                    lastname=lastname
                )
            }
    return JsonResponse(result)


@csrf_exempt
def questions(request):
    """
    Method to handle /questions

    :param request:
    :return:
    """
    result = {
        'status': 'error',
        'message': 'error to handle uri://fqdn/exams/questions/ with method {method}'.format(
            method=request.method)
    }
    if request.method == 'GET':
        if 'score' not in request.session:
            # If we not have active session
            result = {
                'status': 'error',
                'stage': 'init',
                'message': 'session error: no active session found'
            }
        elif len(request.session['questions']) == SOC_LICENSE['length']:
            result = {
                'stage': 'finished',
                'firstname': request.session['firstname'],
                'lastname': request.session['lastname'],
                'score': request.session['score'],
            }
            if request.session['score'] < SOC_LICENSE['threshold']['basic']:
                result['status'] = 'error'
            else:
                result['status'] = 'success'
                if 'uuid' not in request.session:
                    diploma = DiplomaCtrl(session=request.session)
                    request.session['uuid'] = diploma.uuid
                    request.session['signature'] = diploma.signature
                result['uuid'] = '{uuid}'.format(uuid=request.session['uuid'])
                result['signature'] = '{signature}'.format(signature=request.session['signature'])
        else:
            if request.session['score'] < SOC_LICENSE['threshold']['basic']:
                level = 'basic'
            elif request.session['score'] < SOC_LICENSE['threshold']['advanced']:
                level = 'advanced'
            else:
                level = 'expert'
            result = Question.random(used=request.session['questions'],
                                     lang=request.session['lang'],
                                     level=level)
    return JsonResponse(result)


@csrf_exempt
def answer(request, question):
    result = {
        'status': 'error',
        'message': 'error to handle uri://fqdn/exams/questions/answer with method {method}'.format(
            method=request.method)
    }
    if request.method == 'POST':
        data = json.loads(request.body)
        if valid_answer(data):
            result = Question.answer(question=question,
                                     answer=data['answer'],
                                     lang=request.session['lang'])
            request.session['score'] += result['point']
            request.session['questions'].append(question)
            result['score'] = request.session['score']
            result['questions'] = request.session['questions']
    return JsonResponse(result)
