import React, { useState } from 'react'

function Word(props) {
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