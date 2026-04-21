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

    // Keep a named reference so we can remove this specific handler when needed.
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
        //
        // Strategy: generate the UUID up front and insert the entity immediately
        // (while FootnoteSource is definitely still mounted), then asynchronously
        // wire up the new inline panel form row to use that same UUID.
        //
        // We can't do it the other way round (wait for the form row, read its UUID,
        // then insert the entity) because Draftail may unmount FootnoteSource at any
        // point after the modal closes, making onComplete() unreliable to call later.
        $("#footnotes-create-new").on("click", function () {
          // Generate the UUID now so we control it from the start
          const uuid = uuidv4();

          // Read the current total form count BEFORE clicking add — the new form
          // row will be assigned this index by Django's formset machinery.
          const totalFormsInput = document.getElementById(
            "id_footnotes-TOTAL_FORMS"
          );
          const newFormIndex = totalFormsInput
            ? parseInt(totalFormsInput.value, 10)
            : 0;

          // Insert the entity into the rich text editor right now, while
          // FootnoteSource is still mounted and onComplete() is safe to call.
          insertFootnoteEntity(uuid);

          // Remove the modal close handler before hiding so it doesn't fire
          // onClose() on the (now unmounting) component and cause a double-call.
          $(document.body).off("hidden.bs.modal", modalCloseHandler);
          $("#footnotes-modal").modal("hide");

          // Click the inline panel "Add" button to create a new form row.
          // Standard Wagtail inline panel selector.
          const addButton = document.querySelector("#id_footnotes-ADD");
          if (!addButton) return;
          addButton.click();

          // Scroll the footnotes panel into view so the user can fill in the text.
          // The section ID follows Wagtail's InlinePanel naming convention.
          const footnotesSection = document.querySelector(
            "#panel-child-content-footnotes-section"
          );
          if (footnotesSection) {
            footnotesSection.scrollIntoView({ behavior: "smooth" });
          }

          // Watch for the new form row's UUID input to appear in the DOM, then
          // set it to our pre-generated UUID. We know the exact ID because Django
          // formsets use a predictable index (the old TOTAL_FORMS value).
          //
          // We observe document.body (not just the forms container) to avoid
          // missing the element if Wagtail nests the new row inside wrapper elements.
          const expectedInputId = `id_footnotes-${newFormIndex}-uuid`;
          const expectedDisplayId = `${expectedInputId}_display-value`;

          const observer = new MutationObserver(function (mutations, obs) {
            const uuidInput = document.getElementById(expectedInputId);
            if (!uuidInput) return; // row not in DOM yet — keep watching

            // Found the input — stop observing immediately
            obs.disconnect();

            // Set our UUID on the hidden input. If setUUID() hasn't run yet,
            // it will see a non-empty value and skip generating its own UUID.
            // If setUUID() already ran (and generated a different UUID), we
            // overwrite it so the form row matches the entity we already inserted.
            uuidInput.value = uuid;

            // Also update the display div so what the user sees matches
            const displayDiv = document.getElementById(expectedDisplayId);
            if (displayDiv) {
              displayDiv.textContent = uuid.substring(0, 6);
            }
          });

          observer.observe(document.body, { childList: true, subtree: true });
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
