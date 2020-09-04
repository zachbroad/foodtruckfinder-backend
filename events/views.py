from django.views.generic import ListView, DetailView

# Create your views here.
from events.models import Event


class EventList(ListView):
    model = Event


class EventDetail(DetailView):
    model = Event
