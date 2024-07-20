import uuid

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage


from .models import Account
from .forms import TransferForm

# Create your views here.

def index(request):
    accounts_list = Account.objects.all()
    paginator = Paginator(accounts_list, 25) # Show 25 contacts per page

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        accounts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        accounts = paginator.page(paginator.num_pages)
    context = {"accounts": accounts}
    return render(request, "accounts/index.html", context)

def detail(request, account_id: uuid):
    account = get_object_or_404(Account, pk=account_id)
    return render(request, "accounts/detail.html", {"account": account})

def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # If valid, save the transaction
                return redirect('account_list')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = TransferForm()

    return render(request, 'pages/transfer_funds.html', {'form': form})