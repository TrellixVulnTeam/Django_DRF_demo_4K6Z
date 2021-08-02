from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

'''
手动序列化
'''

# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data) # 序列化操作
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)



# @csrf_exempt
# def snippet_list(request):
#     """
#     列出所有的code snippet，或创建一个新的snippet。
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JSONResponse(serializer.data)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=201)
#         return JSONResponse(serializer.errors, status=400)


# @csrf_exempt
# def snippet_detail(request, pk):
#     """
#     获取，更新或删除一个 code snippet。
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JSONResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)


'''
使用api_view封装
'''
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     """
#     列出所有的snippets，或者创建一个新的snippet。
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     """
#     获取，更新或删除一个snippet实例。
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

'''
基于类的视图重写（DRY）
'''
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SnippetList(APIView):
    """
    列出所有的snippets或者创建一个新的snippet。
    """
    @swagger_auto_schema(
     operation_summary='我是摘要',
     operation_description='我是說明',
)
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
 
#     @swagger_auto_schema(
#     operation_summary='我是摘要',
#     operation_description='我是說明',
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=['data'],
#         properties={
#             'data': openapi.Schema(type=openapi.TYPE_STRING),
#             'task_id': openapi.Schema(type=openapi.TYPE_STRING),
#         },
#     ),
#     responses={
#         status.HTTP_200_OK: openapi.Response(
#             '{"message": "accept!", success": True}'),
#         status.HTTP_400_BAD_REQUEST: openapi.Response('{"success": False, "message": "<error message>"}'),
#     },
# )
    @swagger_auto_schema(
        operation_description="Task Service Create API OSG(AppTaskService/13300)",
        tags=["TaskService"],
        operation_id='AppTaskService/13300',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data', 'type', 'url'],
            properties={
                'data': openapi.Schema(type=openapi.TYPE_OBJECT,
                                       description="input内容，任务执行所需的数据"),
                'type': openapi.Schema(type=openapi.TYPE_STRING,
                                       description="操作类型，例如：Group删除、Group扩容、Group禁用 等", ),
                'url': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING,
                                                                                    description="回调url"
                                                                                    ),
                                      description="回调地址列表"),
            },
        ),
        responses={
            status.HTTP_202_ACCEPTED: openapi.Response(
                '''{
                        'result': True,
                        'code': 0,
                        'message': 'Done',
                            'data': {
                                'task_id': <task.id>
                            }
                }'''
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response('{"success": False, "message": "<error message>"}'),
        },
    )


    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SnippetDetail(APIView):
    """
    检索，更新或删除一个snippet示例。
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
mixins
'''

# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import mixins
# from rest_framework import generics

# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


'''
mixed-in
'''
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import generics


# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
