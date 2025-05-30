import React from "react";
import ReactDOM from "react-dom/client";
import './Footer.css';

function Footer() {
    return(
        <div className="footerBase">

            <div className="part1">
                <h3>Plagiarism checker</h3>
                <p> Free plagiarism check in seconds.  For students, writers, and anyone who’s ever clicked "Copy."</p> 
                <ul> <li> Paste </li> <li> Check </li> <li> Breathe </li> </ul>
                
            </div>

            <div className="Contact">
                <ul className="email">
                    <h2>Contact Us </h2>
                    <li className="author1">
                        <i class="bi bi-envelope"></i>
                         prathmeshbajpai123@gmail.com
                    </li>
                    <li className="author2">
                        <i className="bi bi-envelope"></i>
                         dixitaditi20@gmail.com
                    </li>
                </ul>
                
            </div>

            <div className="copyright">
                <p>© 2025 PlagiarismChecker. All rights reserved.</p>
            </div>
        </div>
    )
}

export default Footer;