import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { reviewCode } from "../services/reviewService";
import "../styles/Dashboard.css";

function Dashboard() {

    const [user, setUser] = useState(null);

    const [code, setCode] = useState("");
    const [review, setReview] = useState("");
    const [loading, setLoading] = useState(false);

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

    return (

        <div className="dashboard">

            {/* Welcome Section */}

            <div className="welcome-section">

                <h1>
                    Welcome Back{user ? `, ${user.username}` : ""} 👋
                </h1>

                <p>AI-Powered Code Analysis Platform</p>

            </div>

            {/* Workspace */}

            <div className="workspace">

                {/* Left Panel */}

                <div className="left-panel">

                    <h2>💻 Code Playground</h2>

                    <textarea
                        rows="18"
                        placeholder="Paste your code here..."
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                        style={{
                            width: "100%",
                            height: "450px",
                            background: "#111827",
                            color: "#ffffff",
                            border: "1px solid #374151",
                            borderRadius: "10px",
                            padding: "15px",
                            fontSize: "15px",
                            resize: "none",
                            outline: "none"
                        }}
                    />

                </div>

                {/* Right Panel */}

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

            {/* Toolbar */}

            <div className="toolbar">

                <div className="toolbar-left">

                    <select>

                        <option>Python</option>
                        <option>Java</option>
                        <option>JavaScript</option>
                        <option>C++</option>

                    </select>

                </div>

                <div className="toolbar-right">

                    <button
                        onClick={handleReview}
                        disabled={loading}
                    >
                        {loading ? "Reviewing..." : "Review Code"}
                    </button>

                    <button
                        onClick={handleLogout}
                    >
                        Logout
                    </button>

                </div>

            </div>

        </div>

    );

}

export default Dashboard;