from django.shortcuts import render, redirect
from django.contrib import messages


def message_test(request):
    messages.add_message(request, messages.DEBUG, 'Debug message.')
    messages.add_message(request, messages.INFO, 'Hello world.')
    messages.add_message(request, messages.WARNING, 'This is a test warning message.')
    messages.add_message(request, messages.ERROR, 'This is a test error message.')
    messages.add_message(request, messages.SUCCESS, 'This is a test success message.')
    return redirect('message-test-phase2')


def message_test_phase2(request):
    return render(request, 'message_test.html')