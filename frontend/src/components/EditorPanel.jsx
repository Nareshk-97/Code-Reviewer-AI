import "../styles/Editor.css";

function EditorPanel() {
  return (
    <section className="editor-panel">

      <div className="panel-header">
        <h3>Code Playground</h3>
      </div>

      <div className="editor-placeholder">
        Monaco Editor will be added here.
      </div>

    </section>
  );
}

export default EditorPanel;