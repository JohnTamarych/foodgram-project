from django.shortcuts import render


def handler404(request, exception):
    return render(request, 'includes/404.html')


def handler500(request, *args, **kwargs):
    return render(request, 'includes/500.html')
