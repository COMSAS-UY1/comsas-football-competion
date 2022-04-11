from pipes import Template
from pprint import pp, pprint
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.db.models import Count
from django.views import View
from core.models import Contributor, GalleryImage, News, Gallery
from django.views.generic import ListView
from .forms import ContactForm
from django.core.mail.message import BadHeaderError
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.html import format_html
from tournoi.models import Edition
from django.views.generic import TemplateView


class ContactView(View):
    template_name = 'core/contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Additional fields
            messsage = f"\n\nNouveau message sur coupe.comsas.club : Emetteur: {name}\n\nAdresse: {email} Message:{message}"
            subjectEmail = f'{subject}From <{email}>'

            # Uncomment this later to send email to required address
            # try:
            #     send_mail(
            #         subjectEmail,  #subject
            #         message,  #message
            #         email,  #from email
            #             ,  #to email
            #     )
            # except BadHeaderError:
            #     message.error(request, 'Désolé, Nous avons rencontré un problème lors de l\'envoi de votre reponse. Veuillez réessayer plustard.')

            # Test if form data was saved and output corresponding flash message to confirm message placement or not.
            try:
                form.save()
                message_out_success = format_html(
                    # f'Thanks for contacting us, <strong> {name} </strong> ! Your message has been sent successfully. You will be email a copy at <strong> {email} </strong> !'
                    f'Votre message a été envoyé avec succès. Merci de nous avoir contacté,'
                )
                messages.success(request, message_out_success)
            except:
                messages.error(request, 'Désolé, Nous avons rencontré un problème lors de l\'envoi de votre reponse. Veuillez réessayer plustard.')

            # Redidrect to the same page with message output.
            return redirect('core:contact')
        else:
            return render(request, self.template_name, {'form': form})


class GalleryView(View):
    template_name = "core/gallery.html"

    def get(self, request, *args, **kwargs):
        last_edition = Edition.objects.filter(
            status='programmed').order_by('-end_date').first()
        last_edition_gallery = Gallery.objects.filter(
            edition=last_edition.id).first()
        last_edition_images = GalleryImage.objects.filter(
            gallery=last_edition_gallery.id)
        context = {
            'last_edition_images': last_edition_images,
        }
        return render(request, self.template_name, context)


class ContributorsView(ListView):
    template_name = "core/contributors.html"
    queryset = Contributor.objects.all()


class NewsView(View):
    template_name = "core/blog.html"

    def get(self, request, *args, **kwargs):
        queryset = News.objects.filter(edition__status='active')
        context = {'news': queryset}
        return render(request, self.template_name, context)


class DetailNew(View):
    template_name = "core/single.html"

    def get(self, request, *args, **kwargs):
        new = get_object_or_404(News, id=self.kwargs['id'])
        news = News.objects.filter(edition__status='active')
        context = {'new': new, 'news': news}
        return render(request, self.template_name, context)
