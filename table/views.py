

# table/views.py
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from .models import FoodItem, NotSubmittedItem, SubmittedItem, Category
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    food_items = FoodItem.objects.filter(category=category)
    return render(request, 'index.html', {
        'category': category,
        'food_items': food_items,
    })


def about(request):
    return render(request, 'about.html')
  
def  testimonial(request):
    return render(request , 'testimonial.html')

  
def  booking(request):
    return render(request , 'booking.html')

def contact(request):
    return render(request ,'contact.html')

def bill(request):
    return render(request ,'bill.html')
    # return HttpResponse("in bill")

def submit_order(request):
    not_submitted_items = NotSubmittedItem.objects.all()
    total_bill = 0

    for item in not_submitted_items:
        total_price = item.price * item.quantity
        SubmittedItem.objects.create(
            food_item=item.food_item,
            name=item.name,
            price=item.price,
            image=item.image,
            quantity=item.quantity,
            total_price=total_price
        )
        total_bill += total_price

    NotSubmittedItem.objects.all().delete()  # Clear NotSubmitted items
    not_submitted_items = NotSubmittedItem.objects.all()  # Fetch all the selected items
    submitted_items = SubmittedItem.objects.all()
    # return render(request, 'order.html', {'total_bill': total_bill})

    return render(request, 'order.html', {'not_submitted_items': not_submitted_items  ,'submitted_items':submitted_items ,  'total_bill': total_bill})




from django.http import JsonResponse
from .models import NotSubmittedItem, FoodItem

def add_not_submitted_item(request):
    if request.method == "POST":
        food_item_id = request.POST.get('item_id')  # Use 'food_item' as ForeignKey to FoodItem
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = int(request.POST.get('quantity'))
        image_url = request.POST.get('image_url')

        # Fetch the FoodItem instance
        try:
            food_item = FoodItem.objects.get(id=food_item_id)
        except FoodItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Food item not found'}, status=404)

        # Check if the item is already in the not submitted list
        item, created = NotSubmittedItem.objects.get_or_create(
            food_item=food_item,  # Using ForeignKey to FoodItem
            defaults={
                'name': name,
                'price': price,
                'quantity': quantity,
                'image': image_url  # Assuming you handle image uploads elsewhere
            }
        )

        if not created:
            # If the item already exists, update the quantity
            item.quantity += quantity
            item.save()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


def order(request):
    not_submitted_items = NotSubmittedItem.objects.all()  # Fetch all the selected items
    submitted_items = SubmittedItem.objects.all()
    return render(request, 'order.html', {'not_submitted_items': not_submitted_items  ,'submitted_items':submitted_items })


# views.py

from django.shortcuts import get_object_or_404, redirect
from .models import SubmittedItem

def cancel_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(NotSubmittedItem, id=item_id)
        item.delete()
        return redirect('order')  # Redirect to the order view


def submit_order_final(request):
    not_submitted_items = NotSubmittedItem.objects.all()  # Fetch all not submitted items
    total_bill = 0

    # Move each item to SubmittedItem
    for final_item in not_submitted_items:
        total_price = final_item.price * final_item.quantity
        SubmittedItem.objects.create(
            food_item=final_item.food_item,
            name=final_item.name,
            price=final_item.price,
            image=final_item.image,  # Use the image directly from NotSubmittedItem
            quantity=final_item.quantity,
            total_price=total_price
        )
        total_bill += total_price

    # Delete all items from NotSubmittedItem after submission
    not_submitted_items.delete()

    return render(request, 'order.html', {'total_bill': total_bill})

def add_to_submitted_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        name = request.POST.get('name')
        price = request.POST.get('price')

        # Fetch the actual NotSubmittedItem
        final_item = NotSubmittedItem.objects.get(id=item_id)

        # Move item to SubmittedItem
        SubmittedItem.objects.create(
            food_item=final_item.food_item,
            name=name,
            price=price,
            image=final_item.image,  # Correct image handling
            quantity=final_item.quantity,
            total_price=final_item.price * final_item.quantity
        )

        # Delete the item from NotSubmittedItem
        final_item.delete()

        return JsonResponse({'message': 'Item added to order successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def decrease_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(NotSubmittedItem, id=item_id)

        # If the item's quantity is greater than 1, decrease it by 1
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            new_quantity = item.quantity
        else:
            # If the quantity is 1, remove the item from the list
            item.delete()
            new_quantity = 0

        # Return the new quantity as a JSON response
        return JsonResponse({'success': True, 'new_quantity': new_quantity})
    else:
        return JsonResponse({'success': False}, status=400)


def submit_all_items(request):
    not_submitted_items = NotSubmittedItem.objects.all()

    for item in not_submitted_items:
        # Check if the item already exists in the SubmittedItem model
        submitted_item = SubmittedItem.objects.filter(name=item.name).first()

        if submitted_item:
            # If it exists, just update the quantity
            submitted_item.quantity += item.quantity
            submitted_item.save()
        else:
            # If not, create a new SubmittedItem entry
            SubmittedItem.objects.create(
                name=item.name,
                image=item.image,
                quantity=item.quantity,
            )

        # Delete the item from NotSubmittedItem after submission
        item.delete()

    return redirect('order_page')






