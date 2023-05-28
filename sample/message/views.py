from django.shortcuts import render, redirect
from django.contrib import messages


def test_message_1(request):
    messages.add_message(request, messages.INFO, 'Hello world.')
    messages.add_message(request, messages.WARNING, 'This is a test warning message.')
    messages.add_message(request, messages.ERROR, 'This is a test error message.')
    messages.add_message(request, messages.SUCCESS, 'This is a test success message.')
    return redirect('test-messages-2')


def test_message_2(request):
    return render(request, 'test_message.html')