class CustomEditorController extends window.StimulusModule.Controller {
    connect() {
        setUUID(this.element.id);
    }
}

window.wagtail.app.register('read-only-uuid', CustomEditorController);
