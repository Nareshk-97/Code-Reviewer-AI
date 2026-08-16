import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

import {
    FiMail,
    FiLock,
    FiArrowRight,
    FiShield,
    FiZap,
    FiCode,
    FiCpu
} from "react-icons/fi";

import "../styles/Login.css";

function Login() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const handleLogin = async () => {

        if (!email || !password) {
            alert("Please enter your email and password.");
            return;
        }

        try {

            setLoading(true);

            const response = await axios.post(
                "https://code-reviewer-ai-1-22gz.onrender.com/login",
                {
                    email,
                    password
                }
            );

            localStorage.setItem(
                "token",
                response.data.token
            );

            alert(response.data.message);

            navigate("/dashboard");

        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.message ||
                "Login failed. Please try again."
            );

        } finally {

            setLoading(false);

        }
    };

    return (
        <div className="login-page">

            {/* Background effects */}
            <div className="background-glow glow-one"></div>
            <div className="background-glow glow-two"></div>

            <div className="login-wrapper">

                {/* =========================
                    LEFT SIDE
                ========================== */}

                <section className="login-hero">

                    {/* Brand */}

                    <div className="brand">

                        <div className="brand-icon">
                            <FiCpu />
                        </div>

                        <span>
                            Code Reviewer AI
                        </span>

                    </div>


                    {/* Hero Content */}

                    <div className="hero-content">

                        <div className="hero-badge">

                            <span className="status-dot"></span>

                            AI-Powered Development Platform

                        </div>


                        <h1>
                            Write Better Code.
                            <span> Faster.</span>
                        </h1>


                        <p className="hero-description">
                            Analyze your code with AI-powered insights.
                            Detect bugs, improve performance, strengthen
                            security, and follow better coding practices.
                        </p>


                        {/* Feature Cards */}

                        <div className="feature-list">

                            <div className="feature-item">

                                <div className="feature-icon">
                                    <FiCpu />
                                </div>

                                <div>

                                    <h3>
                                        Gemini AI Analysis
                                    </h3>

                                    <p>
                                        Intelligent code reviews and
                                        actionable recommendations.
                                    </p>

                                </div>

                            </div>


                            <div className="feature-item">

                                <div className="feature-icon">
                                    <FiShield />
                                </div>

                                <div>

                                    <h3>
                                        Security Focused
                                    </h3>

                                    <p>
                                        Identify potential security issues
                                        before they become problems.
                                    </p>

                                </div>

                            </div>


                            <div className="feature-item">

                                <div className="feature-icon">
                                    <FiZap />
                                </div>

                                <div>

                                    <h3>
                                        Instant Feedback
                                    </h3>

                                    <p>
                                        Get useful suggestions in seconds,
                                        not hours.
                                    </p>

                                </div>

                            </div>

                        </div>


                        {/* Code Preview */}

                        <div className="code-preview">

                            <div className="code-header">

                                <div className="window-dots">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>

                                <div className="code-title">

                                    <FiCode />

                                    example.py

                                </div>

                                <div className="ai-status">
                                    AI Ready
                                </div>

                            </div>


                            <div className="code-body">

                                <div>

                                    <span className="line-number">
                                        01
                                    </span>

                                    <span className="keyword">
                                        def
                                    </span>{" "}

                                    <span className="function">
                                        calculate_total
                                    </span>

                                    (items):

                                </div>


                                <div>

                                    <span className="line-number">
                                        02
                                    </span>

                                    &nbsp;&nbsp;&nbsp;&nbsp;

                                    <span className="keyword">
                                        return
                                    </span>{" "}

                                    sum(items)

                                </div>


                                <div className="ai-message">

                                    <FiCpu />

                                    Code looks clean. Ready for review.

                                </div>

                            </div>

                        </div>

                    </div>


                    {/* Footer */}

                    <div className="hero-footer">

                        <span>
                            Built for developers
                        </span>

                        <span>•</span>

                        <span>
                            Powered by Gemini AI
                        </span>

                        <span>•</span>

                        <span>
                            Secure & Fast
                        </span>

                    </div>

                </section>


                {/* =========================
                    RIGHT SIDE LOGIN
                ========================== */}

                <section className="login-section">

                    <div className="login-card">


                        {/* Mobile Brand */}

                        <div className="mobile-brand">

                            <div className="brand-icon">
                                <FiCpu />
                            </div>

                            <span>
                                Code Reviewer AI
                            </span>

                        </div>


                        {/* Heading */}

                        <div className="login-heading">

                            <div className="welcome-icon">
                                👋
                            </div>

                            <h2>
                                Welcome Back
                            </h2>

                            <p>
                                Sign in to continue reviewing your code.
                            </p>

                        </div>


                        {/* Email */}

                        <div className="input-group">

                            <label>
                                Email Address
                            </label>

                            <div className="input-wrapper">

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

                        <div className="input-group">

                            <div className="password-label">

                                <label>
                                    Password
                                </label>

                                <span>
                                    Secure Login
                                </span>

                            </div>

                            <div className="input-wrapper">

                                <FiLock />

                                <input
                                    type="password"
                                    placeholder="Enter your password"
                                    value={password}
                                    onChange={(e) =>
                                        setPassword(e.target.value)
                                    }
                                />

                            </div>

                        </div>


                        {/* Login Button */}

                        <button
                            className="login-button"
                            onClick={handleLogin}
                            disabled={loading}
                        >

                            {loading ? (

                                <>
                                    <span className="spinner"></span>
                                    Signing in...
                                </>

                            ) : (

                                <>
                                    Sign In
                                    <FiArrowRight />
                                </>

                            )}

                        </button>


                        {/* Security */}

                        <div className="security-note">

                            <FiShield />

                            <span>
                                Your connection is protected with
                                secure authentication.
                            </span>

                        </div>


                        {/* Register */}

                        <div className="register-section">

                            <span>
                                Don't have an account?
                            </span>

                            <Link to="/register">
                                Create a free account
                            </Link>

                        </div>

                    </div>

                </section>

            </div>

        </div>
    );
}

export default Login;