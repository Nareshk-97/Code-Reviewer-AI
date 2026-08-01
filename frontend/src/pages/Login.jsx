import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

function Login() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const navigate = useNavigate();

    const handleLogin = async () => {

        try {
            

            const response = await axios.post(
                "https://code-reviewer-ai-1-22gz.onrender.com/login",
                {
                    email,
                    password
                }
            );

            alert(response.data.message);

            localStorage.setItem(
                "token",
                response.data.token
            );

            navigate("/dashboard");

        } catch (error) {

            console.log(error);
            console.log(error.response);
            console.log(error.response?.data);

            alert(
                error.response?.data?.message || "Login Failed"
            );
        }

    };

    return (
        <div className="login-container">

            <div className="login-card">

                <h1>AI Code Reviewer</h1>

                <p>Login to continue</p>

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />

                <button onClick={handleLogin}>
                    Login
                </button>

                <p>
                    Don't have an account?
                    <Link to="/register"> Register</Link>
                </p>

            </div>

        </div>
    );
}

export default Login;