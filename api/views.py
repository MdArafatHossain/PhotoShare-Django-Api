from django.shortcuts import render
from django.http import HttpResponse, Http404
from feed.models import Post 
from feed.models import Comment
from users.models import Profile
from .serializers import ProfileSerializer
from .serializers import PostSerializer
from .serializers import CommentSerializer
from rest_framework.decorators import api_view

from rest_framework import status, permissions
from rest_framework.views import APIView 
from rest_framework.response import Response


class ApiList(APIView):
    def get(self, request):
        api = {"profiles": "http://127.0.0.1:8000/api/profiles",
               "posts"   : "http://127.0.0.1:8000/api/posts"}
        return Response(api)


class PostList (APIView):
    'List all post or create new post'
    #def get is to get all of the posts
    permission_classes = [permissions.IsAuthenticated]
    def get (self, request):
        post = Post.objects.all()
        serializer = PostSerializer(post, many = True, context = {'request': request})
        return Response(serializer.data)
    
    #def post to create a new post 
    def post (self,request):
        serializer = PostSerializer(data=request.data, context = {'request': request})#its gonna request the data from our post
        if serializer.is_valid():
            blank = " "
            serializer.save(user = self.request.user, picture = blank)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)     


class PostDetail(APIView):
    'Read, update or delete an individual '
    permission_classes = [permissions.IsAuthenticated]
    #this is the first function to get the post 
    def get_post(self,pk):
        try:
            return Post.objects.get(pk = pk)
        except:
            raise Http404

    def get(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)
    
    #this is to edit our posts 
    def put (self,request, pk):
        permission_classes = [permissions.IsAuthenticated]
        user = request.user
        post = self.get_post(pk)
        if post.user != user:
            return Response({'response':"You dont have access to edit this post"})
        serializer = PostSerializer(post, data= request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)
    
    def delete (self, request, pk):
        permission_classes = [permissions.IsAuthenticated]
        user = request.user
        post = self.get_post(pk)
        if post.user != user:
            return Response({'response':"You dont have access to delete this post"})
        post.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    
class ProfileList (APIView):
    'List all post or create new post'
    #def get is to get all of the posts
    permission_classes = [permissions.IsAuthenticated]
    def get (self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many = True, context = {'request': request})
        return Response(serializer.data)
    
    #def post to create a new post 
    def post (self,request):
        serializer = ProfileSerializer(data=request.data)#its gonna request the data from our post
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 


class ProfileDetail(APIView):
     
    permission_classes = [permissions.IsAuthenticated]
    #this is the first function to get the profile
    def get_post(self, pk):
        try:
            return Profile.objects.get(pk = pk)
        except:
            raise Http404

    def get(self, request, pk):
        profile = self.get_post(pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    
    #this is to edit our profile
    
    def put (self,request, pk):
        permission_classes = [permissions.IsAuthenticated]
        user = request.user
        profile = self.get_post(pk)
        if profile.user != user:
            return Response({'response':"You dont have access to edit this profile"})
        serializer = ProfileSerializer(profile, data= request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)


class CommentList (APIView):
    #def get is to get all of the comment
    permission_classes = [permissions.IsAuthenticated]
    def get (self, request, post_id):
        comments = Comment.objects.filter(post_id = post_id)
        serializer = CommentSerializer(comments, many = True, context = {'request': request})
        return Response(serializer.data)
    
    #def post to create a new comment
    def post (self,request,post_id):
        serializer = CommentSerializer(data=request.data)#its gonna request the data from our comments
        if serializer.is_valid():
            serializer.save(user = self.request.user,post_id = post_id)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)     

