import Editor from "@monaco-editor/react";

function EditorPanel({ code, setCode, language }) {

    return (

        <div className="left-panel">

            <h2>💻 Code Playground</h2>

            <Editor
                height="500px"
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

        </div>

    );

}

export default EditorPanel;