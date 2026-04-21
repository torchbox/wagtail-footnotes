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

    // Capture content and selection at the time the modal opens — these represent
    // the editor state at the point the user triggered the footnote chooser.
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

        // --- Shared helper: insert a Draft.js footnote entity at the cursor ---
        // Creates an IMMUTABLE entity for the given UUID and inserts "[shortid]"
        // as the visible text at the current selection in the rich text editor.
        function insertFootnoteEntity(uuid) {
          const contentWithEntity = content.createEntity(
            entityType.type,
            "IMMUTABLE",
            { footnote: uuid }
          );
          const entityKey = contentWithEntity.getLastCreatedEntityKey();

          // The short key is the first 6 chars of the UUID — used as visible text
          // in the editor. On the published page this is replaced by a numbered ref.
          const shortKey = uuid.substring(0, 6);
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
        }

        // --- "Create new footnote" button handler ---
        // Closes the modal, triggers the inline panel's "Add" button to create a
        // new footnote row, scrolls the footnotes section into view, then waits
        // for the new row's UUID to be populated before inserting the entity.
        $("#footnotes-create-new").on("click", function () {
          // Hide the modal before doing anything else so the user can see the panel
          $("#footnotes-modal").modal("hide");

          // The inline panel "Add" button — standard Wagtail inline panel selector
          const addButton = document.querySelector("#id_footnotes-ADD");
          if (!addButton) return;
          addButton.click();

          // Scroll the footnotes inline panel section into view.
          // The panel section ID follows Wagtail's naming convention for InlinePanel
          // fields defined inside the page's content_panels.
          const footnotesSection = document.querySelector(
            "#panel-child-content-footnotes-section"
          );
          if (footnotesSection) {
            footnotesSection.scrollIntoView({ behavior: "smooth" });
          }

          // Watch for the new inline panel row to be added to the DOM.
          // We can't use setTimeout here because the render time is unpredictable —
          // MutationObserver lets us react precisely when the new row appears.
          const formsContainer = document.querySelector("#id_footnotes-FORMS");
          if (!formsContainer) return;

          const rowObserver = new MutationObserver(function (mutations, rowObs) {
            for (const mutation of mutations) {
              for (const node of mutation.addedNodes) {
                // Only interested in element nodes (not text nodes etc.)
                if (node.nodeType !== Node.ELEMENT_NODE) continue;

                // The UUID display div is populated by setUUID() once the new row
                // is initialised. Find it within the newly added panel row.
                const displayDiv = node.querySelector('div[id$="_display-value"]');
                if (!displayDiv) continue;

                // Stop watching for new rows — we found the one we want
                rowObs.disconnect();

                // Now watch the display div for its content being set by setUUID().
                // setUUID() calls $displayValue.html(...), which triggers a childList
                // mutation. We use this as the signal that the UUID is ready.
                const uuidObserver = new MutationObserver(function (_, uuidObs) {
                  const uuidInput = node.querySelector('input[id*="-uuid"]');
                  if (!uuidInput || !uuidInput.value) return;

                  // UUID is ready — stop observing and insert the entity
                  uuidObs.disconnect();
                  insertFootnoteEntity(uuidInput.value);
                });

                uuidObserver.observe(displayDiv, { childList: true });
              }
            }
          });

          rowObserver.observe(formsContainer, { childList: true });
        });

        // --- Existing footnote rows: build the chooser table ---
        // Reads footnote content and UUIDs from the live inline panel forms
        // and populates the modal table so the user can pick an existing footnote.
        var live_footnotes = document.querySelectorAll(
          "#id_footnotes-FORMS .w-panel"
        );
        Array.prototype.forEach.call(live_footnotes, function (value) {
          const text = $(".public-DraftEditor-content", value).text();
          const uuid = $('input[id*="-uuid"]', value)[0].value;
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
            insertFootnoteEntity(footnoteUUID);
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
