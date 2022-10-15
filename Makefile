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

setup:
	@pip install ".[testing]" --force
	@python testmanage.py migrate
	@echo "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('admin', '', 'password')" | python testmanage.py shell
	@python testmanage.py loaddata wagtail_footnotes/test/fixtures/initial_data.json
	@make run

fixtures:
	@./fixtures.sh
