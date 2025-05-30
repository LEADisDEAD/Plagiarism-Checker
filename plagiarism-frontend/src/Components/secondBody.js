import React from 'react'
import ReactDOM from 'react-dom/client'
import './secondBody.css';

function SecondBody() {
    return(

        <div className="value-grid">
        <div className="value-card">
          <div className="value-icon">⚡</div>
          <h3>Lightning Fast</h3>
          <p>Get results before you finish your coffee</p>
        </div>
        
        <div className="value-card">
          <div className="value-icon">🛡️</div>
          <h3>High-Level Security</h3>
          <p>Your documents auto-delete after checking</p>
        </div>
        
        <div className="value-card">
          <div className="value-icon">🔍</div>
          <h3>Deep Scan</h3>
          <p>Compares against 25B+ web pages and academic papers</p>
        </div>
      </div>

    )
}

export default SecondBody;