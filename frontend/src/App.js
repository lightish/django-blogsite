import React from 'react';
import { BrowserRouter } from "react-router-dom";
import 'antd/dist/antd.css';

import BaseLayout from "./containers/Layout";
import BaseRoutes from "./routes";

const App = () => (
  <BrowserRouter>
    <BaseLayout>
      <BaseRoutes />
    </BaseLayout>
  </BrowserRouter>
)

export default App;
