import React from "react";
import { connect } from "react-redux";

import Header from "components/LayoutComponents/Header";
import Footer from "components/LayoutComponents/Footer";
import authActions from "redux/auth/actions";

@connect(
  ({ auth }) => ({ authorized: auth.authorized }),
  { logout: authActions.logout }
)
class MainLayout extends React.PureComponent {
  render() {
    const { children, authorized, logout } = this.props; // eslint-disable-line
    
    return (
      <div>
        <Header authorized={authorized} logout={logout}/>
        <div className="utils__content">{children}</div>
        <Footer />
      </div>
    );
  }
}

export default MainLayout;
