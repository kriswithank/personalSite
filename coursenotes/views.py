from .models import Author, Chapter, Course, TextBook
from django.db.models import Max
from django.shortcuts import render



def get_base_context():
    max_year = Course.objects.all().aggregate(Max('year'))['year__max']
    max_sem = Course.objects.filter(year=max_year).aggregate(Max('semester'))['semester__max']
    return {
        'recent_courses': Course.objects.filter(year=max_year, semester=max_sem)
    }



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
    context.update(get_base_context())
    return render(request, 'coursenotes/index.html', context)



def course_index(request, course_slug):
    context = {
        'course': Course.objects.get(slug=course_slug),
    }
    context.update(get_base_context())
    return render(request, 'coursenotes/course_index.html', context)



def chapter_view(request, course_slug, ch_num):
    context = {
        'ch': Course.objects.get(slug=course_slug).chapter_set.get(number=ch_num),
    }
    context.update(get_base_context())
    return render(request, 'coursenotes/chapter_view.html', context)



def course_info_page(request, course_slug):
    context = {
        'course': Course.objects.get(slug=course_slug),
    }
    context.update(get_base_context())
    return render(request, 'coursenotes/course_info.html', context)
