from consumer.localCode import getViewCnt, leaveCampany, getRepostedCompanies, getNotRepostedCompanies
from consumer.models import ConsumerMarketCamp, Consumer
from django.core.management import BaseCommand

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

    def processConsumerMarketCamps(self):
        for c in ConsumerMarketCamp.objects.all():
            try:
                id = c.consumer.vk_id
                post_id = c.postId
                cnt = getViewCnt(id, post_id, c.consumer.vk_token)
                c.viewCnt = cnt
                c.save()
            except:
                print("Запись удалена")


        d = {}
        for c in Consumer.objects.all():
            [rm,rids] = getRepostedCompanies(c.vk_id, c.vk_token)
            nrm = getNotRepostedCompanies(rm)
            d[c] = [rm,nrm,rids]

        for cm in ConsumerMarketCamp.objects.all():
            # среди репостнутых
            if cm.marketCamp in d[c][0]:
                if cm.joinType == ConsumerMarketCamp.TYPE_NOT_JOINED:
                    cm.joinType = ConsumerMarketCamp.TYPE_JOINED_NOW
                    cm.postId = d[c][2][d[c][0].index(cm.marketCamp)]
                    cm.save()

            # среди не репостнутых
            if cm.marketCamp in d[c][1]:
                if cm.joinType == ConsumerMarketCamp.TYPE_JOINED_NOW:
                    leaveCampany(cm)

    def handle(self, *args, **options):
        self.processConsumerMarketCamps()
        self.processUserFriends()
        # for u in Consumer.objects.all():
        #    print(checkBotUser(u))
