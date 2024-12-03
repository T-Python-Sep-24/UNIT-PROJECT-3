from django.contrib import admin
from .models import  Expense, Budget






@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'user', 'amount', 'date')  
    list_filter = ('category', 'user')   
    search_fields = ('note',)  
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'user', 'monthly_limit', 'created_at')  
    list_filter = ('category', 'user')  
    search_fields = ('category__name', 'user__username')  
