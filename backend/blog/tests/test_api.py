from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from mixer.backend.django import mixer

from blog.models import BlogPost
from blog.serializers import BlogPostShortSerializer, BlogPostLongSerializer


BLOG_POSTS_URL = reverse('blog:post-list')


def get_detail_url(pk):
    return reverse('blog:post-detail', kwargs={'pk': pk})


class PublicBlogPostApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_posts(self):
        mixer.cycle(2).blend(BlogPost)
        resp = self.client.get(BLOG_POSTS_URL)

        posts = BlogPost.objects.all().order_by('id')
        serializer = BlogPostShortSerializer(posts, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_detailed_post(self):
        post_model = mixer.blend(BlogPost)
        post_url = get_detail_url(post_model.id)
        resp = self.client.get(post_url)

        post = BlogPost.objects.get(id=post_model.id)
        serializer = BlogPostLongSerializer(post)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_create_post_unauthorized(self):
        payload = {
            'title': 'test',
            'content': 'test content'
        }
        resp = self.client.post(BLOG_POSTS_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(BlogPost.objects.exists())

    def test_update_post_unauthorized(self):
        authorized_user = mixer.blend(get_user_model())
        post = BlogPost.objects.create(title='test',
                                       content='test',
                                       author=authorized_user)

        payload = {
            'title': 'test1',
            'content': 'test1 content'
        }
        blog_update_url = get_detail_url(post.id)
        resp = self.client.put(blog_update_url, payload)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        for field, value in payload.items():
            self.assertNotEqual(value, getattr(post, field))

    def test_delete_post_unauthorized(self):
        post = mixer.blend(BlogPost)

        blog_delete_url = get_detail_url(post.id)
        resp = self.client.delete(blog_delete_url)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(BlogPost.objects.exists())


class PrivateBlogPostApiTest(TestCase):

    def setUp(self):
        self.user = mixer.blend(get_user_model())
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_post_authorized(self):
        payload = {
            'title': 'test',
            'content': 'test content'
        }
        resp = self.client.post(BLOG_POSTS_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        post = BlogPost.objects.get(id=resp.data.get('id'))
        for field, value in payload.items():
            self.assertEqual(value, getattr(post, field))

    def test_update_post_authorized(self):
        post = BlogPost.objects.create(title='test',
                                       content='test',
                                       author=self.user)

        payload = {
            'title': 'test1',
            'content': 'test1 content'
        }
        blog_update_url = get_detail_url(post.id)
        resp = self.client.put(blog_update_url, payload)
        post.refresh_from_db()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field, value in payload.items():
            self.assertEqual(value, getattr(post, field))

    def test_delete_post_unauthorized(self):
        post = mixer.blend(BlogPost)

        blog_delete_url = get_detail_url(post.id)
        resp = self.client.delete(blog_delete_url)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BlogPost.objects.exists())
