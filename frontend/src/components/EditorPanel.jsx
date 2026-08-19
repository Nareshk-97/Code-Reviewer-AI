import Editor from "@monaco-editor/react";

function EditorPanel({ code, setCode, language }) {

    const lineCount = code
        ? code.split("\n").length
        : 0;

    const characterCount = code.length;

    const wordCount = code.trim()
        ? code.trim().split(/\s+/).length
        : 0;

    const getFileName = () => {

        switch (language) {

            case "python":
                return "main.py";

            case "javascript":
                return "main.js";

            case "java":
                return "Main.java";

            case "cpp":
                return "main.cpp";

            case "c":
                return "main.c";

            case "html":
                return "index.html";

            case "css":
                return "style.css";

            default:
                return "main.txt";
        }
    };


    return (

        <div className="left-panel editor-panel">

            {/* =========================
                Editor Header
            ========================= */}

            <div className="panel-header">

                <div>

                    <h3>
                        💻 Code Playground
                    </h3>

                    <span className="editor-file">
                        &lt;/&gt; {getFileName()}
                    </span>

                </div>


                <div className="editor-status">

                    <span className="editor-status-dot"></span>

                    Editor Ready

                </div>

            </div>


            {/* =========================
                Monaco Editor
            ========================= */}

            <div className="editor-container">

                <Editor

                    height="420px"

                    language={language}

                    theme="vs-dark"

                    value={code}

                    onChange={(value) =>
                        setCode(value || "")
                    }

                    options={{

                        minimap: {
                            enabled: false
                        },

                        fontSize: 15,

                        automaticLayout: true,

                        scrollBeyondLastLine: false,

                        wordWrap: "on",

                        smoothScrolling: true,

                        cursorSmoothCaretAnimation: "on",

                        renderWhitespace: "selection",

                        tabSize: 4,

                        padding: {
                            top: 12,
                            bottom: 12
                        }

                    }}

                />

            </div>


            {/* =========================
                Code Statistics
            ========================= */}

            <div className="code-stats">


                <div className="stat-card">

                    <span className="stat-label">
                        📄 Lines
                    </span>

                    <span className="stat-value">
                        {lineCount}
                    </span>

                </div>


                <div className="stat-card">

                    <span className="stat-label">
                        🔤 Characters
                    </span>

                    <span className="stat-value">
                        {characterCount}
                    </span>

                </div>


                <div className="stat-card">

                    <span className="stat-label">
                        📝 Words
                    </span>

                    <span className="stat-value">
                        {wordCount}
                    </span>

                </div>


                <div className="stat-card">

                    <span className="stat-label">
                        💻 Language
                    </span>

                    <span className="stat-value language-value">
                        {language.toUpperCase()}
                    </span>

                </div>


            </div>


            {/* =========================
                Editor Footer
            ========================= */}

            <div className="editor-footer">


                <div className="editor-footer-left">

                    <span className="editor-footer-item">
                        ● Ready
                    </span>

                    <span className="editor-footer-item">
                        Auto Layout
                    </span>

                </div>


                <div className="editor-footer-right">

                    <span className="editor-language">
                        {language.toUpperCase()}
                    </span>

                </div>


            </div>


        </div>

    );
}

export default EditorPanel;