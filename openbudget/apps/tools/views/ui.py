from django.views.generic import DetailView, ListView
from rest_framework.renderers import JSONRenderer
from openbudget.apps.accounts.serializers import AccountMin
from openbudget.apps.tools.models import Tool
from openbudget.apps.tools import serializers


class ToolListView(ListView):
    model = Tool
    template_name = 'tools/tool_list.html'

    def get_context_data(self, **kwargs):

        context = super(ToolListView, self).get_context_data(**kwargs)

        tools_public = []
        tools_developers = []

        for e in self.object_list:
            if e.label == 'public':
                tools_public.append(e)
            else:
                tools_developers.append(e)

        context['tools_public'] = tools_public
        context['tools_developers'] = tools_developers

        return context


class ToolDetailView(DetailView):
    model = Tool

    def get_template_names(self):
        return ['tools/ext/{slug}.html'.format(slug=self.object.slug)]

    def get_context_data(self, **kwargs):

        context = super(ToolDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        renderer = JSONRenderer()
        user_object = {}

        # add logged in user
        if user.is_authenticated():
            user_object = AccountMin(user).data

        context['user_json'] = renderer.render(user_object)
        context['tool_json'] = renderer.render(serializers.Tool(self.object).data)

        return context
