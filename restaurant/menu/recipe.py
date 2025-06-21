from db.models import Recipe, RecipeIngredient, Ingredient
from db.database import Session

class RecipeManager:
    def __init__(self):
        self.session = Session()

    def create_recipe(self, menu_item_id: int, ingredients: dict):
        """
        ingredients: dict {ingredient_id: quantity}
        """
        recipe = Recipe(menu_item_id=menu_item_id)
        self.session.add(recipe)
        self.session.flush()  # aby mieć recipe.id

        for ing_id, qty in ingredients.items():
            ing = self.session.query(Ingredient).get(ing_id)
            if not ing:
                raise ValueError(f"Nie znaleziono składnika o id {ing_id}")
            usage = RecipeIngredient(recipe_id=recipe.id, ingredient_id=ing_id, quantity=qty)
            self.session.add(usage)

        self.session.commit()
        return recipe

    def update_recipe(self, recipe_id: int, ingredients: dict):
        recipe = self.session.query(Recipe).get(recipe_id)
        if not recipe:
            raise ValueError("Przepis nie znaleziony")

        # Usuwamy stare składniki przepisu
        self.session.query(RecipeIngredient).filter_by(recipe_id=recipe_id).delete()
        self.session.flush()

        # Dodajemy nowe składniki
        for ing_id, qty in ingredients.items():
            ing = self.session.query(Ingredient).get(ing_id)
            if not ing:
                raise ValueError(f"Nie znaleziono składnika o id {ing_id}")
            usage = RecipeIngredient(recipe_id=recipe.id, ingredient_id=ing_id, quantity=qty)
            self.session.add(usage)

        self.session.commit()