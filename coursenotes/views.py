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



def book_index(request, book_id):
    context = {
        'book': TextBook.objects.get(id=book_id)
    }
    return render(request, 'coursenotes/book_index.html', context)



def chapter_view(request, book_id, ch_id):
    context = {
        'ch': TextBook.objects.get(id=book_id).chapter_set.get(number=ch_id)
    }
    return render(request, 'coursenotes/chapter_view.html', context)
