import React from "react"
import {Nav, Navbar, NavDropdown} from 'react-bootstrap'
import {Link, useLocation} from "react-router-dom";
import {useEffect, useState} from "react";
import authService from "./services/auth.service";
import DropdownMenu from "react-bootstrap/DropdownMenu";

export default function MyNavbar() {
    const {pathname} = useLocation()
    const [currentUser, setCurrentUser] = useState(undefined);

    useEffect(() => {
        const user = authService.getCurrentUser();

        if (user) {
            setCurrentUser(user);
        }

    }, [pathname]);

    const logOut = () => {
        authService.logout()
    }

  return (
    <div>
      <Navbar bg="dark" variant="dark">
          <Navbar.Brand>
            Cinema
          </Navbar.Brand>
          <Nav>
              <Nav.Link as={Link} to="/movies"> Movies </Nav.Link>
              <Nav.Link as={Link} to="/sessions"> Sessions </Nav.Link>
              <NavDropdown title={"Search by"}>
                  <NavDropdown.Item href="/actors">Actor</NavDropdown.Item>
                  <NavDropdown.Item href="/genres">Genre</NavDropdown.Item>
                  <NavDropdown.Item href="/directors">Director</NavDropdown.Item>
              </NavDropdown>
              {currentUser && <>
                  <Nav.Link as={Link} to="/profile"> Profile </Nav.Link>
              </>}
          </Nav>
          <Nav className="ms-auto">
              { !currentUser ? <>
                  <Nav.Link as={Link} to="/auth/login"> Login </Nav.Link>
                  <Nav.Link href="#"> Sign Up </Nav.Link>
                  </> : <>
                  <Nav.Link onClick={logOut}> Log Out </Nav.Link>
                  </>
              }
          </Nav>
      </Navbar>
    </div>
  );
}