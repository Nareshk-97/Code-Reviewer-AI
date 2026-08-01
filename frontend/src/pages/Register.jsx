import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

function Register() {

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const navigate = useNavigate();

    const handleRegister = async () => {

        try {

            const response = await axios.post(
                "https://code-reviewer-ai-1-22gz.onrender.com/register",
                {
                    username,
                    email,
                    password
                }
            );

            alert(response.data.message);

            navigate("/login");

        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.message || "Registration Failed"
            );

        }

    };

    return (

        <div className="login-container">

            <div className="login-card">

                <h1>Create Account</h1>

                <p>Register to continue</p>

                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />

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

                <button onClick={handleRegister}>
                    Register
                </button>

                <p>
                    Already have an account?
                    <Link to="/login"> Login</Link>
                </p>

            </div>

        </div>

    );
}

export default Register;