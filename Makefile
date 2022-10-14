test-216:
	tox -e python3.9-django3.2-wagtail2.16

test-300:
	tox -e python3.9-django3.2-wagtail3.0

test-400:
	tox -e python3.9-django3.2-wagtail4.0

test-specific:
	python testmanage.py test wagtail_footnotes.test.tests.test_factories.TestPageFactory.test_factory

run: 
	python testmanage.py runserver 0.0.0.0:8000
