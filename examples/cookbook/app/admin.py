from django.contrib import admin
from app.models import Author, CookbookPublisher, CookbookAuthor, CookbookCookbook, CookbookRecipeCategory, \
    CookbookRecipe, CookbookIngredient, CookbookRecIng


# admin.site.register(CookbookPublisher)
# admin.site.register(CookbookAuthor)



class RecipeInline(admin.TabularInline):
    model = CookbookRecipe
    extra = 1
    fields = ["name", "preparation_time", "cooking_time", "servings", "difficulty", "category"]


class IngredientInline(admin.TabularInline):
    model = CookbookIngredient
    extra = 1
    fields = ["name"]


class RecIngInline(admin.TabularInline):
    model = CookbookRecIng
    extra = 1
    fields = [ "ing_id", "quantity", "measurement"]



@admin.register(CookbookRecipeCategory)
class CookbookRecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(CookbookRecipe)
class CookbookRecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "instructions", "preparation_time", "cooking_time", "servings", "difficulty", "category"]
    list_filter = ["difficulty", "category"]
    search_fields = ["name", "difficulty"]
    inlines = [RecIngInline]

@admin.register(CookbookIngredient)
class CookbookIngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "producer", "source", "description"]



@admin.register(CookbookRecIng)
class CookbookRecIngAdmin(admin.ModelAdmin):
    list_display = ["quantity", "measurement"]


@admin.register(CookbookPublisher)
class CookbookPublisherAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "website"]


@admin.register(CookbookCookbook)
class CookbookCookbookAdmin(admin.ModelAdmin):
    list_display = ["title", "published_date", "isbn", "pages", "language", "cover_image"]
    list_filter = ["published_date", "language"]
    search_fields = ["title", "isbn"]
    inlines = [RecipeInline]


@admin.register(CookbookAuthor)
class CookbookAuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "pseudonym", "created_dt", "modified_dt"]
