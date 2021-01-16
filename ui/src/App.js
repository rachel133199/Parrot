import './App.css';
import Word from './Word'
import SpeakButton from './SpeakButton'
import PlayButton from './PlayButton'
import Phoneme from './Phoneme'
import NavBar from './NavBar'
import { useState } from 'react';


function App() {
  const [phmCol, setPhmCol] = useState({color: "gray"})
  
  function onClick() {
    console.log('color change!')
    setPhmCol({color: "green"})
    setTimeout(function(){setPhmCol({color: "gray"})}, 500)
  }

  return (
    <div className="App">
      <NavBar />
      <Word word="Parrot" onClick={onClick}/>
      <Phoneme phmCol={phmCol} phm={"P EH R AH T"}/>
      <SpeakButton />
      <PlayButton />
    </div>
  );
}

export default App;
