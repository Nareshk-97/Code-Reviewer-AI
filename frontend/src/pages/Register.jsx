import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

import {
    FiUser,
    FiMail,
    FiLock,
    FiEye,
    FiEyeOff,
    FiArrowRight,
    FiShield,
    FiCpu,
    FiCheckCircle
} from "react-icons/fi";

import "../styles/Register.css";

function Register() {

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const handleRegister = async (e) => {

        e.preventDefault();

        setError("");

        if (!username || !email || !password) {
            setError("Please fill in all fields.");
            return;
        }

        if (password.length < 6) {
            setError("Password must be at least 6 characters.");
            return;
        }

        try {

            setLoading(true);

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

            setError(
                error.response?.data?.message ||
                "Registration failed. Please try again."
            );

        } finally {

            setLoading(false);

        }
    };

    return (

        <div className="register-page">

            {/* Background effects */}

            <div className="register-glow register-glow-one"></div>
            <div className="register-glow register-glow-two"></div>


            <div className="register-wrapper">


                {/* =================================
                    LEFT HERO SECTION
                ================================= */}

                <section className="register-hero">

                    {/* Brand */}

                    <div className="register-brand">

                        <div className="register-brand-icon">
                            <FiCpu />
                        </div>

                        <span>
                            Code Reviewer AI
                        </span>

                    </div>


                    <div className="register-hero-content">

                        <div className="register-badge">

                            <span className="register-status-dot"></span>

                            Start Your AI Coding Journey

                        </div>


                        <h1>

                            Build.
                            <span> Review.</span>
                            <br />
                            Improve.

                        </h1>


                        <p>

                            Create your account and unlock an
                            intelligent coding assistant that helps
                            you write cleaner, safer, and better code.

                        </p>


                        {/* Benefits */}

                        <div className="register-benefits">

                            <div className="register-benefit">

                                <div className="benefit-icon">
                                    <FiCheckCircle />
                                </div>

                                <div>

                                    <h3>
                                        AI-Powered Reviews
                                    </h3>

                                    <p>
                                        Get intelligent feedback
                                        on your code using Gemini AI.
                                    </p>

                                </div>

                            </div>


                            <div className="register-benefit">

                                <div className="benefit-icon">
                                    <FiCheckCircle />
                                </div>

                                <div>

                                    <h3>
                                        Improve Code Quality
                                    </h3>

                                    <p>
                                        Discover bugs, performance
                                        issues, and better approaches.
                                    </p>

                                </div>

                            </div>


                            <div className="register-benefit">

                                <div className="benefit-icon">
                                    <FiCheckCircle />
                                </div>

                                <div>

                                    <h3>
                                        Developer Focused
                                    </h3>

                                    <p>
                                        Built to make everyday
                                        development faster and easier.
                                    </p>

                                </div>

                            </div>

                        </div>


                        {/* Developer quote */}

                        <div className="developer-message">

                            <FiCpu />

                            <div>

                                <strong>
                                    Your code deserves a second pair of eyes.
                                </strong>

                                <span>
                                    Let AI help you find what you missed.
                                </span>

                            </div>

                        </div>

                    </div>


                    <div className="register-footer">

                        <span>
                            AI-powered development
                        </span>

                        <span>•</span>

                        <span>
                            Secure authentication
                        </span>

                        <span>•</span>

                        <span>
                            Built for developers
                        </span>

                    </div>

                </section>


                {/* =================================
                    RIGHT REGISTER SECTION
                ================================= */}

                <section className="register-section">

                    <div className="register-card">


                        {/* Mobile brand */}

                        <div className="mobile-register-brand">

                            <div className="register-brand-icon">
                                <FiCpu />
                            </div>

                            <span>
                                Code Reviewer AI
                            </span>

                        </div>


                        {/* Heading */}

                        <div className="register-heading">

                            <div className="register-welcome-icon">
                                🚀
                            </div>

                            <h2>
                                Create Your Account
                            </h2>

                            <p>
                                Start reviewing and improving your
                                code with AI.
                            </p>

                        </div>


                        <form onSubmit={handleRegister}>


                            {/* Username */}

                            <div className="register-input-group">

                                <label>
                                    Username
                                </label>

                                <div className="register-input-wrapper">

                                    <FiUser />

                                    <input
                                        type="text"
                                        placeholder="Enter your username"
                                        value={username}
                                        onChange={(e) =>
                                            setUsername(e.target.value)
                                        }
                                    />

                                </div>

                            </div>


                            {/* Email */}

                            <div className="register-input-group">

                                <label>
                                    Email Address
                                </label>

                                <div className="register-input-wrapper">

                                    <FiMail />

                                    <input
                                        type="email"
                                        placeholder="you@example.com"
                                        value={email}
                                        onChange={(e) =>
                                            setEmail(e.target.value)
                                        }
                                    />

                                </div>

                            </div>


                            {/* Password */}

                            <div className="register-input-group">

                                <div className="register-password-label">

                                    <label>
                                        Password
                                    </label>

                                    <span>
                                        Minimum 6 characters
                                    </span>

                                </div>


                                <div className="register-input-wrapper">

                                    <FiLock />

                                    <input
                                        type={
                                            showPassword
                                                ? "text"
                                                : "password"
                                        }
                                        placeholder="Create a password"
                                        value={password}
                                        onChange={(e) =>
                                            setPassword(e.target.value)
                                        }
                                    />


                                    <button
                                        type="button"
                                        className="register-password-toggle"
                                        onClick={() =>
                                            setShowPassword(
                                                !showPassword
                                            )
                                        }
                                    >

                                        {showPassword
                                            ? <FiEyeOff />
                                            : <FiEye />
                                        }

                                    </button>

                                </div>

                            </div>


                            {/* Error */}

                            {error && (

                                <div className="register-error">

                                    {error}

                                </div>

                            )}


                            {/* Register button */}

                            <button
                                type="submit"
                                className="register-button"
                                disabled={loading}
                            >

                                {loading ? (

                                    <>
                                        <span className="register-spinner"></span>
                                        Creating Account...
                                    </>

                                ) : (

                                    <>
                                        Create Account
                                        <FiArrowRight />
                                    </>

                                )}

                            </button>


                            {/* Security */}

                            <div className="register-security">

                                <FiShield />

                                <span>
                                    Your account is protected with
                                    secure authentication.
                                </span>

                            </div>

                        </form>


                        {/* Login link */}

                        <div className="register-login-link">

                            <span>
                                Already have an account?
                            </span>

                            <Link to="/login">
                                Sign in to your account
                            </Link>

                        </div>

                    </div>

                </section>

            </div>

        </div>
    );
}

export default Register;