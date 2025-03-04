import django_tables2 as tables
from crispy_forms.layout import Row

from app.models import CookbookRecipe
from crud_views.lib.crispy import CrispyModelForm, Column2, CrispyModelViewMixin, CrispyDeleteForm, Column6, Column12
from crud_views.lib.table import Table, LinkDetailColumn, LinkChildColumn
from crud_views.lib.views import DetailViewPermissionRequired, UpdateViewPermissionRequired, \
    CreateViewPermissionRequired, \
    ListViewTableMixin, DeleteViewPermissionRequired, ListViewPermissionRequired
from crud_views.lib.viewset import ViewSet

cv_recipe = ViewSet(
    model=CookbookRecipe,
    name="recipe",
    icon_header="fa-solid fa-paw"
)

class RecipeForm(CrispyModelForm):
    submit_label = "Create"

    class Meta:
        model = CookbookRecipe
        fields = ["name", "instructions", "preparation_time", "cooking_time", "servings", "difficulty", "category"]

    def get_layout_fields(self):
        return Row(Column12("name"),
                   Column12("instructions"),
                   Column2("preparation_time"), Column2("cooking_time"), Column2("servings"), Column2("difficulty"), Column2("category"))


class RecipeTable(Table):
    id = LinkDetailColumn()
    name = LinkDetailColumn()
    preparation_time = tables.Column()
    cooking_time = tables.Column()
    servings = tables.Column()
    difficulty = tables.Column()
    category = tables.Column()


class RecipeListView(ListViewTableMixin, ListViewPermissionRequired):
    model = CookbookRecipe
    table_class = RecipeTable
    cv_viewset = cv_recipe
    cv_list_actions = ["detail", "update", "delete"]


class RecipeDetailView(DetailViewPermissionRequired):
    model = CookbookRecipe
    cv_viewset = cv_recipe
    cv_properties = ["name", "instructions", "preparation_time", "cooking_time", "servings", "difficulty"]


class RecipeUpdateView(CrispyModelViewMixin, UpdateViewPermissionRequired):
    model = CookbookRecipe
    form_class = RecipeForm
    cv_viewset = cv_recipe


class RecipeCreateView(CrispyModelViewMixin, CreateViewPermissionRequired):
    model = CookbookRecipe
    form_class = RecipeForm
    cv_viewset = cv_recipe


class RecipeDeleteView(CrispyModelViewMixin, DeleteViewPermissionRequired):
    model = CookbookRecipe
    form_class = CrispyDeleteForm
    cv_viewset = cv_recipe
