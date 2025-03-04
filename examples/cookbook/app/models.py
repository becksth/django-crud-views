import uuid

from django.db import models
from ordered_model.models import OrderedModel
from polymorphic.models import PolymorphicModel


class Author(OrderedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, verbose_name="Vorname")
    last_name = models.CharField(max_length=100)
    pseudonym = models.CharField(max_length=100, blank=True, null=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(OrderedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Foo(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Bar(models.Model):
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Baz(models.Model):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Poly(PolymorphicModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shared = models.CharField(max_length=100)


class PolyOne(Poly):
    one = models.CharField(max_length=100)


class PolyTwo(Poly):
    two = models.CharField(max_length=100)


class Detail(OrderedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    integer = models.IntegerField(verbose_name="An integer field")
    number = models.FloatField(verbose_name="A float field")
    char = models.CharField(max_length=100, verbose_name="Text field")
    text = models.TextField(verbose_name="Multiline Text")
    boolean = models.BooleanField(null=True, default=None, verbose_name="A boolean value")
    boolean_two = models.BooleanField(null=True, default=None, verbose_name="Another boolean value")
    date = models.DateField(verbose_name="A date field")
    date_time = models.DateTimeField(verbose_name="A date field with time")
    author = models.ForeignKey(Author, verbose_name="A foreign key field", on_delete=models.SET_NULL, blank=True,
                               null=True)
    foo = models.ManyToManyField(Foo, verbose_name="Foo selected")
    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"





class Weekday(models.Model):
    weekday_pk = models.AutoField(primary_key=True)
    dow        = models.CharField(max_length=100)
    musc_group = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.dow + ' ' + self.musc_group}"


class Training(models.Model):
    name         = models.CharField(max_length=100)
    weight       = models.IntegerField(default=0)
    repetition   = models.IntegerField(default=12)
    training_dow = models.ForeignKey(Weekday, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Exercise(models.Model):
    day = models.DateField()
    training = models.ForeignKey(Training, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"




class CookbookPublisher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.TextField()
    website = models.URLField()

    def __str__(self):
        return self.name

class CookbookAuthor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CookbookCookbook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    publisher = models.ForeignKey(CookbookPublisher, on_delete=models.CASCADE, related_name='publishers')
    author = models.ForeignKey(CookbookAuthor, on_delete=models.CASCADE, related_name='authors')
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    language = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='cookbook_covers/', blank=True, null=True)

    def __str__(self):
        return self.title

class CookbookRecipeCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CookbookIngredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    producer = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class CookbookRecipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cookbook = models.ForeignKey(CookbookCookbook, on_delete=models.CASCADE, related_name='cookbook')
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    preparation_time = models.IntegerField(help_text="Preparation time in minutes")
    cooking_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    category = models.ForeignKey(CookbookRecipeCategory, on_delete=models.CASCADE, related_name='category')
#    rec_ingredients = models.ManyToManyField("CookbookRecIng", through="CookbookRecIng")

    def __str__(self):
        return self.name


class CookbookRecIng(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rec_id = models.ForeignKey(CookbookRecipe, on_delete=models.CASCADE)
    ing_id = models.ForeignKey(CookbookIngredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)
    measurement = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id} ({self.quantity}) ({self.measurement})"


