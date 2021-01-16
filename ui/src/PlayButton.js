import React from 'react'
import { faVolumeUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Button from 'react-bootstrap/Button';

function PlayButton() {
    return(
        <Button className="PlayButton">
            <FontAwesomeIcon className="VolumeUp" icon={faVolumeUp} size="10x"/>
        </Button>
    )
}

export default PlayButton