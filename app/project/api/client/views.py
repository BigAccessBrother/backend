from django.http import HttpResponse


def ListAllClients(*args, **kwargs):
    return HttpResponse("<h1>List all clients</h1>")
