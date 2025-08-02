import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from main.models import Group

register = template.Library()


@register.inclusion_tag("includes/footer.html")
def show_footer():
    groups = Group.objects.prefetch_related("pages")
    return {"groups": groups}


@register.filter(name="render_markdown")
@stringfilter
def render_markdown(text):
    html = markdown.markdown(text)
    return mark_safe(html)
