from django.shortcuts import render, redirect
from .models import Restaurant, Menu
from .forms import RestaurantForm, MenuForm, MenuUpdateForm

# Create your views here.
def index(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'restaurants/index.html', context)

def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save()
            return redirect('restaurants:detail', restaurant.pk)
    else:
        form = RestaurantForm()
    context = {
        'form': form
    }
    return render(request, 'restaurants/create.html', context)

def detail(request, restaurant_pk):
    restaurant = Restaurant.objects.get(pk=restaurant_pk)
    menus = restaurant.menu_set.all()
    menu_form = MenuForm()
    context = {
        'restaurant': restaurant,
        'menus':menus,
        'menu_form': menu_form
    }
    return render(request, 'restaurants/detail.html', context)

def menus_create(request, restaurant_pk):
    restaurant = Restaurant.objects.get(pk=restaurant_pk)
    if request.method == 'POST':
        menu_form = MenuForm(request.POST)
        if menu_form.is_valid():
            menu = menu_form.save(commit=False)
            menu.restaurant = restaurant
            menu.save()
        else:
            menu_form = MenuForm()
            context = {
                'restaurant': restaurant,
                'menu_form': menu_form
            }
            return render(request, 'restaurants/detail.html', context)
    return redirect('restaurants:detail', restaurant_pk)

def menus_update(request,restaurant_pk, menu_pk):
    menu = Menu.objects.get(pk=menu_pk)
    if request.method == 'POST':
        menu_form = MenuUpdateForm(request.POST, instance=menu)
        if menu_form.is_valid():
            menu_form.save()
            return redirect('restaurants:detail', restaurant_pk)
    else:
        menu_form = MenuUpdateForm(instance=menu)
    context = {
        'menu_form' : menu_form,
        'menu':menu,
        'restaurant_pk': restaurant_pk,
    }
    return render(request, 'restaurants/update_menu.html',context)