from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path(
        "footnotes_modal/",
        TemplateView.as_view(
            template_name="wagtail_footnotes/admin/footnotes_modal.html"
        ),
        name="footnotes-modal",
    )
]
