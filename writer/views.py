from django.shortcuts import HttpResponse


def writer_home(request):
    return HttpResponse("<h1>hello writer</h1>")




