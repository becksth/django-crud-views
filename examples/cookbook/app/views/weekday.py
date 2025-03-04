import django_tables2 as tables
from crispy_forms.layout import Row

from app.models import Weekday
from crud_views.lib.crispy import CrispyModelForm, Column4, CrispyModelViewMixin, CrispyDeleteForm
from crud_views.lib.table import Table, LinkChildColumn, LinkDetailColumn
from crud_views.lib.views import DetailViewPermissionRequired, UpdateViewPermissionRequired, CreateViewPermissionRequired, \
    ListViewTableMixin, DeleteViewPermissionRequired, ListViewPermissionRequired
from crud_views.lib.viewset import ViewSet

cv_weekday = ViewSet(
    model=Weekday,
    name="weekday",
    icon_header="fa-solid fa-paw"
)


class WeekdayForm(CrispyModelForm):
    submit_label = "Create"

    class Meta:
        model = Weekday
        fields =  ["dow", "musc_group"]

    def get_layout_fields(self):
        return Row(Column4("dow"), Column4("musc_group"))


class WeekdayTable(Table):
    weekday_pk = LinkDetailColumn()
    dow = tables.Column()
    musc_group = tables.Column()


class WeekdayListView(ListViewTableMixin, ListViewPermissionRequired):
    model = Weekday
    table_class = WeekdayTable
    cv_viewset = cv_weekday
    cv_list_actions = ["detail", "update", "delete"]


class WeekdayDetailView(DetailViewPermissionRequired):
    model = Weekday
    cv_viewset = cv_weekday
    cv_properties = ["weekday_pk", "dow", "musc_group"]


class WeekdayUpdateView(CrispyModelViewMixin, UpdateViewPermissionRequired):
    model = Weekday
    form_class = WeekdayForm
    cv_viewset = cv_weekday


class WeekdayCreateView(CrispyModelViewMixin, CreateViewPermissionRequired):
    model = Weekday
    form_class = WeekdayForm
    cv_viewset = cv_weekday


class WeekdayDeleteView(CrispyModelViewMixin, DeleteViewPermissionRequired):
    model = Weekday
    form_class = CrispyDeleteForm
    cv_viewset = cv_weekday
