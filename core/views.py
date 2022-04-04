from pipes import Template
from pprint import pp, pprint
from django.shortcuts import redirect, render, HttpResponse
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
            msg = "Si vous recevez ce mail c'est que votre message a bien été envoyé et est en cours de traitement. Voici les détails de votre message:..." + "\n\nNom Complet: " + name + "\nNuméro de téléphone : " + str(
                phone
            ) + "\n\nMessage Envoyé : " + message + "\n\n\nMerci de nous avoir contacté. Nous espérons vous revoir très bientôt.\n\nTel : [blank]\nEmail : [blank]\n\nEcrivez nous à propos de tout ce que vous voulez, a n'importe quel moment comme bon vous semble!"
            subjectEmail = subject + " <" + f'{email}' + ">"

            # Uncomment this later to send email to required address
            try:
                send_mail(
                    subjectEmail,  #subject
                    msg,  #message
                    email,  #from email
                    ['joelfah2003@gmail.com', email],  #to email
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found')

            # Save message in Database
            # form.save()

            # Test if form data was saved and output corresponding flash message to confirm message placement or not.
            try:
                form.save()
                message_out_success = format_html(
                    # f'Thanks for contacting us, <strong> {name} </strong> ! Your message has been sent successfully. You will be email a copy at <strong> {email} </strong> !'
                    f'Cher(e) <b>{name}</b>, merci de nous avoir contacté. Votre message a bien été envoyé. Vous allez recevoir une copie à l\'adresse <b>{email}</b> !'
                )
                messages.success(request, message_out_success)
            except:
                message_out_error = format_html(
                    f'Désolé, <b>{name}</b> ! Nous avons rencontré un problème lors de l\'envoi de votre reponse. Veuillez remplir à nouveau le formulaire.'
                )
                messages.error(request, message_out_error)

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


class InnerBlog(TemplateView):
    template_name = "core/single.html"
