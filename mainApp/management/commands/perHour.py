import datetime

from adminPanel.models import BlackList
from consumer.localCode import getViewCnt, leaveCampany, getRepostedCompanies, getNotRepostedCompanies
from consumer.models import ConsumerMarketCamp, Consumer
from django.core.management import BaseCommand

from customer.models import MarketCamp
from mainApp.localCode import checkBotUser, getImages, getFriendsUsers, getFollowersUsers, getUserCreatedDate, \
    closeMarketCamp


# Алиса 32897432
# Я 303154598
# мама 2600557
# бот 453386628
# Игорь 32381970
# Михан 34499244


class Command(BaseCommand):
    def processMarketCamp(self):
        for m in MarketCamp.objects.filter(isActive=False):
            cnt = 0
            for cm in ConsumerMarketCamp.objects.filter(marketCamp=m,stateCheated=ConsumerMarketCamp.STATE_NOT_CHEATED):
                cnt += cm.viewCnt
            m.curViewCnt = cnt
            if m.curViewCnt>=m.targetViewCnt or m.endTime < datetime.datetime.now():
                closeMarketCamp(m)



    def processConsumerMarketCamps(self):
        for c in ConsumerMarketCamp.objects.all():
            if c.marketCamp.isActive:
                try:
                    id = c.consumer.vk_id
                    post_id = c.postId
                    cnt = getViewCnt(id, post_id, c.consumer.vk_token)
                    c.viewCnt = cnt
                    if c.viewCnt > c.consumer.vkCnt and c.stateCheated == ConsumerMarketCamp.STATE_NOT_CHEATED:
                        c.stateCheated = ConsumerMarketCamp.STATE_PRETEND_CHEATED
                    c.save()
                except:
                    print("Запись удалена")

        d = {}
        for c in Consumer.objects.all():
            [rm, rids] = getRepostedCompanies(c.vk_id, c.vk_token)
            nrm = getNotRepostedCompanies(rm)
            d[c] = [rm, nrm, rids]

        for cm in ConsumerMarketCamp.objects.all():
            # среди репостнутых
            if cm.marketCamp in d[c][0]:
                if cm.joinType == ConsumerMarketCamp.TYPE_NOT_JOINED:
                    cm.joinType = ConsumerMarketCamp.TYPE_JOINED_NOW
                    cm.postId = d[c][2][d[c][0].index(cm.marketCamp)]
                    cm.save()

            # среди не репостнутых
            if cm.marketCamp in d[c][1]:
                if (cm.joinType == ConsumerMarketCamp.TYPE_JOINED_NOW):
                    leaveCampany(cm)

    def handle(self, *args, **options):
        self.processConsumerMarketCamps()
        self.processMarketCamp()
        # for u in Consumer.objects.all():
        #    print(checkBotUser(u))
