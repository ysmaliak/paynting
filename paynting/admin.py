from django.contrib import admin
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Masterpiece, Profile, Search, Sort
from django_reverse_admin import ReverseModelAdmin
from gevent.pool import Pool
from .tokens import account_activation_token
import datetime
from jinja2 import Template


class MasterpieceAdmin(ReverseModelAdmin):
    inline_type = 'tabular'
    inline_reverse = [('made_with', {'fields': ['hardware', 'software']}), ]


def send(queryset_user):
    template = Template("""
    Date/time: {{ now() }}
    Hi {{ user.username }} ({{ user.email }}),

    Please click the following link to confirm your registration:
    http://127.0.0.1:8080/activate/{{ uid }}/{{ token }}
    """)

    template.globals['now'] = datetime.datetime.utcnow
    template.globals['user'] = queryset_user.user
    template.globals['uid'] = urlsafe_base64_encode(force_bytes(queryset_user.user.pk))
    template.globals['token'] = account_activation_token.make_token(queryset_user.user)

    subject = 'Please Activate Your Account'
    queryset_user.user.email_user(subject, template.render())


def send_signup_confirmation(modeladmin, request, queryset):
    pool = Pool(5)
    pool.map(send, queryset)


send_signup_confirmation.short_description = "Send signup confirmation"


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'signup_confirmation']
    ordering = ['user']
    actions = [send_signup_confirmation]


admin.site.register(Masterpiece, MasterpieceAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Search)
admin.site.register(Sort)
