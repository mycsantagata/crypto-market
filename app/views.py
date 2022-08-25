import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import OrderForm
from .models import Profile, Order


def check_login(request):
    if request.method == "POST":
        formFields = AuthenticationForm(data=request.POST)
        if formFields.is_valid():
            username = formFields.cleaned_data['username']
            password = formFields.cleaned_data['password']
            chk_user = authenticate(request, username=username, password=password)
            login(request, chk_user)
            return redirect('home')
        else:
            logout(request)
            formFields = AuthenticationForm()
            messages.success(request, "Username or password is incorrect, please try again.")
            return render(request, 'app/login.html', {'form': formFields})
    else:
        logout(request)
        formFields = AuthenticationForm()
        return render(request, 'app/login.html', {'form': formFields})


def sign_up(request):
    if request.method == "POST":
        formFields = UserCreationForm(data=request.POST)

        if formFields.is_valid():
            new_user = formFields.save()

            profile = Profile()
            profile.user = new_user
            profile.save()

            username = formFields.cleaned_data.get('username')
            password = formFields.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('check_login')
        else:
            for field, errors in formFields.errors.items():
                messages.success(request, 'Field: {} Errors: {}'.format(field, errors.as_data()))

            formFields = UserCreationForm()
            return render(request, 'app/sign_up.html', {'form': formFields})
    else:
        form = UserCreationForm()
        return render(request, 'app/sign_up.html', {'form': form})


@login_required(login_url='/login/')
def home(request):
    chk_auth = False

    if request.user.is_authenticated:
        chk_auth = True
        user = request.user
        profile = get_object_or_404(Profile, user__username=user.username)
        return render(request, 'app/home.html', {'profile': profile, 'chk_auth': chk_auth})
    else:
        return render(request, 'app/home.html', {'chk_auth': chk_auth})


@login_required(login_url='/login/')
def new_order(request):
    user = request.user
    profile = get_object_or_404(Profile, user__username=user.username)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']

            type_order = form.cleaned_data['type']
            order = Order()
            order.profile = profile
            order.type = type_order
            order.quantity = quantity
            order.price = price

            if type_order == 2:
                if 0 < quantity <= profile.btc:
                    buy_order = Order.objects.filter(type=1, price__gte=price, quantity=quantity, status=1) \
                        .order_by('-datetime') \
                        .order_by('price') \
                        .first()

                    if buy_order is None:
                        order.status = 1
                    else:
                        buy_order.status = 2
                        buy_order.save()

                        profile.earning += order.price*quantity
                        buy_profile = get_object_or_404(Profile, user=buy_order.profile.user)
                        buy_profile.earning -= buy_order.price*quantity
                        buy_profile.save()

                        order.status = 2
                    order.save()

                    profile.dollar += price*quantity
                    profile.btc += quantity
                    profile.save()
                else:
                    messages.success(request, 'Invalid value! You do not have enough BTC or you have entered '
                                              'a value less than 1')
                    return redirect('new_order')

            else:
                if 0 < price*quantity <= profile.dollar:
                    sell_order = Order.objects.filter(type=2, price__lt=price, quantity=quantity, status=1) \
                        .order_by('-datetime') \
                        .order_by('price') \
                        .first()

                    if sell_order is None:
                        order.status = 1
                    else:
                        sell_order.status = 2
                        sell_order.save()

                        print(f' {profile.earning} {order.price*quantity}')
                        profile.earning -= order.price*quantity
                        print(profile.earning)
                        sell_profile = get_object_or_404(Profile, user=sell_order.profile.user)
                        print(f' {sell_profile.earning} {sell_order.price*quantity}')
                        sell_profile.earning += sell_order.price*quantity
                        print(sell_profile.earning)
                        sell_profile.save()

                        order.status = 2
                    order.save()

                    profile.dollar -= price*quantity
                    profile.btc -= quantity
                    profile.save()
                else:
                    messages.success(request, 'Invalid value! You do not have enough Dollars or you have entered '
                                              'a value less than 1')
                    return redirect('new_order')
                return redirect('home')


    else:
        form = OrderForm()
        return render(request, 'app/new_order.html', {'form': form,
                                                      'quantity_btc': f'{profile.btc:,}',
                                                      'quantity_dollar': f'{profile.dollar:,}'})


@login_required(login_url='/login/')
def get_active_orders(request):
    orders = Order.objects.filter(status=1).order_by('-datetime')
    json_order = {}
    buy = []
    sell = []
    for order in orders:
        if order.type == 1:
            buy_json = {
                'quantity': order.quantity,
                'price': order.price,
                'datetime': order.datetime,
                'profile': order.profile.user.username
            }
            buy.append(buy_json)
        else:
            sell_json = {
                'quantity': order.quantity,
                'price': order.price,
                'datetime': order.datetime,
                'profile': order.profile.user.username
            }
            sell.append(sell_json)

    json_order['buy'] = buy
    json_order['sell'] = sell
    json_pretty = json.dumps(json_order, cls=DjangoJSONEncoder, indent=4)
    return render(request, 'app/get_orders.html', {'orders': json_pretty})


@login_required(login_url='/login/')
def get_earnings(request):
    earnings = []
    profiles = Profile.objects.all().order_by('-earning')
    n = 1
    for profile in profiles:
        json_user_earning = {
            '#': n,
            'user': profile.user.username,
            'total_earning': f'${profile.earning}'
        }
        n += 1
        earnings.append(json_user_earning)
    json_pretty = json.dumps(earnings, indent=4)
    return render(request, 'app/get_earnings.html', {'earnings': json_pretty})
