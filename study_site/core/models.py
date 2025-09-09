from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان المادة")
    description = models.TextField(verbose_name="وصف المادة")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, verbose_name="صورة المادة")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="نشط")

    class Meta:
        verbose_name = "مادة دراسية"
        verbose_name_plural = "المواد الدراسية"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})

class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الفيديو")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="videos", verbose_name="المادة")
    video_url = models.URLField(verbose_name="رابط الفيديو")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True, verbose_name="صورة مصغرة")
    duration = models.CharField(max_length=20, blank=True, null=True, verbose_name="مدة الفيديو")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="المؤلف")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    views_count = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")

    class Meta:
        verbose_name = "فيديو"
        verbose_name_plural = "الفيديوهات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'pk': self.pk})

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان المنشور")
    content = models.TextField(verbose_name="المحتوى")
    excerpt = models.TextField(max_length=300, blank=True, verbose_name="مقتطف")
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name="صورة المنشور")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="المؤلف")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name="منشور")
    views_count = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")

    class Meta:
        verbose_name = "منشور"
        verbose_name_plural = "المنشورات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = self.content[:300] + "..." if len(self.content) > 300 else self.content
        super().save(*args, **kwargs)

class StudyFile(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('doc', 'Word Document'),
        ('ppt', 'PowerPoint'),
        ('xls', 'Excel'),
        ('other', 'أخرى'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان الملف")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="files", verbose_name="المادة")
    file_upload = models.FileField(upload_to='study_files/', verbose_name="الملف المرفق")
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='pdf', verbose_name="نوع الملف")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="المؤلف")
    created_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0, verbose_name="عدد التحميلات")
    file_size = models.PositiveIntegerField(blank=True, null=True, verbose_name="حجم الملف (بايت)")

    class Meta:
        verbose_name = "ملف دراسي"
        verbose_name_plural = "الملفات الدراسية"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('file_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.file_upload and not self.file_size:
            self.file_size = self.file_upload.size
        super().save(*args, **kwargs)

    def get_file_size_display(self):
        if self.file_size:
            if self.file_size < 1024:
                return f"{self.file_size} بايت"
            elif self.file_size < 1024 * 1024:
                return f"{self.file_size / 1024:.1f} كيلوبايت"
            else:
                return f"{self.file_size / (1024 * 1024):.1f} ميجابايت"
        return "غير محدد"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    bio = models.TextField(max_length=500, blank=True, verbose_name="نبذة شخصية")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="الصورة الشخصية")
    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم الهاتف")
    website = models.URLField(blank=True, verbose_name="الموقع الشخصي")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ملف شخصي"
        verbose_name_plural = "الملفات الشخصية"

    def __str__(self):
        return f"ملف {self.user.username}"
