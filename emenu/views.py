from django.shortcuts import render,get_object_or_404

# Create your views here.
from table.models import Category,FoodItem


def table_home(request, id=None):
    categories = Category.objects.all()
    
    if id:  # if a category ID is provided in the URL
        selected_category = get_object_or_404(Category, id=id)
    else:  # otherwise, show the first category by default
        selected_category = categories.first()

    # Get the food items for the selected category
    food_items = FoodItem.objects.filter(category=selected_category)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'food_items': food_items
    }
    return render(request, 'table_home.html', context)

