from adminPanel.models import BlackList
from consumer.localCode import getViewCnt, leaveCampany, getRepostedCompanies, getNotRepostedCompanies
from consumer.models import ConsumerMarketCamp, Consumer
from django.core.management import BaseCommand

from customer.models import MarketCamp
from mainApp.localCode import checkBotUser, getImages, getFriendsUsers, getFollowersUsers, getUserCreatedDate


# Алиса 32897432
# Я 303154598
# мама 2600557
# бот 453386628
# Игорь 32381970
# Михан 34499244


class Command(BaseCommand):
    def processUserFriends(self):
        id_lst = []
        for c in Consumer.objects.all():
            id_lst.append(c.vk_id)
        for c in Consumer.objects.all():
            if c.vkProcessState == Consumer.VK_STATE_NOT_PROCESSED:
                c.vkProcessState = Consumer.VK_STATE_PROCESSED_NOW
                c.save()
                foCnt = getFollowersUsers(c.vk_id, c.vk_token, id_lst)
                print(foCnt)
                frCnt = getFriendsUsers(c.vk_id, c.vk_token, id_lst)
                print(frCnt)
                frCnt = 0
                c.vkCnt = frCnt + foCnt
                c.vkProcessState = Consumer.VK_STATE_PROCESSED
                c.save()

    def handle(self, *args, **options):
        self.processUserFriends()
