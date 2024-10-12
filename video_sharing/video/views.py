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

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    video.view_count += 1
    video.save()

    return JsonResponse({
        'title': video.title,
        'description': video.description,
        'view_count': video.view_count
    })



@require_POST
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.likes += 1
    video.save()

    return JsonResponse({'message': 'Video liked', 'likes': video.likes})

@require_POST
def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.dislikes += 1
    video.save()

    return JsonResponse({'message': 'Video disliked', 'dislikes': video.dislikes})


@require_POST
def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comment_text = request.POST.get('text')

    if comment_text:
        comment = Comment.objects.create(
            video=video,
            user=request.user,
            text=comment_text
        )
        return JsonResponse({'message': 'Comment added successfully'})
    return JsonResponse({'error': 'Invalid comment'}, status=400)


def video_comments(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments = video.comments.all().values('user__username', 'text', 'created_at')

    return JsonResponse(list(comments), safe=False)