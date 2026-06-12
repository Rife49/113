from django.contrib import admin
from .models import Category, Ingredient, RecipeIngredient, Recipe
# Register your models here.

# admin.site.register([Category, Ingredient, RecipeIngredient, Recipe])

# -------- Category ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'recipe_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug':('name',)}
    
    @admin.display(description='# Recipes')
    def recipe_count(self, obj):
        return obj.recipes.count()
    
    
# -------- Ingredient -----------
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
    
# -------- RecipeIngredient InLine ----------
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3 # how many epmty rows to show by default
    fields = ('ingredient', 'quantity', 'unit', 'note')
    
    
# ---------- Recipe ----------
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'prep_time', 'cook_time', 'created_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RecipeIngredientInline]
    
    
    fieldsets = (
        ('Main Informaition', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('Content', {
            'fields': ('description', 'instructions', 'image')
        }),
        ('Time & Servings', {
            "fields": ('prep_time', 'cook_time', 'servings')
        }),
        ('Timestamps',{
            'fields': ('created_at', 'updated_at'),
            'classes': ('collaspe',)
        }),
    )