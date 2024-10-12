from rest_framework import generics
from video.models import Category
from video.models import Video
from video.models import Comment
from video.serializers import CategorySerializer
from video.serializers import VideoSerializer
from video.serializers import CommentSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class VideoDetailWithViewCount(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get(self, request, *args, **kwargs):
        video = self.get_object()
        video.view_counts += 1
        video.save()
        return Response({
            'title': video.title,
            'description': video.description,
            'view_count': video.view_counts
        })


class LikeVideoView(APIView):
    def post(self, request, video_id, *args, **kwargs):
        video = get_object_or_404(Video, id=video_id)
        video.like_counts += 1
        video.save()
        return Response({'message': 'Video liked', 'likes': video.like_counts})


class DislikeVideoView(APIView):
    def post(self, request, video_id, *args, **kwargs):
        video = get_object_or_404(Video, id=video_id)
        video.dislike_counts += 1
        video.save()
        return Response({'message': 'Video disliked', 'dislikes': video.dislike_counts})
    

class AddCommentView(CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        video = get_object_or_404(Video, id=self.kwargs['video_id'])
        serializer.save(user=self.request.user, video=video)


class VideoCommentsView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        video = get_object_or_404(Video, id=self.kwargs['video_id'])
        return Comment.objects.filter(video=video)