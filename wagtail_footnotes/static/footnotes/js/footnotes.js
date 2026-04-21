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

    // Keep a reference to the bound handler so we can remove it selectively.
    // When the user clicks "Create new footnote" we detach this before hiding the
    // modal — otherwise the hide event would fire onClose(), which cancels the
    // Draftail operation before we've had a chance to call onComplete().
    const modalCloseHandler = this.onClose;
    $(document.body).on("hidden.bs.modal", modalCloseHandler);

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
          // Detach the modal-close handler BEFORE hiding the modal. If we don't,
          // Bootstrap fires "hidden.bs.modal" which calls onClose(), and that
          // cancels the Draftail operation before onComplete() has been called.
          $(document.body).off("hidden.bs.modal", modalCloseHandler);
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

          const formsContainer = document.querySelector("#id_footnotes-FORMS");
          if (!formsContainer) return;

          // Snapshot which UUID display divs already exist so we can identify the
          // newly added one. setUUID() populates these divs; a new one with content
          // means a new footnote row has been initialised and is ready to reference.
          const existingDisplayDivIds = new Set(
            Array.from(
              document.querySelectorAll("div[id*='-uuid_display-value']")
            ).map((el) => el.id)
          );

          // Watch the entire forms container (subtree) for any DOM changes.
          // We need subtree:true because the new panel row may be nested inside
          // a wrapper element rather than being a direct child of formsContainer.
          const observer = new MutationObserver(function (mutations, obs) {
            // After each batch of mutations, check whether a new display div has
            // appeared AND been populated by setUUID(). Both conditions must be
            // true — the div is added empty first, then populated on the next tick
            // by the Stimulus read-only-uuid controller.
            const allDisplayDivs = document.querySelectorAll(
              "div[id*='-uuid_display-value']"
            );
            for (const div of allDisplayDivs) {
              if (existingDisplayDivIds.has(div.id)) continue; // pre-existing
              if (!div.textContent.trim()) continue; // not yet populated

              // Found a new, populated display div. Derive the hidden input's ID
              // by stripping "_display-value" from the div's id, then read the UUID.
              const inputId = div.id.replace("_display-value", "");
              const uuidInput = document.getElementById(inputId);
              if (!uuidInput || !uuidInput.value) continue;

              // Stop observing — we have what we need
              obs.disconnect();
              insertFootnoteEntity(uuidInput.value);
              return;
            }
          });

          observer.observe(formsContainer, {
            childList: true,
            subtree: true,
          });
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
