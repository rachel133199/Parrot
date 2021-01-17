import React, { useEffect } from 'react';
import {getSpeech} from './azure';

function Word(props) {
    useEffect(() => {
       pronounce(props.word);
    });

    let audio;
    
    async function pronounce(word) {
        let recording = await getSpeech(word);
        const audioUrl = URL.createObjectURL(recording);
        audio = new Audio(audioUrl);
        audio.play();
    }

    return (
        <div>
            <span className="Word">
                {/* <a href="#" onClick={props.getWord} onMouseOver={props.changeColor} onMouseLeave={props.changeBackColor} >{props.word}</a> */}
                <a href="#" onClick={props.getWord}>{props.word}</a>
                {/* <h1>{props.Word}</h1> */}
            </span>
        </div>
    )
}

export default Word