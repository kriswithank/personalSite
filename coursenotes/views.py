from .models import Author, Chapter, Course, TextBook
from django.shortcuts import render

def index(request):
    context = {
        'courses': Course.objects.all()
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
