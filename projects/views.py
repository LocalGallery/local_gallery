from django.views.generic import ListView, DetailView

from projects.models import Project


class ProjectListView(ListView):
    model = Project


class ProjectDetailView(DetailView):
    model = Project


class ProjectAppView(ProjectDetailView):
    template_name = "projects/project_app.html"
