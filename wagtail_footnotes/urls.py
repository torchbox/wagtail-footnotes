from django.urls import path
from django.views.generic import TemplateView
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (4, 0):
    template_name = "wagtail_footnotes/admin/footnotes_modal.html"
else:
    template_name = "wagtail_footnotes/admin/footnotes_modal_legacy.html"

urlpatterns = [
    path(
        "footnotes_modal/",
        TemplateView.as_view(template_name=template_name),
        name="footnotes-modal",
    )
]
