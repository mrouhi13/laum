from django import template

register = template.Library()


@register.inclusion_tag('web/includes/google_analytics.html', takes_context=True)
def google_analytics(context):
    """
    Add Google Analytics script.

    Usage:
        {% load google_analytics %}
        {% google_analytics 'UA-111111111' %}
    """

    google_analytics_id = context['GOOGLE_ANALYTICS_ID']

    if not google_analytics_id:
        raise Exception('Google Analytics ID is required.')

    return {'google_analytics_id': google_analytics_id}
