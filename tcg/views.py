from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        'Title': 'PokeTrade',
    }
    return render(request, 'base/base.html', context=context)

