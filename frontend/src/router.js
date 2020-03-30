import React, { PureComponent } from "react";
import { Route, Switch, Redirect } from "react-router";
import { ConnectedRouter } from "connected-react-router";
import Loadable from "react-loadable";

import Loader from "./components/LayoutComponents/Loader";
import NotFound from "./pages/404";
import IndexLayout from "./layouts";

const loadable = loader =>
  Loadable({
    loader,
    delay: false,
    loading: () => <Loader />
  });

const routes = [
  // Home
  {
    path: "/home",
    component: loadable(() => import("./pages/home")),
    exact: true
  },
  // Video Pages
  {
    path: "/watch/:id",
    component: loadable(() => import("./pages/watch")),
    exact: true
  },
  {
    path: "/videos/add",
    component: loadable(() => import("./pages/video-add")),
    exact: true
  },
  // Auth Pages
  {
    path: "/auth/login",
    // component: Login,
    component: loadable(() => import("./pages/auth/login")),
    exact: true
  },
];

class Router extends PureComponent {
  render() {
    const { history } = this.props;

    return (
      <ConnectedRouter history={history}>
        <IndexLayout>
          <Switch>
            <Route exact path="/" render={() => <Redirect to="/home" />} />
            {routes.map(route => (
              <Route
                path={route.path}
                component={route.component}
                key={route.path}
                exact={route.exact}
              />
            ))}
            <Route component={NotFound} />
          </Switch>
        </IndexLayout>
      </ConnectedRouter>
    );
  }
}

export default Router;
