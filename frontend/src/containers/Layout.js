import React from "react";
import { Layout, Menu } from 'antd';
import { Link } from 'react-router-dom';

const { Header, Content } = Layout;

const BaseLayout = (props) => {
  console.log(props)
  return (
    <Layout className="layout">
      <Header>
        <div className="logo" />
        <Menu theme="dark" mode="horizontal">
          <Menu.Item key="1"><Link to={'/posts/page=1'}>Posts</Link></Menu.Item>
          <Menu.Item key="2">nav 2</Menu.Item>
          <Menu.Item key="3">nav 3</Menu.Item>
        </Menu>
      </Header>
      <Content style={{ padding: '0 50px',
                        height: 'calc(100vh - 64px)',
                        paddingTop: 20 }}>
        <div className="site-layout-content">
          {props.children}
        </div>
      </Content>
    </Layout>
  );
}

export default BaseLayout
