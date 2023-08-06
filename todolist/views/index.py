import json
from django.shortcuts import render
from django.http import HttpResponse

from todolist.models import Todo
from . import util

def index(request): 
    return render(request, "index.html")

# get all todolist
def all_list(request):
    if request.method == "GET": 
        # return all todo lists for first time 
        todo_lists = Todo.objects.filter(deleted=0)
        todo_arr = util.get_all_todo(todo_lists)
    return HttpResponse(json.dumps(todo_arr), status=200, content_type="application/json") 
