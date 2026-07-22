import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Dashboard() {

    const [user, setUser] = useState(null);

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

    const handleLogout = () => {

        localStorage.removeItem("token");

        navigate("/login");

    };

    return (

        <div className="dashboard-container">

            <div className="dashboard-card">

                <div className="dashboard-header">

                    <h1>AI Code Reviewer</h1>

                    <button
                        className="logout-btn"
                        onClick={handleLogout}
                    >
                        Logout
                    </button>

                </div>

                {
                    user && (

                        <div className="profile-card">

                            <h2>Welcome, {user.username} 👋</h2>

                            <p><strong>Username:</strong> {user.username}</p>

                            <p><strong>Email:</strong> {user.email}</p>

                        </div>

                    )
                }

                <div className="review-card">

                    <h2>AI Code Review</h2>

                    <p>
                        Paste your source code here and get AI-powered
                        suggestions, bug detection, and optimization tips.
                    </p>

                    <textarea
                        rows="12"
                        placeholder="Paste your code here..."
                    ></textarea>

                    <button className="review-btn">

                        Review Code

                    </button>

                </div>

            </div>

        </div>

    );

}

export default Dashboard;