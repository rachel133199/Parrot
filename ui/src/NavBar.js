import React from 'react'
import { faCrow } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'

function NavBar() {
    return (
        <Navbar bg="outline-primary">
            <a href="#">
                <FontAwesomeIcon className="Bars" icon={faCrow} size="4x" />
                <Navbar.Brand href="#">
                    <h3 className="ParrotHome">Parrot Home</h3>
                </Navbar.Brand>
            </a>
        </Navbar>
    )
}

export default NavBar