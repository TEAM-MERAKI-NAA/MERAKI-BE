from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from ..models.news import News
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed


class CustomFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement("image", item["image"])


class LatestPostsFeed(Feed):
    title = "My blog"
    link = ""
    description = "New posts of my blog."

    def items(self):
        print('kjkj')
        return News.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.long_description, 30)

    def item_link(self, item):
        return 'http://localhost:4200/article/details/'+item.slug

    # def item_extra_kwargs(self, item):
    #     img_url = item.image.url
    #     request_url = self.request.build_absolute_uri('/')[:-1]
    #     image_url_abs = f"{request_url}{img_url}"
    #     return {
    #         'image': image_url_abs
    #     }
