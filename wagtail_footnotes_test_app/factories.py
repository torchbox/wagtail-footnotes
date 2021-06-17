import factory
import wagtail_factories
import uuid


from . import models
from . import blocks
from wagtail_footnotes import blocks as wf_blocks
from wagtail_footnotes import models as wf_models


class RichTextBlockWithFootnotes(wagtail_factories.blocks.BlockFactory):
    class Meta:
        model = wf_blocks.RichTextBlockWithFootnotes


class CustomBlock(wagtail_factories.StructBlockFactory):
    paragraph = factory.SubFactory(RichTextBlockWithFootnotes)

    class Meta:
        model = blocks.CustomBlock


class TestPage(wagtail_factories.PageFactory):
    class Meta:
        model = models.TestPage

    title = factory.Faker("text", max_nb_chars=25)
    body = wagtail_factories.StreamFieldFactory(
        # TODO: I really want to use CustomBlock here so I don't have to redefine the structure.
        {"paragraph": RichTextBlockWithFootnotes}
    )


class Footnote(factory.django.DjangoModelFactory):
    class Meta:
        model = wf_models.Footnote

    page = factory.SubFactory(wagtail_factories.PageFactory)
    uuid = factory.LazyFunction(uuid.uuid4)
    text = factory.Sequence(lambda n: f"Footnote {n}")
