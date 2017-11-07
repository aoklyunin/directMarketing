from consumer.localCode import getViewCnt, leaveCampany, getRepostedCompanies
from consumer.models import ConsumerMarketCamp, Consumer
from django.core.management import BaseCommand

from mainApp.localCode import checkBotUser, getImages, getFriendsUsers, getFollowersUsers, getUserCreatedDate


class Command(BaseCommand):
    def handle(self, *args, **options):
        for c in Consumer.objects.all():
            getUserCreatedDate(c.vk_id)