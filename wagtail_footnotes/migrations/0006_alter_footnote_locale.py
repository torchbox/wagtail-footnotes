# Generated by Django 4.2.14 on 2024-08-12 17:41
import django.db.models.deletion

from django.db import migrations, models
from wagtail import VERSION as WAGTAIL_VERSION


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        (
            "wagtail_footnotes",
            "0005_alter_footnote_locale_alter_footnote_translation_key",
        ),
    ]

    operations = []

    if WAGTAIL_VERSION >= (6, 2):
        operations.append(
            migrations.AlterField(
                model_name="footnote",
                name="locale",
                field=models.ForeignKey(
                    editable=False,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="+",
                    to="wagtailcore.locale",
                    verbose_name="locale",
                ),
            )
        )
