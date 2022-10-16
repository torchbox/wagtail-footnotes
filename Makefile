# django tests
test:
	python testmanage.py test

# convienient tox testing shortcuts
215:
	tox -e python3.9-django3.0-wagtail2.15
216:
	tox -e python3.9-django3.2-wagtail2.16
30:
	tox -e python3.10-django4.0-wagtail3.0
40:
	tox -e python3.10-django4.1-wagtail4.0

# development commands
run: 
	python testmanage.py runserver 0.0.0.0:8000

install:
	@pip install ".[testing]" --force

setup:
	@python testmanage.py migrate
	@python testmanage.py loaddata wagtail_footnotes/test/fixtures/core.json
	@python testmanage.py loaddata wagtail_footnotes/test/fixtures/users.json
	@python testmanage.py loaddata wagtail_footnotes/test/fixtures/page.json
	@python testmanage.py loaddata wagtail_footnotes/test/fixtures/footnotes.json
	@make run

fixtures:
	@echo "Creating fixtures"
	@python testmanage.py dumpdata \
	wagtail_footnotes_test.TestPageStreamField --indent 2 > wagtail_footnotes/test/fixtures/page.json
	@python testmanage.py dumpdata \
	wagtailcore.Page --indent 2 > wagtail_footnotes/test/fixtures/core.json
	@python testmanage.py dumpdata \
	wagtail_footnotes --indent 2 > wagtail_footnotes/test/fixtures/footnotes.json
	@python testmanage.py dumpdata \
	auth.user --indent 2 > wagtail_footnotes/test/fixtures/users.json
