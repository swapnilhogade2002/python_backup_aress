from django.shortcuts import render

def learn(request):
    return render(request, 'learn/learn.html', {'title': 'Django'})
