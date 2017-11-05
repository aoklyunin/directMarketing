from consumer.localCode import getViewCnt, leaveCampany, getRepostedCompanies
from consumer.models import ConsumerMarketCamp, Consumer
from django.core.management import BaseCommand

class process(BaseCommand):
    for c in ConsumerMarketCamp.objects.all():
        try:
            id = c.consumer.vk_id
            post_id = c.postId
            cnt = getViewCnt(id, post_id, c.consumer.vk_token)
            c.viewCnt = cnt
            c.save()
        except:
            print("Запись удалена")

    for u in Consumer.objects.all():
        reposted_cms = getRepostedCompanies(u.vk_id, u.vk_token)

        for r in reposted_cms:
            m = r["m"]
            if m.isActive:
                try:
                    cm = ConsumerMarketCamp.objects.get(marketCamp=m, consumer=u)
                    print("Есть репост, есть компания")
                except:
                    cm = ConsumerMarketCamp.objects.create(marketCamp=m, consumer=u, joinType=1, postId=r["id"],
                                                           link="https://vk.com/wall" + str(u.vk_id) + "_" + str(
                                                               r["id"]))

                    id = cm.consumer.vk_id
                    post_id = cm.postId
                    cnt = getViewCnt(id, post_id, cm.consumer.vk_token)
                    cm.viewCnt = cnt
                    cm.save()

                    print("Есть репост, нет компании")
            else:
                try:
                    cm = ConsumerMarketCamp.objects.get(marketCamp=m, consumer=u, joinType=1)
                    leaveCampany(cm)
                    print("Есть репост, есть неактивная компания ")
                except:
                    pass
