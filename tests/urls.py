from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from wagtail_footnotes import urls as footnotes_urls


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]

urlpatterns += i18n_patterns(
    path("footnotes/", include(footnotes_urls)),
    path("", include(wagtail_urls)),
    prefix_default_language=False,
)
