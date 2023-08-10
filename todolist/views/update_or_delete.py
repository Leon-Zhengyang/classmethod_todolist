import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from todolist.models import Todo
from . import util
from .validation import validate
from . import error_msg

def todo_item_detail(request, pk):
    if request.method == 'PUT':
        return edit(request, pk)
    elif request.method == 'DELETE':
        return delete(request, pk)

# update todolist
@csrf_exempt
def edit(request, pk):
    # get edit request params
    data = json.loads(request.body)
    title = data.get("title", "")
    content = data.get("content", "")
    # edit data validation
    title_blank_check = validate.check_title_blank(title)
    title_double_check = validate.check_double_edit_title(title, pk)
    todo_exist_check = validate.check_exist(pk)
    if not title_double_check:
        todo_err = {"error": error_msg.err_double_title}
        return HttpResponse(json.dumps(todo_err), status=409, content_type="application/json") 
    if not title_blank_check:
        todo_err = {"error": error_msg.err_title_blank}
        return HttpResponse(json.dumps(todo_err), status=400, content_type="application/json")
    if not todo_exist_check:
        todo_err = {"error": error_msg.err_todo_exist}
        return HttpResponse(json.dumps(todo_err), status=404, content_type="application/json")

    # get exist todo data and resave it
    if title_blank_check and title_double_check:
        
        todo = Todo.objects.get(pk=pk)
        todo.title = title
        todo.content = content
        todo.save()

        # return new todo list again
        todo_lists = Todo.objects.filter(deleted=0)
        todo_arr = util.get_all_todo(todo_lists)
        return HttpResponse(json.dumps(todo_arr), status=200, content_type="application/json") 


# delete todolist
@csrf_exempt
def delete(request, pk):
    todo_exist_check = validate.check_exist(pk)
    if not todo_exist_check:
        todo_err = {"error": error_msg.err_todo_exist}
        return HttpResponse(json.dumps(todo_err), status=404, content_type="application/json")
    todo = Todo.objects.get(pk=pk)
    todo.deleted = 1
    todo.save()
    return HttpResponse(todo.id)