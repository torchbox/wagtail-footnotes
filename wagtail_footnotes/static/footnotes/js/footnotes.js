function setUUID(id) {
  const input = document.getElementById(id);
  const displayValue = document.getElementById(`${id}_display-value`);
  if (input && !input.value) {
    const uuid = crypto.randomUUID();
    input.value = uuid;
    if (displayValue) {
      displayValue.textContent = uuid.substring(0, 6);
    }
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
          const shortKey = uuid.substring(0, 6);
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
              displayDiv.textContent = uuid.substring(0, 6);
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
          const row = $("<tr>").attr("data-uuid", uuid).css({ cursor: "pointer" });
          row.append($("<td>").text(text), $("<td>").text(uuid.substring(0, 6)));
          table.append(row);

          row.on("click", function () {
            // Use the row reference from closure rather than navigating from
            // event.target, which varies depending on which child was clicked.
            insertFootnoteEntity(row[0].dataset.uuid);
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

// --- Feature 2: click [fn] in editor → scroll to footnote panel item ---
//
// The Footnote decorator renders each in-text reference as a <sup>. We attach
// a data-footnote-uuid attribute so that panel-side code (Feature 3) can find
// these elements by UUID, and an onClick handler that scrolls to the matching
// footnote panel item when the user clicks the reference in the editor.
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
      // Use Wagtail's link colour token so the reference looks like a link in
      // the editor, consistent with the admin theme.
      style: { cursor: "pointer", color: "var(--w-color-text-link-default)", textDecoration: "underline" },
      title: "Go to footnote",
    },
    props.children
  );
};

// --- Feature 3: "Go to reference" links inside each footnote panel item ---
//
// When the edit page loads, each existing inline panel row gets a small set of
// links that scroll back to the in-text occurrence(s) of that footnote. Because
// new rows can be added dynamically (via the "Create new footnote" button), we
// use a MutationObserver to watch for new panels and inject links into them too.
//
// We wait for DOMContentLoaded to ensure the inline panel has rendered.
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

    // Find all in-text <sup> elements for this footnote.
    // These are rendered by the Footnote decorator above with data-footnote-uuid.
    const refs = document.querySelectorAll(`sup[data-footnote-uuid="${uuid}"]`);
    if (!refs.length) return;

    const container = document.createElement("div");
    container.className = "footnote-back-links";
    container.style.cssText = "margin-top: 4px; font-size: 0.85em;";

    if (refs.length === 1) {
      // Single reference — one plain "↑" link
      const link = document.createElement("a");
      link.href = "#";
      link.textContent = "↑ Go to reference";
      link.style.cssText = "cursor: pointer;";
      link.addEventListener("click", function (e) {
        e.preventDefault();
        refs[0].scrollIntoView({ behavior: "smooth", block: "center" });
      });
      container.appendChild(link);
    } else {
      // Multiple references — "↑ " label followed by numbered links "1 2 3 …"
      const label = document.createTextNode("↑ Go to reference: ");
      container.appendChild(label);

      refs.forEach(function (ref, i) {
        const link = document.createElement("a");
        link.href = "#";
        link.textContent = String(i + 1);
        link.style.cssText = "cursor: pointer; margin-right: 4px;";
        // Capture ref in loop-local variable to avoid closure issues
        const targetRef = ref;
        link.addEventListener("click", function (e) {
          e.preventDefault();
          targetRef.scrollIntoView({ behavior: "smooth", block: "center" });
        });
        container.appendChild(link);
      });
    }

    // Append below the panel's content area so it doesn't disrupt existing layout
    panel.appendChild(container);
  }

  // Inject into all panels already in the DOM on page load.
  // Deferred so Draftail has time to render <sup data-footnote-uuid> elements
  // into the main body editor — those elements exist in the document but outside
  // panelsContainer, so they won't be caught by the observer below.
  setTimeout(function () {
    panelsContainer.querySelectorAll(".w-panel").forEach(injectBackLinks);
  }, 500);

  // Watch for new panels added dynamically (e.g. via "Create new footnote")
  // and inject back-links as soon as each one appears.
  //
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
