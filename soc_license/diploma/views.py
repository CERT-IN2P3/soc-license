from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from diploma.models import Diploma

from diploma.diploma import DiplomaCtrl

import json


@csrf_exempt
def diploma_view(request, diploma):
    result = {
        'status': 'error',
        'message': 'diploma error: get unexcepted behavior'
    }
    if request.method == 'GET':
        if 'format' in request.GET:
            response_format = request.GET['format']
        else:
            response_format = 'pdf'
        try:
            sha512sum = Diploma.objects.get(uuid=diploma)
            result = {
                'status': 'success',
                'uuid': diploma,
                'sha512sum': sha512sum.sha512sum
            }
        except Diploma.DoesNotExist:
            result = {
                'status': 'failed',
                'uuid': diploma,
                'message': 'No diploma found with uuid: {uuid}'.format(uuid=diploma)
            }
        if response_format == 'pdf':
            try:
                with open('./diplomas/{}.pdf'.format(diploma), 'rb') as pdf:
                    response = HttpResponse(pdf.read())
                    response['Content-Disposition'] = 'inline;filename={}.pdf'.format(diploma)
                    return HttpResponse(response.content,
                                        content_type='application/pdf')
                pdf.closed
            except FileNotFoundError:
                pass
    return JsonResponse(result)


@csrf_exempt
def index(request):
    result = {
        'status': 'error',
        'message': 'uri:/diplomas unexcepted behavior'
    }
    if request.method == 'POST':
        data = json.loads(request.body)
        result = DiplomaCtrl.unsign(data['signature'])
    return JsonResponse(result)