import React, { useState } from 'react'
import { faVolumeUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function Word(props) {
    return (
        <div>
            <FontAwesomeIcon className="VolumeUp" icon={faVolumeUp} size="10x" />
            <span className="Word">
                {/* <a href="#" onClick={props.getWord} onMouseOver={props.changeColor} onMouseLeave={props.changeBackColor} >{props.word}</a> */}
                <a href="#" onClick={props.getWord}>{props.word}</a>
                {/* <h1>{props.Word}</h1> */}
            </span>
        </div>
    )
}

export default Word