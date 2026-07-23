import json
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from articles.models.article import status_choices


def json_echo_view(request, *args, **kwargs):
    answer = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'method': request.method,
    }
    answer_as_json = json.dumps(answer)
    response = HttpResponse(answer_as_json)
    response['Content-Type'] = 'application/json'
    return response

@csrf_exempt
def add(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try :
        data = json.loads(request.body)
        a = data['A']
        b = data['B']

        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError

        return JsonResponse({
            "answer": a + b
        })
    except ValueError:
        return JsonResponse(
            {
                "error": "Invalid data"
            }
            , status=400
        )

@csrf_exempt
def subtract(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try :
        data = json.loads(request.body)
        a = data['A']
        b = data['B']

        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError

        return JsonResponse({
            "answer": a - b
        })
    except ValueError:
        return JsonResponse(
            {
                "error": "Invalid data"
            }
            , status=400
        )

