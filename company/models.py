from django.db import models
from django import forms
from django.core.validators import RegexValidator

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, MultiFieldPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index

class HomePage(Page):
    introduction = RichTextField(blank=False)

    content_panels = Page.content_panels + [
        FieldPanel('introduction')
    ]
    
"""
Contact Page
"""
class ContactPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('contacts', label='Contacts')
    ]

class Contact(Orderable):

    contact_page = ParentalKey(ContactPage, related_name='contacts')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    name = models.CharField(max_length=50) # e.g. Bristol Office
    address = RichTextField(blank=True)
    phone = models.CharField(max_length=15, validators=[phone_regex], blank=True)    
    email = models.EmailField(blank=True)
    map_link = models.URLField(blank=True) # link google map, say

"""
Work Pages
"""
class WorkPage(Page):
    introduction = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel('introduction')
    ]

class CaseStudyPage(Page):

    main_image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    body = StreamField([
        ('heading', blocks.CharBlock()),
        ('detail', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])
    site_url = models.URLField()
    client = models.ForeignKey(
        'company.Client', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
        FieldPanel('site_url'),
        FieldPanel('client'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

@register_snippet
class Client(models.Model):
    client_name = models.CharField(max_length=50)

    panels = [
        FieldPanel('client_name')
    ]

    def __str__(self):
        return self.client_name

"""
Staff Page
"""
class StaffPage(Page):

    introduction = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]

class StaffProfile(Page):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    job_title = models.CharField(max_length=30)
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    short_bio = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('first_name'),
                FieldPanel('last_name')
            ],
            heading='Name'
        ),
        FieldPanel('job_title'),
        ImageChooserPanel('image'),
        FieldPanel('short_bio')
    ]

"""
Jobs Pages
"""
class JobsPage(Page):

    introduction = models.TextField(blank=False)

    content_panels = Page.content_panels + [
        FieldPanel('introduction')
    ]

class JobPage(Page):
    job_title = models.CharField(max_length=50)
    job_level = models.ForeignKey(
        'company.JobLevel', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    job_description = RichTextField(blank=False)

    content_panels = Page.content_panels + [
        FieldPanel('job_title'),
        FieldPanel('job_level', widget=forms.RadioSelect),
        FieldPanel('job_description')
    ]

@register_snippet
class JobLevel(models.Model):
    level_description = models.CharField(max_length=20)

    panels = [
        FieldPanel('level_description')
    ]

    def __str__(self):
        return self.level_description