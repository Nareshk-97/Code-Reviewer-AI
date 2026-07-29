import Editor from "@monaco-editor/react";

function EditorPanel({ code, setCode, language }) {

    return (

        <div className="left-panel">

            <h2>💻 Code Playground</h2>

            <Editor
                height="400px"
                language={language}
                theme="vs-dark"
                value={code}
                onChange={(value) => setCode(value || "")}
                options={{
                    minimap: {
                        enabled: false
                    },
                    fontSize: 15,
                    automaticLayout: true,
                    scrollBeyondLastLine: false,
                    wordWrap: "on"
                }}
            />

            {/* Code Statistics */}

            <div className="code-stats">

                <div className="stat-card">
                    <span className="stat-label">📄 Lines</span>
                    <span className="stat-value">
                        {code ? code.split("\n").length : 0}
                    </span>
                </div>

                <div className="stat-card">
                    <span className="stat-label">🔤 Characters</span>
                    <span className="stat-value">
                        {code.length}
                    </span>
                </div>

                <div className="stat-card">
                    <span className="stat-label">📝 Words</span>
                    <span className="stat-value">
                        {code.trim() ? code.trim().split(/\s+/).length : 0}
                    </span>
                </div>

                <div className="stat-card">
                    <span className="stat-label">💻 Language</span>
                    <span className="stat-value">
                        {language}
                    </span>
                </div>

            </div>

        </div>

    );

}

export default EditorPanel;