import "../styles/Navbar.css";

function Navbar({ onLogout }) {
  return (
    <header className="navbar">

      <div className="logo-container">
        <div className="logo-icon">🤖</div>

        <div>
          <h2>Code Reviewer AI</h2>
          <p>Analyze • Improve • Optimize</p>
        </div>
      </div>

      <div className="nav-right">

        <div className="ai-status">
          <span className="status-circle"></span>
          AI Ready
        </div>

        <button className="logout-btn" onClick={onLogout}>
          Logout
        </button>

      </div>

    </header>
  );
}

export default Navbar;