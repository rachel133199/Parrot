import './App.css';
import Word from './Word'
import SpeakButton from './SpeakButton'
import PlayButton from './PlayButton'
import Phoneme from './Phoneme'
import NavBar from './NavBar'
import { useState } from 'react';


function App() {
  const [phmCol, setPhmCol] = useState({ color: "gray" })
  const [word, setWord] = useState({
    phonemes: ["P", "EH1", "R", "AH0", "T"],
    word: "parrot"
  })

  function changeColor() {
    console.log('color change!')
    setPhmCol({ color: "green" })
    setTimeout(function () { setPhmCol({ color: "gray" }) }, 500)
  }

  function getWord() {
    changeColor()
    fetch("http://127.0.0.1:5000/get_word")
      .then(response => response.json())
      .then(response => {
        // console.log(response)
        setWord(response)
        console.log(word)
      });

    return word.word
  }

  return (
    <div className="App">
      <NavBar />
      <Word getWord={getWord} word={word.word}/>
      <Phoneme phmCol={phmCol} phm={word.phonemes} />
      <SpeakButton />
      <PlayButton onClick={changeColor}/>
    </div>
  );
}

export default App;
