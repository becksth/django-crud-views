import django_tables2 as tables
from crispy_forms.layout import Row

from app.models import CookbookCookbook
from crud_views.lib.crispy import CrispyModelForm, Column4, Column2, CrispyModelViewMixin, CrispyDeleteForm
from crud_views.lib.table import Table, LinkChildColumn, LinkDetailColumn
from crud_views.lib.table.columns import NaturalTimeColumn, NaturalDayColumn
from crud_views.lib.views import DetailViewPermissionRequired, UpdateViewPermissionRequired, CreateViewPermissionRequired, \
    ListViewTableMixin, DeleteViewPermissionRequired, ListViewPermissionRequired
from crud_views.lib.viewset import ViewSet

cv_cookbook = ViewSet(
    model=CookbookCookbook,
    name="cookbook",
    icon_header="fa-solid fa-paw"
)


class CookbookForm(CrispyModelForm):
    submit_label = "Create"

    class Meta:
        model = CookbookCookbook
        fields = ["title","published_date","isbn","pages","language","cover_image","author"]

    def get_layout_fields(self):
        return Row(Column2("title","published_date","isbn","pages","language","cover_image","author"))


class CookbookTable(Table):
    id = LinkDetailColumn()
    title = tables.Column()
    published_date = NaturalDayColumn()
    isbn = tables.Column()
    pages = tables.Column()
    language = tables.Column()
    author = LinkChildColumn(name="cookbookauthor", verbose_name="Author", empty_values=())



class CookbookListView(ListViewTableMixin, ListViewPermissionRequired):
    model = CookbookCookbook
    table_class = CookbookTable
    cv_viewset = cv_cookbook
    cv_list_actions = ["detail", "update", "delete"]


class CookbookDetailView(DetailViewPermissionRequired):
    model = CookbookCookbook
    cv_viewset = cv_cookbook
    cv_properties = ["id","title","published_date","isbn","pages","language","cover_image"]


class CookbookUpdateView(CrispyModelViewMixin, UpdateViewPermissionRequired):
    model = CookbookCookbook
    form_class = CookbookForm
    cv_viewset = cv_cookbook


class CookbookCreateView(CrispyModelViewMixin, CreateViewPermissionRequired):
    model = CookbookCookbook
    form_class = CookbookForm
    cv_viewset = cv_cookbook


class CookbookDeleteView(CrispyModelViewMixin, DeleteViewPermissionRequired):
    model = CookbookCookbook
    form_class = CrispyDeleteForm
    cv_viewset = cv_cookbook
