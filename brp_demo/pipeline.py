from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.models import Site, RequestSite
from django.contrib.auth.models import Group
from django.template.loader import render_to_string

from registration.models import RegistrationProfile

USER_FIELDS = ['username', 'email']


def moderate_user(strategy, details, user=None, *args, **kwargs):

    is_new = kwargs.get('is_new')

    # This user has authenticated but not yet moderated.
    if not is_new and not user.is_active:
        return redirect('register')

    if is_new:
        profile = RegistrationProfile.objects.create_profile(user)
        profile.verified = True
        profile.save()

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        # send a new user registration email explaining the next steps
        subject = render_to_string('registration/moderator_subject.txt', {
            'site': site
        })
        # no newlines
        subject = ''.join(subject.splitlines())
        message = render_to_string('registration/moderator_email.txt', {
            'site': site,
            'profile': profile
        })
        user.is_active = False
        moderators = (x[1] for x in settings.MANAGERS)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, moderators)
        strategy.storage.user.changed(user)

        g = Group.objects.get(name='Consortium Members')
        g.user_set.add(user)
        g.save()        
