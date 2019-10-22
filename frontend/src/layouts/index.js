import React, { Fragment } from "react";
import NProgress from "nprogress";
import { Helmet } from "react-helmet";
import { connect } from "react-redux";
import { withRouter, Redirect } from "react-router-dom";
import Loader from "components/LayoutComponents/Loader";

import AuthLayout from "./Auth";
import MainLayout from "./Main";

const Layouts = {
  auth: AuthLayout,
  main: MainLayout
};

@withRouter
@connect(
  ({ auth }) => ({ auth }),
  { }
)
class IndexLayout extends React.PureComponent {
  previousPath = "";

  componentDidUpdate(prevProps) {
    const { location } = this.props;
    const { prevLocation } = prevProps;
    if (location !== prevLocation) {
      window.scrollTo(0, 0);
    }
  }

  render() {
    const {
      children,
      // loading,
      location: { pathname, search },
      auth
    } = this.props;

    // NProgress Management
    const currentPath = pathname + search;
    if (currentPath !== this.previousPath /* || loading.global */) {
      NProgress.start();
    }

    // if (!loading.global) {
    setTimeout(() => {
      NProgress.done();
      this.previousPath = currentPath;
    }, 300);
    // }

    // Layout Rendering
    const getLayout = () => {
      if (/^\/auth(?=\/|$)/i.test(pathname)) {
        return "auth";
      }

      return "main";
    };

    const Container = Layouts[getLayout()];

    const isUserAuthorized = auth.authorized;
    const isUserLoading = auth.loading;
    const isAuthLayout = getLayout() === "auth";

    const BootstrappedLayout = () => {
      // show loader when user in check authorization process, not authorized yet and not on login pages
      if (isUserLoading && !isUserAuthorized && !isAuthLayout) {
        return <Loader />;
      }

      // // redirect to login page if current is not login page and user not authorized
      // if (!isAuthLayout && !isUserAuthorized) {
      //   return <Redirect to="/auth/login" />;
      // }

      // redirect to main dashboard when user on auth page and authorized
      if (isAuthLayout && isUserAuthorized) {
        return <Redirect to="/home/" />;
      }

      // in other case render previously set layout
      return <Container>{children}</Container>;
    };

    return (
      <Fragment>
        <Helmet titleTemplate="%s - TinPennyVideo" title="Welcome" />
        {BootstrappedLayout()}
      </Fragment>
    );
  }
}

IndexLayout.defaultProps = {
  user: {
    authorized: false
  }
};

export default IndexLayout;
