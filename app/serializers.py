from rest_framework import serializers
from .models import *




class SnippetSerializer(serializers.ModelSerializer):
    ''' 
    Snippet Serializer
    '''
    class Meta:
        model = Snippet
        fields = ['id','title','text']

    
    
    
class OverviewSerializer(serializers.ModelSerializer):
    """
    Implement an API endpoint to retrieve the total count of snippets and list all available snippet
    """
    
    class Meta:
        model = Snippet
        fields = ['id','title','text','timestamp','created_user']
        





class SnippetDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Snippet
        fields = ['id','title','text','timestamp','created_user']






class TagListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['id','title']
        
        
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']