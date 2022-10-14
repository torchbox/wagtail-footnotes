# Generated by Django 4.1.2 on 2022-10-14 21:06

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields
import wagtail_footnotes.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0077_alter_revision_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestPageStreamField",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "paragraph",
                                wagtail_footnotes.blocks.RichTextBlockWithFootnotes(
                                    features=["footnotes"]
                                ),
                            )
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
