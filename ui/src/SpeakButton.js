import React from 'react'
import Button from 'react-bootstrap/Button'
import { faMicrophone } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function SpeakButton(props){
    return(
        <Button className="SpeakButton" variant="primary">
            <FontAwesomeIcon className="Microphone" icon={faMicrophone} size="10x"/>
        </Button>
    )
}

export default SpeakButton;