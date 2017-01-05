from .models import Author, Chapter, Course, TextBook
from django.shortcuts import render

def index(request):

    courses_by_year = {}
    for elem in Course.objects.order_by('year', 'semester', 'course_num'):
        when_taken = "{0} Year {1}".format(elem.semester_name(), elem.year)
        if when_taken in courses_by_year:
            courses_by_year[when_taken].append(elem)
        else:
            courses_by_year[when_taken] = [elem, ]

    context = {
        'courses_by_year': courses_by_year,
    }
    return render(request, 'coursenotes/index.html', context)



def course_index(request, course_slug):
    context = {
        'course': Course.objects.get(slug=course_slug)
    }
    return render(request, 'coursenotes/course_index.html', context)



def chapter_view(request, course_slug, ch_num):
    context = {
        'ch': Course.objects.get(slug=course_slug).chapter_set.get(number=ch_num)
    }
    return render(request, 'coursenotes/chapter_view.html', context)



def course_info_page(request, course_slug):
    context = {
        'course': Course.objects.get(slug=course_slug)
    }
    return render(request, 'coursenotes/course_info.html', context)
