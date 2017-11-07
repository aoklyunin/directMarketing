from consumer.localCode import getViewCnt, leaveCampany, getRepostedCompanies
from consumer.models import ConsumerMarketCamp, Consumer
from django.core.management import BaseCommand

from mainApp.localCode import checkBotUser, getImages, getFriendsUsers, getFollowersUsers


# Алиса 32897432
# Я 303154598
# мама 2600557
# бот 453386628
# Игорь 32381970
# Михан 34499244


class Command(BaseCommand):
    def processUserFriends(self):
        id_lst = []
        for c in Consumer.objecst.all():
            id_lst.append(c.vk_id)
        for c in Consumer.objecst.all():
            if c.vkProcessState == Consumer.VK_STATE_NOT_PROCESSED:
                c.vkProcessState = Consumer.VK_STATE_PROCESSED_NOW
                c.save()
                foCnt = getFriendsUsers(c.vk_id, c.vk_token, id_lst)
                frCnt = getFollowersUsers(c.vk_id, c.vk_token, id_lst)
                c.vkCnt = frCnt + foCnt
                c.vkProcessState = Consumer.VK_STATE_PROCESSED
                c.save()

    def handle(self, *args, **options):
        # checkBotUser(2600557, Consumer.objects.first().vk_token)
        self.processUserFriends()
        # for u in Consumer.objects.all():
        #    print(checkBotUser(u))
