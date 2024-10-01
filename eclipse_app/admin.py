from xml.dom.minidom import Document
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from .models import *


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

    formfield_overrides = {
        models.TextField: {'widget': RichTextField},
    }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    filter_horizontal = ('tags',)

    formfield_overrides = {
        RichTextField: {'widget': CKEditorWidget()},
    }


class InstallationStepInline(admin.TabularInline):
    model = InstallationStep
    extra = 1


class CurrentVersionInline(admin.TabularInline):
    model = CurrentVersion
    extra = 1


class LinuxDistributionAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date')
    inlines = [InstallationStepInline, CurrentVersionInline]
    search_fields = ['name', 'tags__name']
    filter_horizontal = ('tags',)


admin.site.register(LinuxDistribution, LinuxDistributionAdmin)
admin.site.register(Tag)
admin.site.register(CurrentVersion)
admin.site.register(Profile)
admin.site.register(ArticleTag)
