from django.http import HttpResponse


def HomeView(*args, **kwargs):
    return HttpResponse("<h1>Welcome, big Brother</h1><p>This is the home page...</p>")
