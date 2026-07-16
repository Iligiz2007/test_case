from django.shortcuts import render
from rest_framework.views import APIView, Response,status
from .serializers import PostSerializers,IdPostSerializers
from rest_framework.permissions import IsAuthenticated
from .models import Post
from django.shortcuts import get_object_or_404
class CreatePost(APIView):
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        if request.user.role == 'user':
            queryset = Post.objects.filter(author=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.role == 'admin':
            queryset = Post.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
class IDUpdateDeletePost(APIView):
    serializer_class = IdPostSerializers
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user.role != 'admin' and post.author != request.user:
            return Response({"detail": "У вас нет прав на редактирование этого поста"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializers(instance=post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user.role != 'admin' and post.author != request.user:
            return Response({"detail": "У вас нет прав на удаление этого поста"}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"detail": "Пост удалён"}, status=status.HTTP_200_OK)
