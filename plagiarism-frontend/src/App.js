import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ReactDOM from 'react-dom/client'
import Navbar from '../src/Components/Navbar';
import './App.css';
import Body from './Components/Body';
import image from './sideimage.png';
import FileUploadBox from './Components/FileUploadBox';
import Footer from './Components/Footer';
import SecondBody from './Components/secondBody';
import ResultPage from './Components/ResultPage';




function App() {


  return (
    <Router>
      <div className='appBase'>
      < Navbar/>

      <Routes>
        <Route path="/" element={
        <>
          <div className='main'>
            <div className='Body'> <Body /> </div>
            <div className='flex-container'>
              <div className='image'> <img src={image} alt="plagiarism-image"></img></div>
              <div className='uploadBox'> <FileUploadBox /></div>
            </div> 
            <div className='postbody'><SecondBody /></div>
          </div>
        </>
      }/>
       <Route path="/results" element={<ResultPage />} />
      </Routes>
      
      <div className='footerbase'>
        <Footer />
      </div>  
    </div>
    </Router>
    
    
  );
}

export default App;
