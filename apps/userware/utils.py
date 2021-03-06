import datetime
import hashlib
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth import logout
from django.contrib.auth import get_user_model; User = get_user_model()

from toolware.utils.generic import is_valid_email

from models import UserAudit
import constants

def get_user_by_username_or_email(username_or_email):
    """ Given an email or username, returns a user object or None """

    try:
        if is_valid_email(username_or_email):
            user = User.objects.get(email__iexact=username_or_email)
        else:
            user = User.objects.get(username__iexact=username_or_email)
    except User.DoesNotExist:
        try:
            from emailware.models import EmailAddress
        except ImportError:
            return None
        try:
            user = EmailAddress.objects.get(email__iexact=username_or_email).user
        except EmailAddress.DoesNotExist:
            return None
    return user

def get_logged_in_users(last_activity_in_minutes=5):
    """ Return all users with last activity less than `last_activity_in_minutes` ago."""

    last_active_delta = datetime.timedelta(minutes=last_activity_in_minutes)
    last_active = timezone.now() - last_active_delta
    query = Q(**{"useraudit__updated_at__gte": last_active.isoformat()})
    related_fields = ['useraudit__updated_at']
    users = User.objects.select_related(*related_fields).filter(query)
    return users


def get_sessions_for_user(user):
    """Returns all activity audit sessions for user"""

    audit_sessions = UserAudit.objects.filter(user=user)
    return audit_sessions


def force_logout(user, request=None):
    """ logout all other sessions of this active user """

    audit_sessions = get_sessions_for_user(user=user)
    for audit in audit_sessions:
        if request and audit.audit_key == request.session.get(constants.USERWARE_AUDIT_KEY, ''):
            audit.force_logout = False
        else:
            audit.force_logout = True
        audit.save()

def get_audit_object_for_session(request):
    """ Given a request, returns a Audit object or logs user out """

    try:
        cache_key = request.session[constants.USERWARE_AUDIT_KEY]
    except KeyError:
        logout(request) # cache_key is a MUST
        return None

    audit = cache.get(cache_key)
    if audit is None:
        try:
            audit = UserAudit.objects.get(audit_key=cache_key)
        except UserAudit.DoesNotExist:
            logout(request) # audit instance is a MUST
            return None

    cache.get(cache_key, audit)
    return audit


def cleanup_user_audits(user, audit_age_in_days=14):
    """ cleanup user audits that are older than  audit_age_in_days"""

    last_active_delta = datetime.timedelta(days=audit_age_in_days)
    last_active = timezone.now() - last_active_delta
    audit_sessions = get_sessions_for_user(user=user)
    for audit in audit_sessions:
        if audit.updated_at < last_active:
            audit.delete()





