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



def course_index(request, course_id):
    context = {
        'course': Course.objects.get(id=course_id)
    }
    return render(request, 'coursenotes/course_index.html', context)



def chapter_view(request, course_id, ch_id):
    context = {
        'ch': Course.objects.get(id=course_id).chapter_set.get(number=ch_id)
    }
    return render(request, 'coursenotes/chapter_view.html', context)
