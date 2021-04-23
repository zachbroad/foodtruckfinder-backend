import graphene
from graphene_django import DjangoObjectType

from announcements.models import Announcement
from catering.models import CaterRequest
from events.models import Event
from trucks.models import Truck
from users.models import User


class TruckType(DjangoObjectType):
    class Meta:
        model = Truck
        fields = '__all__'


class TruckQuery(graphene.ObjectType):
    trucks = graphene.List(TruckType)
    truck = graphene.Field(TruckType, id=graphene.Int(required=True))

    def resolve_trucks(self, info):
        return Truck.objects.all()

    def resolve_truck(self, info, id):
        return Truck.objects.get(id=id)


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = '__all__'


class EventQuery(graphene.ObjectType):
    events = graphene.List(EventType)
    event = graphene.Field(EventType, id=graphene.Int(required=True))

    def resolve_events(self, info):
        return Event.objects.all()

    def resolve_event(self, info, id):
        return Event.objects.get(id=id)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(id=id)


class CateringType(DjangoObjectType):
    class Meta:
        model = CaterRequest
        fields = '__all__'


class CateringQuery(graphene.ObjectType):
    cater_requests = graphene.List(CateringType)
    cater_request = graphene.Field(CateringType, id=graphene.Int(required=True))

    def resolve_cater_requests(self, info):
        return CaterRequest.objects.all()

    def resolve_cater_request(self, info, id):
        return CaterRequest.objects.get(id=id)


class AnnouncementType(DjangoObjectType):
    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementQuery(graphene.ObjectType):
    announcements = graphene.List(AnnouncementType)
    announcement = graphene.Field(AnnouncementType, id=graphene.Int(required=True))

    def resolve_announcements(self, info):
        return Announcement.objects.all()

    def resolve_announcement(self, info, id):
        return Announcement.objects.get(id=id)


class Query(
    TruckQuery,
    EventQuery,
    UserQuery,
    CateringQuery,
    AnnouncementQuery,
    graphene.ObjectType
):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
