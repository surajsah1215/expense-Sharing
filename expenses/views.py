from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Expense

def add_expense(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type')
        participants = request.POST.getlist('participants')
        shares = request.POST.get('shares')

        user = User.objects.get(userId=user_id)
        expense = Expense.objects.create(user=user, amount=amount, expense_type=expense_type)

        if expense_type == Expense.EQUAL:
            expense.participants.add(*User.objects.all())
            expense.shares = amount / User.objects.count()
        elif expense_type == Expense.EXACT:
            if sum(map(float, participants)) != float(amount):
                return JsonResponse({'error': 'Total sum of shares must be equal to the total amount.'}, status=400)
            for participant_id, share in zip(participants, participants):
                participant = User.objects.get(userId=participant_id)
                expense.participants.add(participant)
        elif expense_type == Expense.PERCENT:
            if sum(map(float, participants)) != 100:
                return JsonResponse({'error': 'Total sum of percentage shares must be 100.'}, status=400)
            for participant_id, percent_share in zip(participants, participants):
                participant = User.objects.get(userId=participant_id)
                expense.participants.add(participant)
                expense.shares = (amount * percent_share) / 100

        expense.save()
        return JsonResponse({'message': 'Expense added successfully.'}, status=201)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def get_balances(request, user_id):
    user = User.objects.get(userId=user_id)
    balances = {}
    for other_user in User.objects.exclude(userId=user_id):
        balance = sum(expense.amount for expense in other_user.expense_set.filter(user=user))
        if balance != 0:
            balances[other_user.name] = round(balance, 2)
    return JsonResponse(balances)
