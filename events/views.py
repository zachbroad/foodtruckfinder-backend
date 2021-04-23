from django.db.models import Q
from django.views.generic import ListView, DetailView

# Create your views here.
from events.models import Event


class EventList(ListView):
    model = Event

    def get_queryset(self):
        if query := self.request.GET.get('query'):
            return Event.objects.filter(Q(trucks__events__description__icontains=query) | Q(trucks__title__icontains=query))

        return super(EventList, self).get_queryset()


class EventDetail(DetailView):
    model = Event
