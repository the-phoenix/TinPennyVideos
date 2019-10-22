import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import actions from "redux/auth/actions";
import LoginForm from "./LoginForm";
import { Helmet } from "react-helmet";

@connect(
  state => ({
    auth: state.auth
  }),
  { login: actions.login }
)
class Login extends Component {
  onSubmit = ({email, password }) => {
    const { login } = this.props;
    
    login(email, password);
  };

  render() {
    const {auth} = this.props;
    
    return (
      <Fragment>
        <Helmet title="Login"></Helmet>
        <LoginForm onSubmit={this.onSubmit} serverError={auth.error} />
      </Fragment>
    )
  }
}

export default Login;
