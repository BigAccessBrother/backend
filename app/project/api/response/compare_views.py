from django.http import HttpResponse


def CompareView(*args, **kwargs):
    return HttpResponse("<h1>Here you gonna see the comparision of security standards and agents' response.<h1>")
