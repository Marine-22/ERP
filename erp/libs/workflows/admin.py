from django.contrib import admin
from erp.libs.workflows.models import State
from erp.libs.workflows.models import StateObjectRelation
from erp.libs.workflows.models import Transition
from erp.libs.workflows.models import Workflow
from erp.libs.workflows.models import WorkflowObjectRelation
from erp.libs.workflows.models import WorkflowModelRelation

class StateInline(admin.TabularInline):
    model = State

class WorkflowAdmin(admin.ModelAdmin):
    inlines = [
        StateInline,
    ]

admin.site.register(Workflow, WorkflowAdmin)

admin.site.register(State)
admin.site.register(StateObjectRelation)
admin.site.register(Transition)
admin.site.register(WorkflowObjectRelation)
admin.site.register(WorkflowModelRelation)

