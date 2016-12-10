from django.db import models
import markdown
import pypandoc

class Course(models.Model):
    """
    Represents a course that has been taken.

    Attributes:
        name - The given name of the course.
        dept_num - The 4 digit code that corresponds to the department which offers
                   the course.
        course_num - The corresponding course number of the course.
        year - The year the course was taken. 1 for first year, 2 for second year, ...
        semester - The semester in which the course was taken. 1 for fall, 2 for
                   spring, 3 for summer. Preferably, use the provided constants:
                   SEM_FALL, SEM_SPRING, SEM_SUMMER.
        instructor - Person who taught the class.
    """
    name = models.CharField(max_length=500)
    dept_num = models.CharField(max_length=4)
    course_num = models.CharField(max_length=50)
    year = models.SmallIntegerField()
    semester = models.SmallIntegerField()
    instructor = models.CharField(max_length=1000)

    SEM_FALL = 1
    SEM_SPRING = 2
    SEM_SUMMER = 3

    def semester_name(self):
        """
        Returns the string name of the objects semester. Throwns and error if the
        semester is not one of SEM_FALL, SEM_SPRING, SEM_SUMMER.
        """
        if (self.semester == self.SEM_FALL):
            return "Fall"
        if (self.semester == self.SEM_SPRING):
            return "Spring"
        if (self.semester == self.SEM_SUMMER):
            return "Summer"

    def __str__(self):
        return self.name



class TextBook(models.Model):
    """
    Represents a text book that was used in a course.

    Attributes:
        title
        course - The course for which the book was used.
    """
    title = models.CharField(max_length=1000)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Author(models.Model):
    """
    Represents a single author of a TextBook, a book can have multiple authors.

    Attributes:
        name
        book - The TextBook to which the author is assosiated.
    """
    name = models.CharField(max_length=1000)
    book = models.ForeignKey('Textbook', on_delete=models.CASCADE)

    def __str__(self):
        return self.name




class Chapter(models.Model):
    """
    Represents a chapter that was covered in a TextBook.

    Attributes:
        parent_book - The TextBook to which the chapter is assosiated.
        number - The number of the chapter.
        title - The chapter's title.
    """
    parent_book = models.ForeignKey('TextBook', on_delete=models.CASCADE)
    number = models.SmallIntegerField()
    title = models.CharField(max_length=500)

    def __str__(self):
        return self.title



class Section(models.Model):
    """
    Represents a section within a Chapter of a TextBook.

    Attributes:
        parent_chapter - The Chapter to which the section belongs.
        number - The section's number.
        title - The *optional* title of the section.
        content_markdown - The markdown that is the section's notes. This should be
                           the only thing that the user ever edits.
        content_html - The safe html that is generated from the user-defined
                       content_markdown.
    """
    parent_chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    number = models.SmallIntegerField()
    title = models.CharField(max_length=500, blank=True)
    content_markdown = models.TextField()
    content_html = models.TextField()

    def save(self):

        # Append image refs to markdown
        image_refs = ""
        for image in self.sectionimage_set.all():
            image_refs += '\n[{0}]: {1}'.format(image.name, image.image.url)
        markdown_with_images = '{0}\n{1}'.format(self.content_markdown, image_refs)

        self.content_html = pypandoc.convert(markdown_with_images, format='md',
                    to='html', extra_args=['--mathjax'])

        super(Section, self).save()

    def __str__(self):
        return self.title


class SectionImage(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="notes/images")
    parent = models.ForeignKey('Section', on_delete=models.CASCADE)
