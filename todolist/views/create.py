import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from todolist.models import Todo
from . import util
from .validation import validate
from . import error_msg


# create new todolist
@csrf_exempt
def create_todo_item(request):
   if request.method == "POST":
    # get regist request params
    data = json.loads(request.body)
    title = data.get("title", "")
    content = data.get("content", "")

    # regist data validation
    title_blank_check = validate.check_title_blank(title)
    title_double_check = validate.check_double_title(title)
    if not title_double_check:
        todo_err = {"error": error_msg.err_double_title}
        return HttpResponse(json.dumps(todo_err), status=409, content_type="application/json") 
    if not title_blank_check:
        todo_err = {"error": error_msg.err_title_blank}
        return HttpResponse(json.dumps(todo_err), status=400, content_type="application/json") 

    # create new todo list
    if title_blank_check and title_double_check:
        Todo.objects.create(
            title=title,
            content=content
        )
        todo_lists = Todo.objects.filter(deleted=0)

        todo_arr = util.get_all_todo(todo_lists)
    return HttpResponse(json.dumps(todo_arr), status=201, content_type="application/json") 