import React from 'react';
import { Link } from "react-router-dom";

import {Navbar, NavDropdown, Nav, Button, Form, FormControl} from 'react-bootstrap'

export default class Header extends React.Component {
    render() {
        return (
            <Navbar bg="light" expand="lg">
            <Navbar.Brand href="home">The Bakery</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                <Nav.Link href="FetchCookies">Cookies</Nav.Link>
                <Nav.Link href="FetchCustomers">Customers</Nav.Link>
                {/* <NavDropdown title={this.state.user} id="basic-nav-dropdown">
                  <NavDropdown.Item href="login">Log in</NavDropdown.Item>
                  <NavDropdown.Item href="register">Register</NavDropdown.Item>
                  <NavDropdown.Divider />
                  <NavDropdown.Item href="myPage">My page</NavDropdown.Item>
                </NavDropdown> */}
              </Nav>
              <Form inline>
                <FormControl type="text" placeholder="Search for recipe" className="mr-sm-2" />
                <Button variant="outline-success">Search</Button>
              </Form>
            </Navbar.Collapse>
          </Navbar>
        );
    }
}