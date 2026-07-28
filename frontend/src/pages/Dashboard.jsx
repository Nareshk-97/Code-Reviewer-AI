import { useEffect, useState, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { reviewCode } from "../services/reviewService";
import "../styles/Dashboard.css";
import EditorPanel from "../components/EditorPanel";
import Navbar from "../components/Navbar";

function Dashboard() {

    const [user, setUser] = useState(null);
    const [code, setCode] = useState("");
    const [language, setLanguage] = useState("python");
    const [review, setReview] = useState("");
    const [loading, setLoading] = useState(false);

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

                    <h2>🤖 AI Analysis</h2>

                    {
                        review ? (

                            <pre
                                style={{
                                    whiteSpace: "pre-wrap",
                                    color: "#e5e7eb",
                                    lineHeight: "1.6"
                                }}
                            >
                                {review}
                            </pre>

                        ) : (

                            <p
                                style={{
                                    color: "#9ca3af"
                                }}
                            >
                                Your AI review will appear here after clicking
                                <strong> Review Code</strong>.
                            </p>

                        )
                    }

                </div>

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

    <button
        onClick={handleReview}
        disabled={loading}
    >
        {loading ? "Reviewing..." : "🤖 Review Code"}
    </button>

    <button onClick={handleLogout}>
        🚪 Logout
    </button>

</div>
            </div>

        </div>

    );

}

export default Dashboard;