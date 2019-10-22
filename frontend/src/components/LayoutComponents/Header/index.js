import React from 'react'
import { Link } from "react-router-dom"

const Header = (props) => (
  <nav className="navbar" data-bulma="navbar">
    <div className="container">
      <div className="navbar-brand">
        <a className="navbar-item" href="/home">
          TinPennyVideo
        </a>
        <span className="navbar-burger burger" data-trigger data-target="navbarMenu">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </div>
      <div id="navbarMenu" className="navbar-menu">
        <div className="navbar-end">
          <Link to="/home" className="navbar-item">
            Home
          </Link>
          <div className="navbar-item">
            <div className="buttons">
              {props.authorized ?
                <a className="button is-primary" onClick={props.logout}>
                  Logout
                </a>
              : <Link to="/auth/login" className="button is-primary">
                  Login
                </Link>
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
)

export default Header
