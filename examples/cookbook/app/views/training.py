import django_tables2 as tables
from crispy_forms.layout import Row

from app.models import Training
from crud_views.lib.crispy import CrispyModelForm, Column4, CrispyModelViewMixin, CrispyDeleteForm
from crud_views.lib.table import Table, LinkChildColumn, LinkDetailColumn
from crud_views.lib.view import cv_property
from crud_views.lib.views import DetailViewPermissionRequired, UpdateViewPermissionRequired, CreateViewPermissionRequired, \
    ListViewTableMixin, DeleteViewPermissionRequired, ListViewPermissionRequired
from crud_views.lib.viewset import ViewSet

cv_training = ViewSet(
    model=Training,
    name="training",
    icon_header="fa-solid fa-paw"
)


class TrainingForm(CrispyModelForm):
    submit_label = "Create"

    class Meta:
        model = Training
        fields = ["name", "repetition", "weight", "training_dow"]

    def get_layout_fields(self):
        return Row(Column4("name"), Column4("repetition"), Column4("weight"), Column4("training_dow"))


class TrainingTable(Table):
    id = LinkDetailColumn()
    name = tables.Column()
    weight = tables.Column()
    repetition = tables.Column()

class TrainingListView(ListViewTableMixin, ListViewPermissionRequired):
    model = Training
    table_class = TrainingTable
    cv_viewset = cv_training
    cv_list_actions = ["detail", "update", "delete"]


class TrainingDetailView(DetailViewPermissionRequired):
    model = Training
    cv_viewset = cv_training
    cv_properties = ["name", "repetition", "weight", "weekday"]

    @cv_property(foo=4711)
    def weekday(self) -> str:
        return str(self.object.training_dow)


class TrainingUpdateView(CrispyModelViewMixin, UpdateViewPermissionRequired):
    model = Training
    form_class = TrainingForm
    cv_viewset = cv_training


class TrainingCreateView(CrispyModelViewMixin, CreateViewPermissionRequired):
    model = Training
    form_class = TrainingForm
    cv_viewset = cv_training


class TrainingDeleteView(CrispyModelViewMixin, DeleteViewPermissionRequired):
    model = Training
    form_class = CrispyDeleteForm
    cv_viewset = cv_training
