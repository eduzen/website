from rest_framework import viewsets
from rest_framework import permissions

from .serializers import ExpenseSerializer, CategorySerializer
from .models import Expense, Category


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.order_by('created_date').all()
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by('created_date').all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
