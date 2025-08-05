from modeltranslation.translator import TranslationOptions, register

from main.models import Page, Slider


@register(Page)
class PageOptions(TranslationOptions):
    fields = ["title", "content"]


@register(Slider)
class SliderOptions(TranslationOptions):
    fields = ["title", "short_description", "url_text"]
