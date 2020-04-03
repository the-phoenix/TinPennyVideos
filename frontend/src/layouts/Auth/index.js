import React from "react";
import { Link } from "react-router-dom";
import { withRouter } from "react-router";

class AuthLayout extends React.PureComponent {
  render() {
    const { children } = this.props;

    return (
      <section className="hero is-fullheight">
        <div className="hero-body">
          <div className="container has-text-centered">
            <div className="column is-4 is-offset-4">
              {children}
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default withRouter(AuthLayout);
