import React from 'react'

function Word(props){
    return(
        <div className="Word">
            <a href="#" onClick={props.onClick}>{props.word}</a>
        </div>
    )
}

export default Word