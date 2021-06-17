from django.urls import include, path

from wagtail.core import urls as wagtail_urls

from wagtail_footnotes import urls as footnotes_urls

urlpatterns = [
    path("", include(wagtail_urls)),
    path("footnotes/", include(footnotes_urls)),
]
