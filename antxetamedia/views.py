from django.views.generic import TemplateView

from antxetamedia.structure.models import Node
from antxetamedia.recordings.models import News, Program, INTERVIEW
from antxetamedia.multimedia.models import get_orphaned_media
from antxetamedia.agenda.models import Happening
from antxetamedia.misc.models import Widget, Feed, Link, PANEL

class FrontPageView(TemplateView):
    template_name = 'frontpage.html'

    def get_context_data(self, **kwargs):
        c = super(FrontPageView, self).get_context_data(**kwargs)

        programs = {}
        for node in Node.objects.filter(on_frontpage=True):
            programs[node] = Program.objects.filter(
                    program__in=node.descendents(including_this=True),
                    )[:10]

        c.update({
            'news': News.objects.all()[:13],
            'programs': programs,
            'orphaned_media': get_orphaned_media()[:10],
            'happenings': Happening.objects.future()[:10],
            'widgets': Widget.objects.all(),
            'feeds': Feed.objects.filter(where=PANEL),
            'links': Link.objects.all(),
            })
        return c
