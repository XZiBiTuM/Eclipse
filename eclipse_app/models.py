from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import os
from django.core.validators import MinLengthValidator


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class CurrentVersion(models.Model):
    version = models.CharField(max_length=50, verbose_name='Версия')
    current_version = models.CharField(max_length=50, verbose_name='Текущая версия')
    code_name = models.CharField(max_length=128, verbose_name='Кодовое имя')
    architectures = models.CharField(max_length=55, verbose_name='Количество поддерживаемых архитектур')
    packages = models.CharField(max_length=55, verbose_name='Количество пакетов')
    release_date = models.DateField(verbose_name='Дата выпуска')
    support_end_date = models.DateField(verbose_name='Дата окончания поддержки', blank=True, null=True)
    full_support_end_date = models.DateField(verbose_name='Дата окончания длительной поддержки', blank=True, null=True)
    distribution = models.ForeignKey('LinuxDistribution', on_delete=models.CASCADE, related_name='current_versions', verbose_name='Дистрибутив')

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


def validate_square_image(image):
    if image.width != image.height:
        raise ValidationError("Стороны изображения должны быть равны!")


def distro_image_upload_path(instance, filename):
    return f'distros/{instance.name}/{filename}'


class LinuxDistribution(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(validators=[validate_square_image], upload_to=distro_image_upload_path, verbose_name='Изображение')
    short_description = models.TextField(max_length=255, verbose_name='Краткое описание')
    official_website = models.URLField(verbose_name='Официальный сайт')
    release_date = models.DateField(verbose_name='Дата выпуска')
    based_on = models.CharField(max_length=100, verbose_name='Основа для данной ОС')
    description = models.TextField(verbose_name='Описание')
    history = models.TextField(verbose_name='История создания')
    features = models.TextField(verbose_name='Особенности')
    tags = models.ManyToManyField(Tag, related_name='distributions', verbose_name='Теги')

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            img = img.resize((600, 600), Image.Resampling.LANCZOS)

            img.save(img_path)

    class Meta:
        verbose_name = 'Дистрибутив Linux'
        verbose_name_plural = 'Дистрибутивы Linux'


def distro_step_upload_path(instance, filename):
    return f'installation_steps/{instance.distribution.name}/{filename}'


class InstallationStep(models.Model):
    distribution = models.ForeignKey(LinuxDistribution, on_delete=models.CASCADE, related_name='installation_steps',
                                     verbose_name='Дистрибутив')
    step_number = models.IntegerField(verbose_name='Номер шага')
    step_text = models.TextField(verbose_name='Текст шага')
    step_image = models.ImageField(upload_to=distro_step_upload_path, verbose_name='Изображение шага', blank=True)

    def __str__(self):
        return f"{self.distribution.name} - Шаг {self.step_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.step_image:
            img_path = self.step_image.path
            img = Image.open(img_path)

            img = img.resize((800, 450), Image.Resampling.LANCZOS)

            img.save(img_path)

    class Meta:
        verbose_name = 'Шаг установки'
        verbose_name_plural = 'Шаги установки'


def documentation_image_upload_path(instance, filename):
    return f'documentation/{instance.title}/{filename}'


def documentation_pdf_upload_path(instance, filename):
    return f'documentation_pdf/{instance.title}/{filename}'


class Documentation(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название документации')
    content = RichTextField(verbose_name='Контент документации', blank=True, null=True)
    image = models.ImageField(validators=[validate_square_image], upload_to=documentation_image_upload_path, default='/')
    author = models.CharField(max_length=255, verbose_name='Автор', default='Нет')
    year = models.CharField(max_length=16, verbose_name='Год выпуска', default='2001', blank=True, null=True)
    topic = models.CharField(max_length=255, verbose_name='Тема', default='Нет', blank=True, null=True)
    pdf_only = models.BooleanField(verbose_name='True = Только в PDF', default=False)
    pdf = models.FileField(verbose_name='PDF', upload_to=documentation_pdf_upload_path, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            img = img.resize((600, 600), Image.Resampling.LANCZOS)

            img.save(img_path)

    class Meta:
        verbose_name = 'Документация'
        verbose_name_plural = 'Документация'
        unique_together = (('title', 'content'),)


def profile_image_upload_path(instance, filename):
    return f'profile_image/{instance.user.username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='USER')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    profile_image = models.ImageField(
        upload_to=profile_image_upload_path,
        null=True,
        blank=True,
        verbose_name='Изображение профиля',
        validators=[validate_square_image]
    )
    changed = models.BooleanField(verbose_name='Подтверждены изменения', default=False)

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self._original_birth_date = self.birth_date
        self._original_profile_image = self.profile_image
        self._original_first_name = self.user.first_name if self.user else None
        self._original_last_name = self.user.last_name if self.user else None
        self._original_email = self.user.email if self.user else None

    def save(self, *args, **kwargs):
        if (self.birth_date != self._original_birth_date or
                self.profile_image != self._original_profile_image or
                (self.user and (self.user.first_name != self._original_first_name or
                                self.user.last_name != self._original_last_name or
                                self.user.email != self._original_email))):
            self.changed = True

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


def article_image_upload_path(instance, filename):
    return f'article_image/{instance.title}/{filename}'


class ArticleTag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег для статьи'
        verbose_name_plural = 'Теги для статей'


class Article(models.Model):
    title = models.CharField(max_length=55, verbose_name='Название статьи')
    description = models.TextField(max_length=256, validators=[MinLengthValidator(200, message="Кол-во символов: min:200-max:255")], verbose_name='Описание', blank=True, null=True)
    content = RichTextField(verbose_name='Контент статьи')
    image = models.ImageField(validators=[validate_square_image], upload_to=article_image_upload_path, verbose_name='Изображение статьи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан в')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Отредактирован в')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    tags = models.ManyToManyField(ArticleTag, related_name='articles', verbose_name='Теги')
    verification = models.BooleanField(verbose_name='Верификация', default=False)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            img = img.resize((600, 600), Image.Resampling.LANCZOS)

            img.save(img_path)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
