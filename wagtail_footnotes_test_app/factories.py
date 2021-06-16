import factory
import wagtail_factories
from faker import Factory as FakerFactory

from .models import TestPage


class TestPage(wagtail_factories.PageFactory):
    class Meta:
        model = TestPage

    title = factory.Faker("text", max_nb_chars=25)
