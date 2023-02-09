from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from pprint import pprint

# BrainTree
import braintree

# Payme
from payme.cards.subscribe_cards import PaymeSubscribeCards
from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts

# apps
from orders.models import Order

from .forms import PaymeCartCreateForm, PaymeCartVerifyForm


client = PaymeSubscribeCards(base_url=settings.PAYME['PAYME_URL'], paycom_id=settings.PAYME['PAYME_ID'])

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def braintree_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.total_price

    if request.method == 'POST':
        # oluchenie tokena dlya sozdaniya  transzaksii
        nonce = request.POST.get('payment_method_nonce', None)
        # sozdaniya i soxraneniya tranzaksii
        result = braintree.Transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {'submit_for_settlement': True}
        })
        if result.is_success:
            # Отметка заказа как оплаченного.
            order.is_paid = True
            # Сохранение ID транзакции в заказе.
            order.transaction_code = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # Формирование одноразового токена для JavaScript SDK.
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})


def payment_done(request):
    pprint(request.body)
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')


# Payme views
def payme_cart_create(request):
    if request.method == 'POST':
        form = PaymeCartCreateForm(request.POST)
        if form.is_valid():
            create_resp = client._cards_create(
                number=str(form.cleaned_data['card_number']),
                expire=str(form.cleaned_data['card_expire']),
                save=True,
            )
            pprint(create_resp)
            print()
            print()
            print()
            get_verify_code_resp = client._card_get_verify_code(
                token=create_resp['result']['card']['token']
            )
            pprint(get_verify_code_resp)
            print()
            print()
            print()
            request.session['subscribe_token'] = create_resp['result']['card']['token']
            return redirect('payment:payme_verify')
    else:
        form = PaymeCartCreateForm()

    return render(request, 'payment/card_create.html', {'form': form})


def payme_verify(request):
    if request.method == 'POST':
        form = PaymeCartVerifyForm(request.POST)
        if form.is_valid():
            order_id = request.session['order_id']
            order = get_object_or_404(Order, id=order_id)
            token = request.session['subscribe_token']
            
            verify_resp = client._cards_verify(
                verify_code=form.cleaned_data['sms_code'],
                token=token
            )
            print()
            pprint(verify_resp)
            print()
            print()
            if 'result' in verify_resp.keys():
                rclient = PaymeSubscribeReceipts(
                    base_url=settings.PAYME['PAYME_URL'], 
                    paycom_id=settings.PAYME['PAYME_ID'],
                    paycom_key=settings.PAYME['PAYME_KEY']
                )
                resp = rclient._receipts_pay(
                    invoice_id=order.transaction_code,
                    token=token,
                    phone="998901304527"
                )
                pprint(resp)
                print()
                print()
                print('end receipts pay')
                if 'result' in resp.keys():
                    order.is_paid = True
                    order.save()
                    return redirect('payment:done')
    else:
        form = PaymeCartVerifyForm()

    return render(request, 'payment/card_verify.html', {'form': form})