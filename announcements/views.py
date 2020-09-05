from django.views.generic import ListView, DetailView

# Create your views here.
from .models import Announcement


class AnnouncementList(ListView):
    model = Announcement


class AnnouncementDetail(DetailView):
    model = Announcement
