import os

from django.core.mail import send_mail
from django.views.generic import TemplateView

from blog.models import ArticlePage
from trucks.models import Truck



class IndexView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = ArticlePage.objects.all().live().order_by('?')[:3]

        # TODO BETTER TRUCKS... this probably can be quicker
        # context["trucks"] = Truck.get_trending()
        context["random_trucks"] = Truck.objects.all().order_by('?')[:4]
        context["latest_trucks"] = Truck.objects.all().order_by('-created')[:4]
        return context
