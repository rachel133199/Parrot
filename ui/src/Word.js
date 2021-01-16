import React, { useState } from 'react'

function Word(props) {
    return (
        <div className="Word">
            <a href="#" onClick={props.getWord}>{props.word}</a>
        </div>
    )
}

export default Word