from django.views.generic import DetailView, ListView
from rest_framework.renderers import JSONRenderer
from openbudget.apps.accounts.serializers import AccountMin
from openbudget.apps.projects.models import Project
from openbudget.apps.projects import serializers


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'

    def get_context_data(self, **kwargs):

        context = super(ProjectListView, self).get_context_data(**kwargs)

        projects_public = []
        projects_developers = []

        for e in self.object_list:
            if e.label == 'public':
                projects_public.append(e)
            else:
                projects_developers.append(e)

        context['projects_public'] = projects_public
        context['projects_developers'] = projects_developers

        return context


class ProjectDetailView(DetailView):
    model = Project

    def get_template_names(self):
        return ['projects/ext/{slug}.html'.format(slug=self.object.slug)]

    def get_context_data(self, **kwargs):

        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        renderer = JSONRenderer()
        user_object = {}

        # add logged in user
        if user.is_authenticated():
            user_object = AccountMin(user).data

        context['user_json'] = renderer.render(user_object)
        context['project_json'] = renderer.render(serializers.ProjectBaseSerializer(self.object).data)

        return context
