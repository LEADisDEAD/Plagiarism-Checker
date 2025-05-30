import React from "react";
import axios from "axios";
import { useState , useCallback} from "react";
import "../Components/FileUploadBox.css";
import { useNavigate } from "react-router-dom";

function FileUploadBox() {
    const navigate = useNavigate();
    const[file, setFile] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [text, setText] = useState("");

    const handlefilechange = (e) => {
        setFile(e.target.files[0]);
        setText("");
    };

    const handleDragEnter = useCallback((e) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(true);
    }, []);

    const handDragLeave = useCallback((e) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
    }, []);

    const handleTextChange = (e) => {
      setText(e.target.value);
      if(e.target.value) setFile(null);
    }

    const handleDragOver = useCallback((e) => {
      e.preventDefault();
      e.stopPropagation();
    }, []);

    const handleDrop = useCallback((e) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      if(e.dataTransfer.files && e.dataTransfer.files[0]) {
        setFile(e.dataTransfer.files[0]);
      }
    }, []);

    const handleSubmit = async () => {
    if (!file) {
      alert("Please select or drop a file first.");
      return;
    }


    setIsLoading(true);

    try {
      const formData = new FormData();
      if(file) formData.append("file", file);
      if(text) formData.append("text" , text);

      
        const res = await axios.post("http://127.0.0.1:5000/upload", 
            text ? { text } : formData,  // Send as JSON if text, FormData if file
            {
                headers: {
                    "Content-Type": text ? "application/json" : "multipart/form-data",
                },
            }
        );

      navigate('/results', {state: res.data});

    } catch (err) {
      console.error("Upload failed", err);
      alert("Failed to check plagiarism. Try again.");
    
    }finally {
      setIsLoading(false);
    }
  };

  

    return (
    <div className="container">
        
        <p className="uploadtext"> Please upload your file here to check plagiarism score :</p>
        
        <div 
          className={`upload-box ${isDragging ? 'dragging' : ''}`}
          onDragEnter ={handleDragEnter}
          onDragLeave={handDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => document.querySelector('.file-input').click()}
        >
          {file ? (
            <p className = "file-name"> 📄 {file.name}</p>
          ): (
            <>
            Drag and Drop or <span className="browse"> Browse </span> your files
            </>
          )}
          <input
            type = "file"
            className="file-input"
            onChange={handlefilechange}
          />
        </div>
        <button className="submit-button" onClick={handleSubmit} disabled={isLoading}>{isLoading ? 'Analyzing...' : 'CHECK FOR PLAGIARISM'}</button>
    </div>
      
    );
  
}

export default FileUploadBox;