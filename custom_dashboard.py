"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'dashboard.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from reports.utils import get_summary_table

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

class ChartDashboard(modules.DashboardModule):
    """
    """
    template = 'reports/dashboard/chart_dashboard.html'
    layout = 'stacked'
    headers = []
    fields = []
    children = []

    def __init__(self, title, chart_id, **kwargs):
        super(ChartDashboard, self).__init__(title, **kwargs)
        self.chart_id=chart_id
        self.title = title

    def init_with_context(self, context):
        from stats.utils import render_chart
        render_chart( context, self.chart_id)
        return super(ChartDashboard, self).init_with_context(context)

class TableDashboard(modules.DashboardModule):
    """
    """
    template = 'reports/dashboard/table_dashboard.html'
    layout = 'stacked'
    headers = []
    fields = []

    def __init__(self, title, children, headers, fields, **kwargs):
        super(TableDashboard, self).__init__(title, **kwargs)
        self.children = children or []
        self.headers = headers
        self.fields = fields
        self.title = title

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for dashboard.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Reportes'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))

        qs = get_summary_table()
        self.children.append(
            TableDashboard(
                title='Resumen de Ventas',
                children = qs,
                headers = ['CODE','Pais','Ventas Esperadas','Ventas Reales','Desv','%','Comentarios'],
                fields = ['id','operator','expected','real','diff','percent','inactive']
                )
        )


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for dashboard.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
