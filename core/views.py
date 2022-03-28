from telnetlib import STATUS
from django.shortcuts import redirect, render, HttpResponse
from django.db.models import Count
from django.views import View
from core.models import Contributor, Edition, Player, Goal, GoalType, GalleryImage, PouleTeam, Team, MatchState, News, Gallery
from django.views.generic import TemplateView
from .forms import ContactForm
from django.core.mail.message import BadHeaderError
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.html import format_html


class IndexView(View):
    """ Class view for home page """
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = Edition.objects.filter(status='active').first()
        if current_edition:
            # get all scorers in the current edition
            goals = Goal.objects.exclude(
                goal_type=GoalType.CSC,
                match__edition__active=False).values("player").annotate(
                    nbgoal=Count("id"),
                    nbmatch=Count("match")).order_by("-nbgoal", "match")
            for i, elt in enumerate(goals):
                goals[i]["player"] = Player.objects.filter(
                    id=goals[i]["player"]).first()
            # get stats
            poules = current_edition.poules.all()
            classements = {}
            for poule in poules:
                poule_teams = PouleTeam.objects.filter(poule=poule).order_by(
                    "-points", "-goals_average")
                classements[poule.name] = poule_teams

            teams = Team.objects.all()

            next_match = current_edition.matches.filter(
                state=MatchState.to_program).order_by("date_to_play",
                                                      "id").first()

            match_not_play = current_edition.matches.exclude(
                state=MatchState.finish)
            played_match = current_edition.matches.filter(
                state=MatchState.finish).order_by("-date_to_play")
            all_match = current_edition.matches.all().order_by(
                "date_to_play", "id")

            # get news
            newsLimit = 3
            news = News.objects.all().order_by('-id')[:newsLimit]

            context = {
                "current_edition": current_edition,
                "poules": poules,
                "standing": classements,
                "goals": goals,
                "teams": teams,
                "matchs": all_match,
                "next_match": next_match,
                "not_played": match_not_play,
                "played_match": played_match,
                "last_match": played_match.first(),
                "news": news,
            }
        else:
            context = {}
        return render(request, self.template_name, context)


class MatchView(View):
    template_name = 'matches.html'

    def get(self, request, *args, **kwargs):
        # get current edition
        current_edition = Edition.objects.filter(status='active').first()
        match_not_play = current_edition.matches.exclude(
            state=MatchState.finish).order_by("date_to_play")

        played_match = current_edition.matches.filter(
            state=MatchState.finish).order_by("-date_to_play")
        all_match = current_edition.matches.all().order_by("date_to_play")
        context = {
            "nbar": "match",
            "to_plays": match_not_play,
            "played_matchs": played_match,
            "all_match": match_not_play
        }
        return render(request, self.template_name, context)


class ContactView(TemplateView):
    template_name = 'contact.html'


class TeamView(TemplateView):
    template_name = "players.html"

    def teams(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class GalleryView(View):
    template_name = "gallery.html"

    def get(self, request, *args, **kwargs):
        last_edition = Edition.objects.filter(status='programmed').order_by('-end_date').first()
        last_edition_gallery = Gallery.objects.filter(edition=last_edition.id).first()
        last_edition_images = GalleryImage.objects.filter(gallery=last_edition_gallery.id)
        context = {
            'last_edition_images': last_edition_images,
        }
        return render(request, self.template_name, context)

class ContributorsView(TemplateView):
    template_name = "contributors.html"

    def getContributors(self, request, *args, **kwargs):
        contributors = Contributor.objects.all()
        context = {
            'contributors': contributors,
        }
        return render(request, self.template_name, context)


# Contact form function
def getMessage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
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
        form = ContactForm()

    context = {'modelform': ContactForm}
    return render(request, 'contact.html', context)
