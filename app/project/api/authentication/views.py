from django.http import HttpResponse


def AuthView(*args, **kwargs):
    return HttpResponse("<h1>Login Page</p>")
