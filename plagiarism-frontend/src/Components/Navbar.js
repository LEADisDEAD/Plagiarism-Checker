import React from "react";
import ReactDOM from "react-dom/client"
import './Navbar.css'; 
import logo from './Logo.png';


function Navbar() {
    return (
        <div className="navbar">
            <img src={logo} className="logo"/>
            <h2 className="heading"> Plagiarism Checker</h2>
        </div>
        
    )
}

export default Navbar;