from .forms import NewEntryForm
from .models import Category, Retailer, Transaction, TransactionMethod
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

def basic_view(request):
    if request.method == 'POST':  # Form submit for adding a new transaction.
        form = NewEntryForm(request.POST)
        if form.is_valid():
            form.save_transaction()
            form = NewEntryForm()
    else:                           # Default view.
        form = NewEntryForm()

    context = {
        'entries': Transaction.objects.order_by('date'),
        'form': form
    }
    return render(request, 'finance/basic.html', context)



def populated_basic_view(request, target_id):
    transaction = Transaction.objects.get(id=target_id)
    # By default populate the form with current values.
    form = NewEntryForm(
        { 'date': transaction.date,
          'payment_method': transaction.transaction_method.id,
          'retailer': transaction.retailer.id,
          'total': transaction.total,
          'tax': transaction.tax,
          'categories': list(map(lambda x: x.id, transaction.categories.all())),
          'description': transaction.description
        })
    if request.method == 'POST':            # If submiting an edit form submit.
        print(request.POST)
        form = NewEntryForm(request.POST)   # Update form to have user entered values (for error messages).
        if form.is_valid():
            form.save_transaction(transaction_to_edit=transaction)
            return HttpResponseRedirect(reverse('finance:basic_view'))   # Exit edit mode via redirect.

    context = {
        'entries': Transaction.objects.order_by('date'),
        'form': form
    }
    return render(request, 'finance/basic.html', context)



@csrf_exempt
def sumbit_changes_in_table(request):
    """
    This view should only be acessed via ajax POST requests.

    It re-saves the total and description of the transaction whose id has also been
    submitted.

    The request should have the id of the transaction that is being edited,
    the [altered] total, and [altered] description.
    """
    if request.method == 'POST' and request.is_ajax():
        request_data = json.loads(request.POST.get('request_data'))
        print(request_data)

        # Udate the target's total and description.
        update_target = Transaction.objects.get(id=request_data['id'])
        update_target.total = request_data['total']
        update_target.description = request_data['description']
        update_target.save()

        return JsonResponse(request_data)
    else:
        return JsonResponse({'error': 'request method was not post.'})





@csrf_exempt
def submit_transaction_form(request):
    if request.method == 'POST' and request.is_ajax():
        request_data = json.loads(request.POST.get('request_data'))
        print(request_data)

        return JsonResponse({})
