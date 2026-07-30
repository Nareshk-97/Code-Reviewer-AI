import { useEffect, useState, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { reviewCode } from "../services/reviewService";
import "../styles/Dashboard.css";
import EditorPanel from "../components/EditorPanel";
import Navbar from "../components/Navbar";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

function Dashboard() {

    const [user, setUser] = useState(null);
    const [code, setCode] = useState("");
    const [language, setLanguage] = useState("python");
    const [review, setReview] = useState("");
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem("reviewHistory");
    return saved ? JSON.parse(saved) : [];
    
});
const [searchHistory, setSearchHistory] = useState("");

    const fileInputRef = useRef(null);

    const navigate = useNavigate();

    useEffect(() => {

        const token = localStorage.getItem("token");

        if (!token) {
            navigate("/login");
            return;
        }

        const fetchProfile = async () => {

            try {

                const response = await axios.get(
                    "http://127.0.0.1:5000/profile",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                setUser(response.data.user);

            } catch (error) {

                console.log(error);

                localStorage.removeItem("token");
                navigate("/login");

            }

        };

        fetchProfile();

    }, [navigate]);

    // ==========================
    // AI Review Function
    // ==========================

    const handleReview = async () => {

        if (!code.trim()) {
            alert("Please enter some code.");
            return;
        }

        try {

            setLoading(true);

            const response = await reviewCode(code);

            if (response.success) {

    setReview(response.review);

    const newReview = {
        id: Date.now(),
        language,
        review: response.review,
        createdAt: new Date().toLocaleString()
    };

    const updatedHistory = [newReview, ...history].slice(0, 5);

    setHistory(updatedHistory);

    localStorage.setItem(
        "reviewHistory",
        JSON.stringify(updatedHistory)
    );

} else {

    alert(response.message);

}

        } catch (error) {

            console.log(error);
            alert("Unable to review code.");

        } finally {

            setLoading(false);

        }

    };

    // ==========================
    // Logout
    // ==========================

    const handleLogout = () => {

    localStorage.removeItem("token");
    navigate("/login");

};

const handleUploadClick = () => {
    fileInputRef.current.click();
};

const handleFileUpload = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = (e) => {
        setCode(e.target.result);
    };

    reader.readAsText(file);
};

// ==========================
// Copy AI Review
// ==========================

const handleCopyReview = async () => {

    if (!review.trim()) {
        alert("No review available to copy.");
        return;
    }

    try {

        await navigator.clipboard.writeText(review);

        alert("Review copied successfully!");

    } catch (error) {

        console.error(error);

        alert("Failed to copy review.");

    }

};
const handleDownloadReview = () => {

    if (!review.trim()) {
        alert("No review available to download.");
        return;
    }

    const blob = new Blob([review], { type: "text/plain" });

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "AI_Review.txt";

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    window.URL.revokeObjectURL(url);

};
const handleClearEditor = () => {

    if (window.confirm("Are you sure you want to clear the editor?")) {
        setCode("");
    }

};

const handleClearReview = () => {

    if (window.confirm("Are you sure you want to clear the AI review?")) {
        setReview("");
    }

};
// ==========================
// Delete History Item
// ==========================

const handleDeleteHistory = (id) => {

    const updatedHistory = history.filter(item => item.id !== id);

    setHistory(updatedHistory);

    localStorage.setItem(
        "reviewHistory",
        JSON.stringify(updatedHistory)
    );
};

// ==========================
// Clear All History
// ==========================

