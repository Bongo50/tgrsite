from django.shortcuts import render
from django.views import generic
from .models import Report

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# In order to access global bug list, must be an admin.
class Index(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
	model = Report

	permission_required = 'change_report'

	# Until I make a "permission denied" page myself, this is better than an infinite redirect loop
	raise_exception = True

class Detail(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
	model = Report

	permission_required = 'change_report'
	raise_exception = True

	# in order to access a given report, must be admin OR be the creator of that report
	def has_permission(self):
		print(self.request)
		can_admin = self.request.user.has_perms(self.get_permission_required())

		report_object = Report.objects.get(id=self.kwargs['pk'])
		is_reporter = (report_object.reporter == self.request.user.member)

		return can_admin or is_reporter

# must be logged in to create a bug report
class Create(LoginRequiredMixin, generic.CreateView):
	model = Report
	fields = ['title', 'body', 'feature']

	def form_valid(self, form):
		# Adds the current logged-in user as the reporter of the bug
		form.instance.reporter = self.request.user.member
		return super(Create, self).form_valid(form)
