from django.views.generic import DetailView, ListView
from rest_framework.renderers import JSONRenderer
from openbudgets.apps.accounts.serializers import AccountMin
from openbudgets.apps.tools import models
from openbudgets.apps.tools import serializers


class ToolListView(ListView):
    model = models.Tool
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


class ToolDetailBaseView(DetailView):

    model = models.Tool

    def get_context_data(self, **kwargs):

        context = super(ToolDetailBaseView, self).get_context_data(**kwargs)
        state = {}
        renderer = JSONRenderer()

        try:
            state_id = self.kwargs.get('state')
            state = serializers.State(models.State.objects.get(id=state_id), context={'request': self.request}).data
        except models.State.DoesNotExist:
            pass

        context['tool_json'] = renderer.render(serializers.Tool(self.object, context={'request': self.request}).data)
        context['state_json'] = renderer.render(state)

        return context


class ToolDetailView(ToolDetailBaseView):

    def get_template_names(self):
        return ['tools/ext/{slug}/tool.html'.format(slug=self.object.slug)]

    def get_context_data(self, **kwargs):

        context = super(ToolDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        renderer = JSONRenderer()
        user_object = {}

        # add logged in user
        if user.is_authenticated():
            user_object = AccountMin(user).data

        context['user_json'] = renderer.render(user_object)

        return context


class ToolEmbedView(ToolDetailBaseView):

    def get_template_names(self):
        return ['tools/ext/{slug}/embed.html'.format(slug=self.object.slug)]
