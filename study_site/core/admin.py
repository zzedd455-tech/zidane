from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Course, Video, Post, StudyFile, UserProfile

# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'الملف الشخصي'

# Extend User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('title', 'description', 'image', 'is_active')
        }),
        ('معلومات إضافية', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'author', 'views_count', 'is_active', 'created_at')
    list_filter = ('course', 'is_active', 'created_at', 'author')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'views_count')
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('title', 'course', 'video_url', 'description')
        }),
        ('إعدادات إضافية', {
            'fields': ('thumbnail', 'duration', 'author', 'is_active')
        }),
        ('إحصائيات', {
            'fields': ('views_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'views_count', 'created_at')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content', 'excerpt')
    readonly_fields = ('created_at', 'updated_at', 'views_count')
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('title', 'content', 'excerpt', 'image')
        }),
        ('إعدادات النشر', {
            'fields': ('author', 'is_published')
        }),
        ('إحصائيات', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(StudyFile)
class StudyFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'file_type', 'author', 'download_count', 'get_file_size_display', 'created_at')
    list_filter = ('course', 'file_type', 'created_at', 'author')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'download_count', 'file_size')
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('title', 'course', 'file_upload', 'file_type', 'description')
        }),
        ('إعدادات إضافية', {
            'fields': ('author',)
        }),
        ('إحصائيات', {
            'fields': ('download_count', 'file_size', 'created_at'),
            'classes': ('collapse',)
        }),
    )

# Customize admin site headers
admin.site.site_header = "لوحة تحكم الموقع التعليمي"
admin.site.site_title = "إدارة الموقع"
admin.site.index_title = "مرحباً بك في لوحة التحكم"
