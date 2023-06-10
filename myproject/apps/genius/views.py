from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Action

def book_list(request):
    books = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
        {"title": "1984", "author": "George Orwell"}
    ]
    return JsonResponse({"books": books})

def action_list(request):
    actions = Action.object.Action()
    data = {'actions':list(actions.values())}
    return JsonResponse(data)