const handleClearHistory = () => {

    if (!window.confirm("Delete all review history?")) return;

    setHistory([]);

    localStorage.removeItem("reviewHistory");
};

    return (

    <div className="dashboard">

        <Navbar />

        <div className="welcome-section">

            <h1>
                Welcome Back{user ? `, ${user.username}` : ""} 👋
            </h1>

            <p>AI-Powered Code Analysis Platform</p>

        </div>

            {/* Workspace */}

            <div className="workspace">

                {/* Monaco Editor */}

                <EditorPanel
                    code={code}
                    setCode={setCode}
                    language={language}
                />
                {/* AI Analysis */}

                <div className="right-panel">

                    
                    <div className="analysis-header">

    <div>
        <h2 className="analysis-title">
            🤖 AI Analysis
        </h2>

        <p className="analysis-subtitle">
            Powered by Gemini AI • Real-time Code Review
        </p>
    </div>

    <div className="analysis-badge">
        {loading ? "Analyzing..." : "Ready"}
    </div>

</div>
<div className="insight-grid">

    <div className="insight-card">
        <span>📄 Lines</span>
        <h3>{code ? code.split("\n").length : 0}</h3>
    </div>

    <div className="insight-card">
        <span>💻 Language</span>
        <h3>{language.toUpperCase()}</h3>
    </div>

    <div className="insight-card">
        <span>⭐ Status</span>
        <h3>{review ? "Reviewed" : "Pending"}</h3>
    </div>

    <div className="insight-card">
        <span>🤖 AI</span>
        <h3>Gemini</h3>
    </div>

</div>

                   <div className="markdown-body">
    {review ? (
        <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
                code({ inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || "");

                    return !inline && match ? (
                        <SyntaxHighlighter
                            style={oneDark}
                            language={match[1]}
                            PreTag="div"
                            {...props}
                        >
                            {String(children).replace(/\n$/, "")}
                        </SyntaxHighlighter>
                    ) : (
                        <code className={className} {...props}>
                            {children}
                        </code>
                    );
                },
            }}
        >
            {review}
        </ReactMarkdown>
    ) : (
        <div className="empty-review">
            <h2>🤖 Ready to Review</h2>

            <p>
                Paste your code into the editor and click
                <strong> Review Code</strong>.
            </p>

            <ul>
                <li>✅ Bug Detection</li>
                <li>✅ Performance Suggestions</li>
                <li>✅ Code Quality Analysis</li>
                <li>✅ Best Practices</li>
                <li>✅ Security Checks</li>
            </ul>
        </div>
    )}
</div>
    
                    
                                </div>

            </div>
            {/* Review History */}

<div className="history-panel">

    <div className="history-header">

        <h3>📜 Review History</h3>

        <button
            className="clear-history-btn"
            onClick={handleClearHistory}
        >
            Clear All
        </button>

    </div>

    <input
        type="text"
        className="history-search"
        placeholder="🔍 Search by language..."
        value={searchHistory}
        onChange={(e) => setSearchHistory(e.target.value)}
    />

    {history
        .filter((item) =>
            item.language
                .toLowerCase()
                .includes(searchHistory.toLowerCase())
        )
        .length === 0 ? (

        <p style={{ color: "#9ca3af" }}>
            No matching reviews.
        </p>

    ) : (

        history
            .filter((item) =>
                item.language
                    .toLowerCase()
                    .includes(searchHistory.toLowerCase())
            )
            .map((item) => (

                <div
                    key={item.id}
                    className="history-card"
                >

                    <div
                        style={{ flex: 1, cursor: "pointer" }}
                        onClick={() => setReview(item.review)}
                    >

                        <strong>{item.language.toUpperCase()}</strong>

                        <br />

                        <small>{item.createdAt}</small>

                        <p>
                            {item.review.substring(0, 80)}...
                        </p>

                    </div>

                    <button
                        className="delete-history-btn"
                        onClick={() => handleDeleteHistory(item.id)}
                    >
                        🗑
                    </button>

                </div>

            ))

    )}

</div>

            

            <input
                type="file"
    ref={fileInputRef}
    style={{ display: "none" }}
    accept=".py,.java,.js,.cpp,.c,.txt"
    onChange={handleFileUpload}
/>

            {/* Toolbar */}

            <div className="toolbar">

                <div className="toolbar-left">

                    <select
    value={language}
    onChange={(e) => setLanguage(e.target.value)}
>

                        <option value="python">Python</option>
                        <option value="java">Java</option>
                        <option value="javascript">JavaScript</option>
                        <option value="cpp">C++</option>

                    </select>

                </div>

                <div className="toolbar-right">

    <button onClick={handleUploadClick}>
        📁 Upload
    </button>

    <button onClick={handleCopyReview}>
        📋 Copy Review
    </button>

    <button onClick={handleDownloadReview}>
        📥 Download
    </button>

    <button onClick={handleClearEditor}>
        🗑️ Clear Editor
    </button>

    <button onClick={handleClearReview}>
        🧹 Clear Review
    </button>

    <button
    onClick={handleReview}
    disabled={loading}
>
    {loading ? (
        <span className="loading-content">
            <span className="loading-spinner"></span>
            Reviewing...
        </span>
    ) : (
        "🤖 Review Code"
    )}
</button>

    <button onClick={handleLogout}>
        🚪 Logout
    </button>

</div>
            </div>
            <footer className="footer">
    <p>© 2026 Code Reviewer AI • Analyze • Improve • Optimize</p>
    <p>Built with ❤️ using React, Flask, MySQL & Gemini AI</p>
</footer>
            

        </div>

    );

}

export default Dashboard;