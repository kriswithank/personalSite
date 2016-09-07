from .models import Author, Chapter, Course, Section, TextBook
from django.contrib import admin
from nested_inline import admin as nested_admin

class SectionInline(nested_admin.NestedStackedInline):
    model = Section
    fields = ['number', 'title', 'content_markdown']
    extra = 0

class ChapterInline(nested_admin.NestedStackedInline):
    model = Chapter
    inlines = [SectionInline]
    extra = 1

class AuthorInline(nested_admin.NestedStackedInline):
    model = Author
    extra = 1

class TextBookInline(nested_admin.NestedStackedInline):
    model = TextBook
    inlines = [AuthorInline, ChapterInline]
    extra = 0

class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [TextBookInline]


admin.site.register(Course, CourseAdmin)
