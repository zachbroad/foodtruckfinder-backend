from django.contrib import messages


class FormSuccessMessageMixin:
    message = ''
    message_level = messages.INFO

    def form_valid(self):
        messages.add_message(self.request, self.message_level, self.message)
