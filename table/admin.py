



from django.contrib import admin
from table.models import Category, FoodItem, NotSubmittedItem, SubmittedItem

# Admin configuration for Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


from .models import FoodItem

class FoodItemAdmin(admin.ModelAdmin):
    # your custom admin settings here
    pass

admin.site.register(FoodItem, FoodItemAdmin)

# Admin configuration for NotSubmittedItem model
@admin.register(NotSubmittedItem)
class NotSubmittedItemAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'quantity')      # Display food item and its quantity
    search_fields = ['food_item__name']           # Search by food item name
    list_filter = ['food_item']                   # Filter by food item

# Admin configuration for SubmittedItem model
@admin.register(SubmittedItem)
class SubmittedItemAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'quantity', 'total_price')  # Display food item, quantity, and total price
    search_fields = ['food_item__name']                      # Search by food item name
    list_filter = ['food_item']                              # Filter by food item

