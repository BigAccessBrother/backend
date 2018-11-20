from django.http import HttpResponse


def GetClientsResponsesView(*args, **kwargs):
    return HttpResponse("<h1>Gonna see clients responses</h1>")
