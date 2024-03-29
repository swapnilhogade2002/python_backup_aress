from django.shortcuts import render

# Define the learn view function
def learn(request):
    return render(request, 'course/course.html', {'title': 'learn Django'})
