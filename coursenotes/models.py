from django.db import models
from django.utils.text import slugify
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
    slug = models.SlugField(unique=True)

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


    def generate_slug(self):
        """
        Generates a unique slug for the object does **not** save the object. If a
        course already exists with that same slug, it should append a unque slug
        modifer to the end of the slug that is 1 more than the largest modifer already
        in existance.

        Ex.
            If CSCI-2011 and CSCI-2011-2 and CSCI-2011-4 already exist, then the unique
            slug generated will be CSCI-2011-5.

        Assumes that all slugs share the same structure:
            <dept>-<course_num>   OR   <dept>-<course_num>-<slug_unique_modifier>
        where the unique slug modifier is a positive integer. This is important because
        this is expolited when generating a unique slug.
        """
        new_slug = slugify(self.dept_num) + '-' + slugify(self.course_num)

        # Ensure uniqueness.
        similar_slugs = [course.slug for course in Course.objects.filter(slug__startswith=new_slug).all()]
        slug_modifiers = [slug.split(new_slug)[1][1:] for slug in similar_slugs]
        # Repalce blank with 0 and cast other modifers to int.
        slug_modifiers = [1 if modifier == '' else int(modifier) for modifier in slug_modifiers]

        if len(slug_modifiers) <= 0:
            return new_slug
        else:
            return new_slug + '-' + str(max(slug_modifiers)+1)


    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = self.generate_slug()
        super(Course, self).save(*args, **kwargs)


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
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
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

    GRAPH_START_TAG = '<graph>'
    GRAPH_END_TAG = '</graph>'

    def get_markdown_with_image_refs(self, markdown):
        """
        Returns a string of markdown with image urls appended to end.

        Argument 'markdown' is not modified.

        Takes advantatge of the syntax in markdown to append the urls of named images
        at the end of a file in order to make inclusion of images easier.
        """
        image_refs = ""

        for image in self.sectionimage_set.all():
            image_refs += '\n[{0}]: {1}'.format(image.name, image.image.url)

        return '{0}\n{1}'.format(markdown, image_refs) # Append image_refs to markdown.

    def get_markdown_graphviz_sub(self, markdown):
        """
        Substitutes graphviz start and end tags with appropriate, working tags and
        returns result.

        Argument 'markdown' is not modified.
        """
        working_start_tag = "<img src='http://g.gravizo.com/g?"
        working_end_tag = "'/>"

        copy = markdown.replace(self.GRAPH_START_TAG, working_start_tag)
        copy = copy.replace(self.GRAPH_END_TAG, working_end_tag)

        return copy

    def save(self):

        processed_markdown = self.get_markdown_with_image_refs(self.content_markdown)
        processed_markdown = self.get_markdown_graphviz_sub(processed_markdown)

        self.content_html = pypandoc.convert(processed_markdown, format='md',
                    to='html', extra_args=['--mathjax'])

        super(Section, self).save()

    def __str__(self):
        return self.title


class SectionImage(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="notes/images")
    parent = models.ForeignKey('Section', on_delete=models.CASCADE)
