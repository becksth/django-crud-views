import django_tables2 as tables
from crispy_forms.layout import Row

from app.models import Baz
from crud_views.lib.crispy import CrispyModelForm, Column4, CrispyModelViewMixin, CrispyDeleteForm
from crud_views.lib.table import Table, LinkDetailColumn
from crud_views.lib.views import DetailViewPermissionRequired, UpdateViewPermissionRequired, CreateViewPermissionRequired, \
    ListViewTableMixin, DeleteViewPermissionRequired, ListViewPermissionRequired
from crud_views.lib.viewset import ViewSet, ParentViewSet

vs_baz = ViewSet(
    model=Baz,
    name="baz",
    parent=ParentViewSet(name="bar"),
    icon_header="fa-solid fa-dog"
)


class BazForm(CrispyModelForm):
    submit_label = "Create"

    class Meta:
        model = Baz
        fields = ["name"]

    def get_layout_fields(self):
        return Row(Column4("name"))


class BazTable(Table):
    id = LinkDetailColumn()
    name = tables.Column()

    def render_baz(self, record):
        return "baz"


class BazListView(ListViewTableMixin, ListViewPermissionRequired):
    model = Baz
    table_class = BazTable
    vs = vs_baz
    vs_list_actions = ["detail", "update", "delete"]


class BazDetailView(DetailViewPermissionRequired):
    model = Baz
    vs = vs_baz
    vs_properties = ["id", "name"]


class BazUpdateView(CrispyModelViewMixin, UpdateViewPermissionRequired):
    model = Baz
    form_class = BazForm

    vs = vs_baz


class BazCreateView(CrispyModelViewMixin, CreateViewPermissionRequired):
    model = Baz
    form_class = BazForm
    vs = vs_baz


class BazDeleteView(CrispyModelViewMixin, DeleteViewPermissionRequired):
    model = Baz
    form_class = CrispyDeleteForm
    vs = vs_baz
