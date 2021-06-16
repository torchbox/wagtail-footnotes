from django.urls import include, path

from wagtail_footnotes import urls as footnotes_urls

urlpatterns = [
    path("footnotes/", include(footnotes_urls)),
]
