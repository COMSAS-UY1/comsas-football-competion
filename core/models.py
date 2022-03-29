from django.db import models
from django_tuieditor.models import MarkdownField
from tournoi.models import Edition


class ContactInfo(models.Model):
    '''Manages the contact form/page'''
    name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        error_messages={'required': ("Veuillez entrer votre nom et prénom.")})
    email = models.EmailField(
        null=True,
        blank=True,
        error_messages={'required': ("Veuillez entrer votre adresse email.")})
    phone = models.CharField(max_length=9,
                             null=False,
                             blank=False,
                             error_messages={
                                 'required':
                                 ("Veuillez entrer votre numéro de téléphone.")
                             })
    subject = models.CharField(
        max_length=100,
        error_messages={
            'required': ("Veuillez entrer le titre de votre message.")
        })
    message = models.TextField(
        null=False,
        blank=False,
        error_messages={'required': ("Veuillez entrer votre message.")})

    def __str__(self):
        return self.name + ' ' + self.subject


class News(models.Model):
    image = models.ImageField(
        upload_to='actualites/',
        default="news_placeholder.jpg",
    )
    title = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    description = MarkdownField(
        max_length=150,
        null=False,
        blank=False,
    )
    edition = models.ForeignKey(Edition, models.CASCADE)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=300, blank=True, null=True)
    edition = models.ForeignKey(Edition,
                                models.CASCADE,
                                related_name='gallery',
                                null=True,
                                blank=True)

    def __str__(self) -> str:
        return self.title


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='galleries/', null=False)
    alt = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self) -> str:
        return f'photo de {self.gallery.title}'


class Contributor(models.Model):
    image = models.ImageField(upload_to='contributors/', null=False)
    name = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    website = models.URLField(max_length=300, )
    twitter = models.URLField(max_length=300, )
    github = models.URLField(max_length=300, )
    description = models.TextField()
