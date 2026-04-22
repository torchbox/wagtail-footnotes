// Number of UUID characters shown in the editor and chooser table.
// Also used by the display-value div rendered by ReadonlyUUIDInput.
const UUID_SHORT_LENGTH = 6;

function setUUID(id) {
  const input = document.getElementById(id);
  if (!input || input.value) return;
  const uuid = crypto.randomUUID();
  input.value = uuid;
  const displayValue = document.getElementById(`${id}_display-value`);
  if (displayValue) {
    displayValue.textContent = uuid.substring(0, UUID_SHORT_LENGTH);
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
        const table = $("#footnotes-listing tbody");
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
          const shortKey = uuid.substring(0, UUID_SHORT_LENGTH);
          const newContent = Modifier.replaceText(
            content,
            selection,
            `[${shortKey}]`,
            null,
            entityKey
          );
          onComplete(EditorState.push(editorState, newContent, "insert-characters"));
        }

        // --- "Create new footnote" button handler ---
        //
        // Strategy: generate the UUID up front and insert the entity immediately
        // (while FootnoteSource is definitely still mounted), then asynchronously
        // wire up the new inline panel form row to use that same UUID.
        //
        // We can't do it the other way round (wait for the form row, read its UUID,
        // then insert the entity) because Draftail unmounts FootnoteSource after
        // onComplete() is called, making it unsafe to call later.
        $("#footnotes-create-new").on("click", function () {
          const uuid = crypto.randomUUID();

          // Read the current total form count BEFORE clicking add — the new form
          // row will be assigned this index by Django's formset machinery.
          const totalFormsInput = document.getElementById("id_footnotes-TOTAL_FORMS");
          if (!totalFormsInput) return;
          const newFormIndex = parseInt(totalFormsInput.value, 10);

          // Insert the entity while FootnoteSource is still mounted and
          // onComplete() is safe to call.
          insertFootnoteEntity(uuid);

          // Remove the modal close handler before hiding so it doesn't fire
          // onClose() on the now-unmounting component.
          $(document.body).off("hidden.bs.modal", modalCloseHandler);
          $("#footnotes-modal").modal("hide");

          // Click the inline panel "Add" button to create a new form row.
          // Standard Wagtail inline panel selector.
          const addButton = document.querySelector("#id_footnotes-ADD");
          if (!addButton) return;
          addButton.click();

          // Watch for the new form row's UUID input to appear in the DOM, then
          // stamp it with our pre-generated UUID. We know the exact input ID because
          // Django formsets use a predictable index (the pre-add TOTAL_FORMS value).
          //
          // We observe document.body to avoid missing the element if Wagtail
          // nests the new row inside wrapper elements.
          const expectedInputId = `id_footnotes-${newFormIndex}-uuid`;
          const expectedDisplayId = `${expectedInputId}_display-value`;

          const observer = new MutationObserver(function (mutations, obs) {
            const uuidInput = document.getElementById(expectedInputId);
            if (!uuidInput) return; // row not in DOM yet — keep watching

            obs.disconnect();

            // Stamp our UUID onto the hidden input. If setUUID() hasn't run yet it
            // will skip (input is non-empty). If it already ran with a different UUID
            // we overwrite it so the form row matches the entity we inserted.
            uuidInput.value = uuid;

            const displayDiv = document.getElementById(expectedDisplayId);
            if (displayDiv) {
              displayDiv.textContent = uuid.substring(0, UUID_SHORT_LENGTH);
            }

            // Scroll to the new row and focus its Draftail editor. Deferred because
            // onComplete() causes Draftail to refocus the rich text editor — we run
            // after that so our scroll and focus take effect last.
            const newRow = uuidInput.closest(".w-panel");
            if (!newRow) return;

            setTimeout(function () {
              newRow.scrollIntoView({ behavior: "smooth", block: "center" });

              // The Draftail editor in the new row may not be initialised yet.
              // Try immediately, and if not ready, observe until it appears.
              const existingEditor = newRow.querySelector(".public-DraftEditor-content");
              if (existingEditor) {
                existingEditor.focus();
                return;
              }

              const editorObserver = new MutationObserver(function (_, editorObs) {
                const editor = newRow.querySelector(".public-DraftEditor-content");
                if (!editor) return;
                editorObs.disconnect();
                clearTimeout(editorObserverTimeout);
                editor.focus();
              });
              editorObserver.observe(newRow, { childList: true, subtree: true });

              // Disconnect after 5s as a leak guard in case the editor never appears
              const editorObserverTimeout = setTimeout(
                () => editorObserver.disconnect(),
                5000
              );
            }, 100);
          });

          observer.observe(document.body, { childList: true, subtree: true });
        });

        // --- Existing footnote rows: build the chooser table ---
        // Reads footnote content and UUIDs from the live inline panel forms
        // and populates the modal table so the user can pick an existing footnote.
        document.querySelectorAll("#id_footnotes-FORMS .w-panel").forEach(function (panel) {
          const text = $(".public-DraftEditor-content", panel).text();
          const uuid = $('input[id*="-uuid"]', panel)[0].value;

          // Build the row using DOM methods rather than HTML string concatenation
          // to avoid injection issues with footnote text content.
          const row = $("<tr>").data("uuid", uuid);
          row.append($("<td>").text(text), $("<td>").text(uuid.substring(0, UUID_SHORT_LENGTH)));
          table.append(row);
        });

        // Use event delegation rather than per-row listeners — one handler on the
        // table catches clicks from any row.
        table.on("click", "tr", function () {
          const uuid = $(this).data("uuid");
          if (uuid) {
            insertFootnoteEntity(uuid);
            $("#footnotes-modal").modal("hide");
          }
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

// Renders each in-text footnote reference as a clickable <sup>. Clicking scrolls
// to the matching footnote panel row. data-footnote-uuid is set so the panel-side
// back-links can locate this element by UUID.
const Footnote = (props) => {
  const { entityKey, contentState } = props;
  const data = contentState.getEntity(entityKey).getData();
  const uuid = data.footnote;

  function handleClick(e) {
    e.preventDefault();

    // Find the hidden UUID input inside the footnote's inline panel row.
    // The selector matches any input whose id contains "-uuid" and whose value
    // is the exact UUID for this reference.
    const uuidInput = document.querySelector(`input[id*="-uuid"][value="${uuid}"]`);
    if (!uuidInput) return;

    // Walk up to the nearest .w-panel ancestor — that is the inline panel row
    // for this footnote.
    const panel = uuidInput.closest(".w-panel");
    if (!panel) return;

    panel.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  return React.createElement(
    "sup",
    {
      "data-footnote-uuid": uuid,
      onClick: handleClick,
      className: "footnote-ref-sup",
      title: "Go to footnote",
    },
    props.children
  );
};

// Injects "↑ Go to reference" back-links into each footnote inline panel row,
// positioned just below the short ID. Each link scrolls to the corresponding
// in-text <sup> in the editor. A MutationObserver handles rows added dynamically.
document.addEventListener("DOMContentLoaded", function () {
  const panelsContainer = document.getElementById("id_footnotes-FORMS");
  if (!panelsContainer) return; // not on an edit page

  // Injects "↑ Go to reference" (or numbered links for multiple refs) into a
  // footnote panel row. Safe to call multiple times — bails if links already
  // injected for this panel.
  function injectBackLinks(panel) {
    if (panel.querySelector(".footnote-back-links")) return;

    const uuidInput = panel.querySelector('input[id*="-uuid"]');
    if (!uuidInput || !uuidInput.value) return;

    const uuid = uuidInput.value;

    // Find all in-text <sup data-footnote-uuid> elements for this footnote.
    const refs = document.querySelectorAll(`sup[data-footnote-uuid="${uuid}"]`);
    if (!refs.length) return;

    const container = document.createElement("div");
    container.className = "footnote-back-links";

    if (refs.length === 1) {
      // Single reference — one plain button
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "footnote-back-link";
      btn.textContent = "↑ Go to reference";
      btn.addEventListener("click", function () {
        refs[0].scrollIntoView({ behavior: "smooth", block: "center" });
      });
      container.appendChild(btn);
    } else {
      // Multiple references — "↑ " label followed by numbered buttons "1 2 3 …"
      container.appendChild(document.createTextNode("↑ Go to reference: "));

      refs.forEach(function (ref, i) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "footnote-back-link";
        btn.textContent = i + 1;
        btn.addEventListener("click", function () {
          ref.scrollIntoView({ behavior: "smooth", block: "center" });
        });
        container.appendChild(btn);
      });
    }

    // Insert immediately after the UUID display div so the back-link sits just
    // below the footnote's ID — the most natural place to see "where is this used".
    // Falls back to appending to the panel if the display div isn't found.
    const displayDiv = document.getElementById(`${uuidInput.id}_display-value`);
    if (displayDiv) {
      displayDiv.insertAdjacentElement("afterend", container);
    } else {
      panel.appendChild(container);
    }
  }

  // Initial pass — Stimulus initialises Draftail synchronously before this
  // handler runs, so sups may already be in the DOM at this point.
  panelsContainer.querySelectorAll(".w-panel").forEach(injectBackLinks);

  // Watch for Draftail to render footnote entities in the main body editor.
  // <sup data-footnote-uuid> elements live outside panelsContainer so won't be
  // caught by the panel observer below — we watch document.body instead and
  // filter to only act when a relevant element appears.
  const supObserver = new MutationObserver(function (mutations) {
    const hasNewSup = mutations.some(function (m) {
      return Array.from(m.addedNodes).some(function (n) {
        return (
          n.nodeType === Node.ELEMENT_NODE &&
          ((n.tagName === "SUP" && n.hasAttribute("data-footnote-uuid")) ||
            n.querySelector("sup[data-footnote-uuid]") !== null)
        );
      });
    });

    if (!hasNewSup) return;

    panelsContainer.querySelectorAll(".w-panel").forEach(injectBackLinks);
  });

  supObserver.observe(document.body, { childList: true, subtree: true });

  // Watch for new panels added dynamically (e.g. via "Create new footnote").
  // childList-only (no subtree) so this doesn't fire on every keystroke inside
  // the footnote text editors — we only care about panel rows being added/removed.
  const panelObserver = new MutationObserver(function () {
    panelsContainer.querySelectorAll(".w-panel").forEach(injectBackLinks);
  });

  panelObserver.observe(panelsContainer, { childList: true });
});

window.draftail.registerPlugin({
  type: "FOOTNOTES",
  source: FootnoteSource,
  decorator: Footnote,
});
