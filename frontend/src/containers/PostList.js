import React, { useEffect, useState } from 'react'
import { useParams, useHistory } from 'react-router-dom'
import { List, Card } from 'antd'

import { BACKEND_PATH, LIST_POSTS_API_PATH } from "../share";

const PostList = (props) => {
  const params = useParams()
  const history = useHistory()
  const [page, setPage] = useState(params.page ? params.page : 1);
  const [total, setTotal] = useState(0)
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch(`${LIST_POSTS_API_PATH}?page=${page}`)
    .then(resp => resp.json())
    .then(resp => {
      setPosts(resp.results);
      setTotal(resp.count)
    })
  }, [page]);

  return (
    <List
      grid={{
        gutter: 20,
        xs: 1,
        sm: 2,
        md: 2,
        lg: 4,
        xl: 4,
        xxl: 3,
      }}
      pagination={{
        defaultCurrent: page,
        total: total,
        onChange: page => {
          history.push('/posts/page=' + page)
          setPage(page)
        }
      }}
      dataSource={posts}
      renderItem={post => (
        <List.Item>
          <Card
            hoverable
            style={{width: 300}}
            cover={
              <img alt={post.title}
                   src={post.thumbnail ?
                        BACKEND_PATH + post.thumbnail :
                        BACKEND_PATH + post.category.thumbnail}/>
            }
          >
            <Card.Meta title={post.title}
                       description={post.author.username}/>
          </Card>
        </List.Item>
      )}
    />
  );
}

export default PostList;