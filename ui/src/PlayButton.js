import React from 'react'
import { faPlayCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Button from 'react-bootstrap/Button';


function PlayButton(props) {
    return(
        <Button className="PlayButton" onClick={props.onClick} disabled={false}>
            <FontAwesomeIcon className="PlayCircle" icon={faPlayCircle} size="10x"/>
        </Button>
    )
}

export default PlayButton