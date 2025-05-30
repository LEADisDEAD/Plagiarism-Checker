import React from "react";
import { useLocation , useNavigate } from "react-router-dom";
import "./ResultPage.css"; // Create this CSS file for styling

function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const resultData = location.state;

  if (!resultData) {
    return (
      <div className="error-container">
        <h2>No results found</h2>
        <p>Please upload a document first to check for plagiarism</p>
      </div>
    );
  }

  return (
    <div className="results-container">
      <h1>Plagiarism Report</h1>
      
      <div className="summary">
        <h3>{resultData.filename}</h3>
        <div className={`score ${resultData.plagiarism_score > 50 ? 'high' : 'low'}`}>
          {resultData.plagiarism_score}% similar content found
        </div>
      </div>

      <button
        onClick={()=> navigate("/")}
        style={{
          padding: "8px 16px",
          background: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          margin: "10px 0"
        }}
      >
        ← Back to Home
      </button>





      <div className="detailed-results">
        {resultData.results.map((item, index) => (
          <div key={index} className="phrase-result">
            <p className="original-phrase">"{item.phrase}"</p>
            
            {item.matches.length > 0 ? (
              <ul className="matches-list">
                {item.matches.map((match, i) => (
                  <li key={i}>
                    <a href={match.url} target="_blank" rel="noopener noreferrer">
                      {match.url}
                    </a>
                    <span> - {match.match}% match</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="no-matches">No similar content found</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ResultPage;