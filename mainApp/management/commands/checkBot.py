from consumer.localCode import getViewCnt, leaveCampany, getRepostedCompanies
from consumer.models import ConsumerMarketCamp, Consumer
from django.core.management import BaseCommand

from mainApp.localCode import checkBotUser, getImages


class Command(BaseCommand):
    def handle(self, *args, **options):
        checkBotUser(453386628, Consumer.objects.first().vk_token)
        #for u in Consumer.objects.all():
        #    print(checkBotUser(u))
