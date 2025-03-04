import django_tables2 as tables
from crispy_forms.layout import Row

from app.models import CookbookIngredient
from crud_views.lib.crispy import CrispyModelForm, Column2, CrispyModelViewMixin, CrispyDeleteForm, Column12, Column6
from crud_views.lib.table import Table, LinkDetailColumn
from crud_views.lib.views import DetailViewPermissionRequired, UpdateViewPermissionRequired, \
    CreateViewPermissionRequired, \
    ListViewTableMixin, DeleteViewPermissionRequired, ListViewPermissionRequired
from crud_views.lib.viewset import ViewSet

cv_ingredient = ViewSet(
    model=CookbookIngredient,
    name="ingredient",
    icon_header="fa-solid fa-paw"
)

class IngredientForm(CrispyModelForm):
    submit_label = "Create"

    class Meta:
        model = CookbookIngredient
        fields = ["name", "producer", "source", "description"]

    def get_layout_fields(self):
        return Row(Column6("name"), Column6("producer"), Column6("source"), Column12("description"))


class IngredientTable(Table):
    name = LinkDetailColumn()
    quantity = tables.Column()


class IngredientListView(ListViewTableMixin, ListViewPermissionRequired):
    model = CookbookIngredient
    table_class = IngredientTable
    cv_viewset = cv_ingredient
    cv_list_actions = ["detail", "update", "delete"]


class IngredientDetailView(DetailViewPermissionRequired):
    model = CookbookIngredient
    cv_viewset = cv_ingredient
    cv_properties =  ["name", "producer", "source", "description"]


class IngredientUpdateView(CrispyModelViewMixin, UpdateViewPermissionRequired):
    model = CookbookIngredient
    form_class = IngredientForm
    cv_viewset = cv_ingredient


class IngredientCreateView(CrispyModelViewMixin, CreateViewPermissionRequired):
    model = CookbookIngredient
    form_class = IngredientForm
    cv_viewset = cv_ingredient


class IngredientDeleteView(CrispyModelViewMixin, DeleteViewPermissionRequired):
    model = CookbookIngredient
    form_class = CrispyDeleteForm
    cv_viewset = cv_ingredient
