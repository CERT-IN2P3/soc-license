from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from diploma.diploma import DiplomaCtrl

import json


@csrf_exempt
def diploma_view(request, uuid, format):
    result = {
        'status': 'error',
        'message': 'diploma error: get unexcepted behavior'
    }
    if request.method == 'GET':
        if 'data' in request.GET:
            data = json.loads(request.GET['data'])
            print('diploma_view()\n    data: {}'.format(data))
        elif request.body.decode('utf-8') != '':
            data = json.loads(request.body)
        else:
            data = dict()
        if 'signature' in data:
            signature = data['signature']
        else:
            signature = None

        diploma = DiplomaCtrl(session=request.session,
                              uuid=uuid,
                              signature=signature)
        result = diploma.get(format)
        if format == 'pdf':
            response = HttpResponse(result)
            response['Content-Disposition'] = 'inline;filename={}.pdf'.format(diploma)
            return HttpResponse(response.content,
                                content_type='application/pdf')
    return JsonResponse(result)


@csrf_exempt
def index(request):
    result = {
        'status': 'error',
        'message': 'uri:/diplomas unexcepted behavior'
    }
    if request.method == 'POST':
        data = json.loads(request.body)
        print('diploma_view()\n    uuid: {}\n    signature: {}'.format(data['uuid'], data['signature']))
        diploma = DiplomaCtrl(session=request.session,
                              uuid=data['uuid'],
                              signature=data['signature'])
        result = diploma.unsign()
    return JsonResponse(result)