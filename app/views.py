from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import AdminPermission
from .serializers import *
from rest_framework import status



class Overview(APIView):
    '''
    Total number of snippet and list all available snippets
    '''
    
    permission_classes = [AdminPermission]
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        snippet_list = Snippet.objects.filter(created_user=user)
        snippet = OverviewSerializer(snippet_list,many=True)
        result = []
        for item in snippet.data:
            result.append({
                'title':item.get('title'),
                'text':item.get('text'),
                'timestamp':item.get('timestamp'),
                'created_user':item.get('created_user'),
                'url':'http://127.0.0.1:8000/api/snippet/{}/'.format(item.get('id'))
            })
        return Response({'count':f"{len(snippet_list)}",'snippet':result},status=status.HTTP_200_OK)
    
    
    
class Create(APIView):
    '''
    API to collect the snippet information and save the data to DB.
    '''
    
    permission_classes = [AdminPermission]
    
    def post(self, request, *args, **kwargs):
        snippet_serializer = SnippetSerializer(data=request.data)
        if snippet_serializer.is_valid(raise_exception=True):
            user_enterd_title = snippet_serializer.validated_data.get('title')
            tag = Tag.objects.get_or_create(title=user_enterd_title)
            user = User.objects.get(username=request.user)
            snippet_serializer.save(tag=tag[0],created_user=user)
            result = [{
                'status':'Success',
                'message':'snippet created successfully',
                'snippet':snippet_serializer.data
            }]
            return Response(result,status=status.HTTP_201_CREATED)
        return Response({'status':"error",'message':'snippet is not created','required_field':['titile','text']},status=status.HTTP_401_UNAUTHORIZED)
    
    

class Details(APIView):
    '''
    API display the snippet title, content, and timestamp information.
    '''
    
    permission_classes = [AdminPermission]
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        try:
            snippet_details = Snippet.objects.get(id=user_id)
        except Exception:
            return Response({'status':'error','message':'snippet id is not valid'},status=status.HTTP_404_NOT_FOUND)
        snippet_detail_serializer = SnippetDetailSerializer(snippet_details)
        return Response({"status":"OK","message":'successfully get details','snippet':snippet_detail_serializer.data})



class Update(APIView):
    '''
    API to update individual items.
    '''
    
    permission_classes = [AdminPermission]
    
    def put(self, request, *args, **kwargs):
        snippet_id = kwargs.get('snippetid')
        try:
            database_snippet = Snippet.objects.get(id = snippet_id)
        except Exception:
            return Response({'error': 'Snippet not found.'}, status=status.HTTP_404_NOT_FOUND)
        snippet_serializer = SnippetSerializer(database_snippet, data=request.data)
        if snippet_serializer.is_valid(raise_exception=True):
            snippet_serializer.save()
            result = [{
                'status':'Success',
                'message':'snippet update successfully',
                'snippet':snippet_serializer.data
            }]
            return Response(result,status=status.HTTP_200_OK)
        return Response({'status':'error','message':'snippet update faild','required_field':['title','text']},status=status.HTTP_424_FAILED_DEPENDENCY)
    


class Delete(APIView):
    '''
    API to delete selected items.
    '''
    
    permission_classes = [AdminPermission]
    
    def delete(self, request, *args, **kwargs):
        snippet_id = kwargs.get('snippetid')
        try:
            database_snippet = Snippet.objects.get(id = snippet_id)
        except Exception:
            return Response({'status':'error','message': 'Snippet id not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            database_snippet.delete()
            return Response({'status':'success','message':'snippet delete successfully'})
        
        

class TagList(APIView):
    '''
    API to list tags
    '''
    
    permission_classes = [AdminPermission]
    
    def get(self, request, *args, **kwargs):
        tag_list = Tag.objects.all()
        tag_list_serializer = TagListSerializer(tag_list,many=True)
        return Response({'status':'success','message':'list all Tags','tag':tag_list_serializer.data})
        
        

class TagDetails(APIView):
    '''
    API to return snippets linked to the selected tag.
    '''
    
    permission_classes = [AdminPermission]
    
    def get(self, request, *args, **kwargs):
        '''
        get all tag details
        '''
        tag_id = kwargs.get('tagid')
        try:
            tag_object = Tag.objects.get(id=tag_id)
        except Exception:
            return Response({'status':'error','message':'tag id is not valid'},status=status.HTTP_404_NOT_FOUND)
        else:
            snippet_objects = Snippet.objects.filter(tag=tag_object)
            snippet_serializer = SnippetDetailSerializer(snippet_objects, many=True)
            return Response({'status':'success','message':'Tag Details ','snippets':snippet_serializer.data},status=status.HTTP_200_OK)
    
    
    def put(self, request, *args, **kwargs):
        '''
        update tag details
        '''
        tag_id = kwargs.get('tagid')
        try:
            tag_object = Tag.objects.get(id=tag_id)
        except Exception:
            return Response({'status':'error','message':'tag id is not valid'},status=status.HTTP_404_NOT_FOUND)
        else:
            tag_serializer = TagSerializer(tag_object, data=request.data)
            if tag_serializer.is_valid(raise_exception=True):
                tag_serializer.save()
                return Response({'status':'success','message':'tag successfully updated'},status=status.HTTP_200_OK)
            return Response({'status':'error','message':'tag update faild','required_field':['title']},status=status.HTTP_204_NO_CONTENT)


    def delete(self, request, *args, **kwargs):
        '''
        delete tag details
        '''
        tag_id = kwargs.get('tagid')
        try:
            tag_object = Tag.objects.get(id=tag_id)
        except Exception:
            return Response({'status':'error','message':'tag id is not valid'},status=status.HTTP_404_NOT_FOUND)
        else:
            tag_object.delete()
            return Response({'status':'success','message':'tag is successfully deleted'},status=status.HTTP_200_OK)
        


class ShowAllApiDoc(APIView):
    
    def get(self, request, *args, **kwargs):
        
        result = [
            ('http://127.0.0.1:8000/api/snippets/','overview api'),
            ('http://127.0.0.1:8000/api/snippet/<int:id>/','details api'),
            ('http://127.0.0.1:8000/api/snippet/create/','create api'),
            ('http://127.0.0.1:8000/api/snippet/<int:snippetid>/update/','update api'),
            ('http://127.0.0.1:8000/api/snippet/<int:snippetid>/delete/','delete api'),
            ('http://127.0.0.1:8000/api/tag/','tag list api'),
            ('http://127.0.0.1:8000/api/tag/<int:tagid>/' ,'tag details api'),
        ]
        return Response({'status':'success','message':'show all api list','all api list':result},status=status.HTTP_200_OK)
        
        
        
