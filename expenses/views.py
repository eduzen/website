from rest_framework import permissions, viewsets

from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.order_by("created_date").all()
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by("created_date").all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
