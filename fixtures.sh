FILE="wagtail_footnotes/test/fixtures/initial_data.json"

if [ ! -f $FILE ]; then
	echo "Creating fixtures"
    python testmanage.py dumpdata \
    --natural-foreign \
    --indent 2 \
    -e contenttypes -e auth.permission \
    -e wagtailcore.groupcollectionpermission \
    -e wagtailcore.grouppagepermission \
    -e wagtailimages.rendition \
    -e wagtailsearch.sqliteftsindexentry -e wagtailsearch.indexentry \
    -e sessions \
    > wagtail_footnotes/test/fixtures/initial_data.json
else
    echo "Fixtures already exist, you'll need to delete them to regenerate"
fi
