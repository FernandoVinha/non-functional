from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import PaymentRequestForm
from django.shortcuts import render, redirect

from rest_framework import viewsets, permissions
from .models import Transfer, PaymentRequest
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

@login_required
def transaction_report(request):
    user = request.user
    current_date = datetime.now()
    
    # Verifique se uma data específica foi fornecida na URL
    date_param = request.GET.get('date')  # Suponha que a URL tenha um parâmetro 'date'
    
    if date_param:
        try:
            date_param = datetime.strptime(date_param, '%Y-%m-%d')  # Formato da data na URL (ano-mês-dia)
            thirty_days_ago = date_param
        except ValueError:
            thirty_days_ago = current_date - timedelta(days=30)
    else:
        thirty_days_ago = current_date - timedelta(days=30)
    
    transactions = Transfer.objects.filter(user=user, data__gte=thirty_days_ago, data__lte=current_date).order_by('-data')
    
    context = {
        'transactions': transactions,
    }

    return render(request, 'transaction_report.html', context)


@login_required
def payment_request_list(request):
    user = request.user
    current_date = datetime.now()
    
    # Verifique se uma data específica foi fornecida na URL
    date_param = request.GET.get('date')  # Suponha que a URL tenha um parâmetro 'date'
    
    if date_param:
        try:
            date_param = datetime.strptime(date_param, '%Y-%m-%d')  # Formato da data na URL (ano-mês-dia)
            thirty_days_ago = date_param
        except ValueError:
            thirty_days_ago = current_date - timedelta(days=30)
    else:
        thirty_days_ago = current_date - timedelta(days=30)
    
    payment_requests = PaymentRequest.objects.filter(user=user, request_date__gte=thirty_days_ago, request_date__lte=current_date).order_by('-request_date')
    
    context = {
        'payment_requests': payment_requests,
    }

    return render(request, 'payment_request_list.html', context)


@login_required
def create_payment_request(request):
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
        if form.is_valid():
            payment_request = form.save(commit=False)
            payment_request.user = request.user  # Defina o usuário como o usuário logado
            payment_request.save()
            return redirect('payment_request_details', id=payment_request.id)  # Redirecione para a página de detalhes do pedido
    else:
        form = PaymentRequestForm()
    
    return render(request, 'create_payment_request.html', {'form': form})

@login_required
def payment_request_details(request, id):
    payment_request = get_object_or_404(PaymentRequest, id=id, user=request.user)

    context = {
        'payment_request': payment_request,
    }

    return render(request, 'payment_request_details.html', context)

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transfer.objects.filter(user=user)

class PaymentRequestViewSet(viewsets.ModelViewSet):
    queryset = PaymentRequest.objects.all()
    serializer_class = PaymentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PaymentRequest.objects.filter(user=user)

    @action(detail=True, methods=['post'])
    def generate_payment(self, request, pk=None):
        user = request.user
        payment_request = get_object_or_404(PaymentRequest, pk=pk, user=user)
        payment_request.payment_status = 'paid'
        payment_request.save()
        serializer = PaymentRequestSerializer(payment_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payment_details(self, request, pk=None):
        user = request.user
        payment_request = get_object_or_404(PaymentRequest, pk=pk, user=user)
        serializer = PaymentRequestSerializer(payment_request)
        return Response(serializer.data)

@login_required
class UserBalanceAPIView(APIView):
    def get(self, request):
        user = request.user

        received_amount = Transfer.objects.filter(user=user, received=True).aggregate(Sum('valor'))['valor__sum'] or 0
        spent_amount = Transfer.objects.filter(user=user, received=False).aggregate(Sum('valor'))['valor__sum'] or 0
        balance = received_amount - spent_amount

        serializer = UserBalanceSerializer({'balance': balance})
        return Response(serializer.data, status=status.HTTP_200_OK)