import React from 'react'
import { Switch, Route } from 'react-router-dom'

import PostList from "./containers/PostList";

const BaseRoutes = () => (
  <div>
    <Switch>
      <Route exact path="/" component={PostList} />
      <Route exact path="/posts/page=:page" component={PostList} />
    </Switch>
  </div>
);

export default BaseRoutes;