from django.views.generic import DetailView, ListView
from openbudget.apps.projects.models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'


class ProjectDetailView(DetailView):
    model = Project

    def get_template_names(self):
        return ['projects/ext/{slug}.html'.format(slug=self.object.slug)]
