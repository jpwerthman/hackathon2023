import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';
import Response from './components/response';
import Prompt from './components/prompt';



function App() {
const [transactions, setTransactions] = useState([]);


  return (
    <div className="app-container">
      <div className='vertical-stack'>
      <Response />
      <Prompt />
      </div>
      
    </div>
  );
}

export default App;
