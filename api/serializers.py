from feed.models import Post
from feed.models import Comment 
from users.models import Profile 
from rest_framework import serializers



class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = 'user.username', read_only = True)
    class Meta:
        model = Profile
        fields = [
                  'id',
                  'user', 
                  'image', 
                  'bio',
                  'url'
                  ]




class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = 'user.username', read_only = True)
    class Meta:
        model = Comment
        fields = [
            'user', 
            'comment', 
            'comment_date'
            ]

class PostSerializer(serializers.HyperlinkedModelSerializer):
    
    author = serializers.ReadOnlyField(source = 'author.username')
    # user = serializers.CharField(source = 'user.username', read_only = True)
    url = serializers.HyperlinkedIdentityField(
        view_name = 'post-detail',
       )
    user = ProfileSerializer(read_only = True)
    comments = CommentSerializer(many = True, read_only = True)
    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'description',
            'picture', 
            'date_posted', 
            'comments',
            'url', 
            'author'
             ]