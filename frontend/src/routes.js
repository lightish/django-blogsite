import React from 'react'
import { Route } from 'react-router-dom'

const mainPage = _ => <div>Content</div>

const BaseRoutes = (props) => (
  <Route exact path="/" component={mainPage} />
)

export default BaseRoutes