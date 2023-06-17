from django.shortcuts import render, redirect


def modal_test(request):
    return render(request, 'modal_test.html')