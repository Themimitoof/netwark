"""
Contains all pyramid events
"""
from pyramid.events import NewRequest


def flash_messages(event: NewRequest) -> list:
    """
    Retrieve flash messages stored in session, store it in request object and
    delete flash messages from the session.
    """
    flash = []

    if hasattr(event.request, 'session'):
        flash = event.request.session.pop('flash', [])

    event.request.flash = flash
