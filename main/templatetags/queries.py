from django import template

from main.models import Group

register = template.Library()


@register.inclusion_tag("includes/footer.html")
def show_footer():
    groups = Group.objects.prefetch_related("pages")
    return {"groups": groups}
