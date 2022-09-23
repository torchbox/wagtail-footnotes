function uuidv4() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
    (
      c ^
      (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
    ).toString(16)
  );
}

function setUUID(id) {
  var $input = $("input#" + id);
  var $displayValue = $("div#" + id + "_display-value");
  if (!$input.val()) {
    var uuid = uuidv4();
    // Set hidden field
    $input.val(uuid);
    // Set displayed text
    $displayValue.html(uuid.substring(0, 6));
  }
}

const React = window.React;
const Modifier = window.DraftJS.Modifier;
const EditorState = window.DraftJS.EditorState;

class FootnoteSource extends React.Component {
  constructor(props) {
    super(props);
    this.onClose = this.onClose.bind(this);
  }

  componentDidMount() {
    const { editorState, entityType, onComplete } = this.props;

    const content = editorState.getCurrentContent();
    const selection = editorState.getSelection();

    $(document.body).on("hidden.bs.modal", this.onClose);

    $("body > .modal").remove();

    $.ajax({
      url: "/footnotes/footnotes_modal/",
      success: function (data) {
        $("body").append(data);
        var table = $("#footnotes-listing tbody");
        table.empty();

        var live_footnotes = document.querySelectorAll(
          "#id_footnotes-FORMS .w-panel"
        );
        Array.prototype.forEach.call(live_footnotes, function (value) {
          var text = $(".public-DraftEditor-content", value).text();
          var uuid = $('input[id*="-uuid"]', value)[0].value;
          var row = $(
            "<tr data-uuid=" +
            uuid +
            "><td>" +
            text +
            "</td><td>" +
            uuid.substring(0, 6) +
            "</td></tr>"
          ).css({ cursor: "pointer" });
          table.append(row);

          row.on("click", function (event) {
            const footnoteUUID = event.target.parentElement.dataset["uuid"];

            // Uses the Draft.js API to create a new entity with the right data.
            const contentWithEntity = content.createEntity(
              entityType.type,
              "IMMUTABLE",
              {
                footnote: footnoteUUID,
              }
            );
            const entityKey = contentWithEntity.getLastCreatedEntityKey();

            // We also add some text for the entity to be activated on.
            const shortKey = footnoteUUID.substring(0, 6);
            const text = `[${shortKey}]`;

            const newContent = Modifier.replaceText(
              content,
              selection,
              text,
              null,
              entityKey
            );
            const nextState = EditorState.push(
              editorState,
              newContent,
              "insert-characters"
            );

            onComplete(nextState);

            $("#footnotes-modal").modal("hide");
          });
        });

        $("#footnotes-modal").modal("show");
      },
      dataType: "html",
    });
  }

  onClose(e) {
    const { onClose } = this.props;
    e.preventDefault();
    onClose();
  }

  render() {
    console.log("FootnoteSource", this.props);
    return null;
  }
}

const Footnote = (props) => {
  const { entityKey, contentState } = props;
  const data = contentState.getEntity(entityKey).getData();
  return React.createElement("sup", {}, props.children);
};

window.draftail.registerPlugin({
  type: "FOOTNOTES",
  source: FootnoteSource,
  decorator: Footnote,
});
