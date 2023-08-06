import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from todolist.models import Todo
from . import util


# search todolist
@csrf_exempt
def get_todo_list(request):
    if request.method == 'POST':
        # get search params
        data = json.loads(request.body)
        title_search = data.get("title_search", "")
        content_search = data.get("content_search", "")

        # filter todo list by above conditions
        q_title = Q(title__icontains=title_search) if title_search else Q()
        q_content = Q(content__icontains=content_search) if content_search else Q()

        todo_list = Todo.objects.filter(
            q_title, q_content, Q(deleted=0)
        )
        todo_arr = util.get_all_todo(todo_list)

    return HttpResponse(json.dumps(todo_arr), status=200, content_type="application/json") 