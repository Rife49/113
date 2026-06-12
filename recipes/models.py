from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User 


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta: # Rearrange the displayable items on the admen sight
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    

class Ingredient(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    
    
    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ["name"]
        
        
    def __str__(self):
        return self.name


# ------- ManyToMany ---------
# SIMPLE ManyToMany - Django automatically creates he junction table
# it only store both ID's. We can't add extra fields
# class Recipe(models.model):
    #Ingredients = models.ManyToManyField(Ingredient)
    
# ManyToMany with THROUGH - We define the junction table ourselves
# We can add whatever field we need (quantity, unit, etc...)
# class Recipe(models.model):
    #Ingredients = models.ManyToManyField(Ingredient, through="Recipe Ingredient")

    
# ---- Recipe Ingredient Model (Junction Table) -----
# Relation between Recipe <---> Ingredient

class RecipeIngredient (models.Model):
    
    UNIT_CHOICES = [
        ('cup', 'Cup'),
        ('tbsp', 'Tablespoon'),
        ('tsp', 'Teaspoon'),
        ('g', 'Grams'),
        ('kg', 'Kilograms'),
        ('ml', 'Milliliters'),
        ('l', 'Liters'),
        ('lb', 'Pounds'),
        ('piece', 'Piece'),
        ('pinch', 'Pinch'),
        ('to_taste', 'To taste'),
    ]
    
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='recipe_ingredient')
    
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True)
    
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        blank=True)
    
    note = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe Ingredients"
        unique_together = ('recipe', 'ingredient')
        
    
    def __str__(self):
        return f'(self.ingredient.name) -> (self.recipe.title)'
    
# ------ Image helper function --------
def recipe_image_path(instance, filename):
    """Saves the image to: media/recipes/<author_id>/<filename>"""
    return f"recipes(instance.author.id)/{filename}"
    
    
# ------ Recipe Models ---------

class Recipe(models.Model):
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published')
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    instructions = models.TextField()
    prep_time = models.PositiveIntegerField(help_text="Time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Time in minutes")
    servings = models.PositiveIntegerField(default=2)
    image = models.ImageField(
        upload_to=recipe_image_path,
        blank=True,
        null=True
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes"
    )
    
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes"
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering  = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    @property
    def total_time(self):
        return self.prep_time + self.cook_time