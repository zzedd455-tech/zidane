from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, FileResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Course, Video, Post, StudyFile

def home(request):
    """Home page view"""
    recent_courses = Course.objects.filter(is_active=True)[:6]
    recent_posts = Post.objects.filter(is_published=True)[:3]
    recent_videos = Video.objects.filter(is_active=True)[:6]
    
    context = {
        'recent_courses': recent_courses,
        'recent_posts': recent_posts,
        'recent_videos': recent_videos,
    }
    return render(request, 'core/home.html', context)

def course_list(request):
    """List all courses"""
    courses = Course.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(courses, 9)  # Show 9 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'core/course_list.html', context)

def course_detail(request, pk):
    """Course detail view"""
    course = get_object_or_404(Course, pk=pk, is_active=True)
    videos = course.videos.filter(is_active=True)
    files = course.files.all()
    
    context = {
        'course': course,
        'videos': videos,
        'files': files,
    }
    return render(request, 'core/course_detail.html', context)

def video_list(request):
    """List all videos"""
    videos = Video.objects.filter(is_active=True)
    
    # Filter by course
    course_id = request.GET.get('course')
    if course_id:
        videos = videos.filter(course_id=course_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        videos = videos.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(videos, 12)  # Show 12 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all courses for filter dropdown
    courses = Course.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'courses': courses,
        'search_query': search_query,
        'selected_course': course_id,
    }
    return render(request, 'core/video_list.html', context)

def video_detail(request, pk):
    """Video detail view"""
    video = get_object_or_404(Video, pk=pk, is_active=True)

    # Increment view count
    video.views_count += 1
    video.save()

    # تحويل رابط يوتيوب إلى embed إذا كان الرابط من يوتيوب
    video_url = video.video_url
    if "youtube.com/watch?v=" in video_url:
        import re
        match = re.search(r"v=([\w-]+)", video_url)
        if match:
            video_url = f"https://www.youtube.com/embed/{match.group(1)}"
    elif "youtu.be/" in video_url:
        import re
        match = re.search(r"youtu.be/([\w-]+)", video_url)
        if match:
            video_url = f"https://www.youtube.com/embed/{match.group(1)}"

    # Get related videos from the same course
    related_videos = Video.objects.filter(
        course=video.course,
        is_active=True
    ).exclude(pk=pk)[:4]

    context = {
        'video': video,
        'related_videos': related_videos,
        'video_url': video_url,
    }
    return render(request, 'core/video_detail.html', context)

def post_list(request):
    """List all posts"""
    posts = Post.objects.filter(is_published=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'core/post_list.html', context)

def post_detail(request, pk):
    """Post detail view"""
    post = get_object_or_404(Post, pk=pk, is_published=True)
    
    # Increment view count
    post.views_count += 1
    post.save()
    
    # Get recent posts for sidebar
    recent_posts = Post.objects.filter(is_published=True).exclude(pk=pk)[:5]
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
    }
    return render(request, 'core/post_detail.html', context)

def file_download(request, pk):
    """Handle file downloads"""
    study_file = get_object_or_404(StudyFile, pk=pk)

    # Ensure file exists on storage
    file_field = study_file.file_upload
    if not file_field:
        raise Http404("File not found")

    # Increment download count
    study_file.download_count += 1
    study_file.save(update_fields=['download_count'])

    # Stream the file
    import os
    import mimetypes
    try:
        # Build a user-friendly download name preserving extension
        file_name = os.path.basename(file_field.name)
        ext = os.path.splitext(file_name)[1]
        download_name = f"{study_file.title}{ext}"

        # Guess content type
        content_type, _ = mimetypes.guess_type(download_name)
        content_type = content_type or 'application/octet-stream'

        # Open from storage (works with local and remote storages)
        file_field.open('rb')
        return FileResponse(file_field, as_attachment=True, filename=download_name, content_type=content_type)
    except FileNotFoundError:
        raise Http404("File not found")

def search(request):
    """Global search functionality"""
    query = request.GET.get('q', '')
    results = {
        'courses': [],
        'videos': [],
        'posts': [],
        'files': [],
    }
    
    if query:
        # Search courses
        results['courses'] = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_active=True
        )[:5]
        
        # Search videos
        results['videos'] = Video.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_active=True
        )[:5]
        
        # Search posts
        results['posts'] = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        )[:5]
        
        # Search files
        results['files'] = StudyFile.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:5]
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'core/search_results.html', context)
