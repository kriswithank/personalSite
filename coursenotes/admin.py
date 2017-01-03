from .models import Author, Chapter, Course, Section, SectionImage, TextBook
from django import forms
from django.db import models
from django.contrib import admin
from nested_inline import admin as nested_admin
from pagedown.widgets import AdminPagedownWidget

class AuthorInline(nested_admin.NestedStackedInline):
    model = Author
    extra = 1

class TextBookInline(nested_admin.NestedStackedInline):
    model = TextBook
    inlines = (AuthorInline,)
    extra = 0

class CourseAdmin(nested_admin.NestedModelAdmin):
    fields = ('name', ('dept_num', 'course_num'), ('year', 'semester'), 'instructor',)
    inlines = (TextBookInline,)

class SectionImageInline(nested_admin.NestedStackedInline):
    fields = (('name', 'image'),)
    model = SectionImage
    extra = 0

class SectionInline(nested_admin.NestedStackedInline):
    model = Section
    fields = (('number', 'title'), 'content_markdown')
    inlines = (SectionImageInline,)
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget(show_preview=False)},
    }

class ChapterAdmin(nested_admin.NestedModelAdmin):
    fields = ('course', ('number', 'title'),)
    inlines = (SectionInline,)
    list_display = ('course', 'number', 'title',)
    list_filter = ('course',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
