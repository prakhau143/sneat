from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from .forms import UnifiedLoginForm, UserRegistrationForm, MerchantForm, TransactionForm, ChangePasswordForm
from .models import Merchant, Transaction
from django.contrib.auth.models import User

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def is_merchant(user):
    return user.is_authenticated and user.is_staff and not user.is_superuser

def is_normal_user(user):
    return user.is_authenticated and not user.is_staff and not user.is_superuser

@csrf_protect
def unified_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('sneat_app:super_admin_dashboard')
        elif request.user.is_staff:
            return redirect('sneat_app:merchant_dashboard')
        else:
            return redirect('sneat_app:user_dashboard')
    
    if request.method == 'POST':
        form = UnifiedLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Debug: Print user info
            print(f"Login successful for user: {user.username}")
            print(f"Is superuser: {user.is_superuser}")
            print(f"Is staff: {user.is_staff}")
            
            # Redirect based on user type with explicit URL
            if user.is_superuser:
                messages.success(request, f'Welcome back, Super Admin {user.username}!')
                print("Redirecting to superadmin dashboard")
                return redirect('/super-admin/dashboard/')
            elif user.is_staff:
                messages.success(request, f'Welcome back, Merchant {user.get_full_name()}!')
                return redirect('sneat_app:merchant_dashboard')
            else:
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('sneat_app:user_dashboard')
        else:
            print(f"Login form errors: {form.errors}")
    else:
        form = UnifiedLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})

@csrf_protect
def register(request):
    if request.user.is_authenticated:
        return redirect('sneat_app:unified_login')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data.get('is_staff', False)
            user.save()
            
            # If merchant, create merchant profile
            if user.is_staff:
                Merchant.objects.create(
                    user=user,
                    business_name=f"{user.get_full_name()}'s Business",
                    status='active'
                )
            
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('sneat_app:unified_login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('sneat_app:unified_login')

@login_required
def user_dashboard(request):
    if not is_normal_user(request.user):
        messages.error(request, 'Access denied.')
        return redirect('sneat_app:unified_login')
    
    context = {
        'user': request.user,
        'total_transactions': Transaction.objects.filter(merchant__user=request.user).count(),
        'total_amount': Transaction.objects.filter(merchant__user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0,
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def merchant_dashboard(request):
    if not is_merchant(request.user):
        messages.error(request, 'Access denied.')
        return redirect('sneat_app:unified_login')
    
    try:
        merchant = request.user.merchant_profile
        context = {
            'user': request.user,
            'merchant': merchant,
            'total_transactions': merchant.transactions.count(),
            'total_revenue': merchant.transactions.filter(type='credit').aggregate(Sum('amount'))['amount__sum'] or 0,
            'recent_transactions': merchant.transactions.all()[:5],
        }
        return render(request, 'merchant/dashboard.html', context)
    except Merchant.DoesNotExist:
        messages.error(request, 'Merchant profile not found.')
        return redirect('sneat_app:unified_login')

# Super Admin Views
@login_required
@user_passes_test(is_superuser)
def super_admin_dashboard(request):
    try:
        # Debug: Print user info
        print(f"Superadmin dashboard accessed by: {request.user.username}")
        print(f"User is superuser: {request.user.is_superuser}")
        
        # Get statistics
        total_merchants = Merchant.objects.count()
        active_merchants = Merchant.objects.filter(status='active').count()
        total_transactions = Transaction.objects.count()
        total_revenue = Transaction.objects.filter(type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Recent data
        recent_merchants = Merchant.objects.all()[:5]
        recent_transactions = Transaction.objects.all()[:5]
        
        context = {
            'total_merchants': total_merchants,
            'active_merchants': active_merchants,
            'total_transactions': total_transactions,
            'total_revenue': total_revenue,
            'recent_merchants': recent_merchants,
            'recent_transactions': recent_transactions,
        }
        
        print(f"Dashboard context: {context}")
        return render(request, 'super_admin/dashboard.html', context)
        
    except Exception as e:
        print(f"Error in superadmin dashboard: {e}")
        messages.error(request, f'Dashboard error: {e}')
        return redirect('sneat_app:unified_login')

@login_required
@user_passes_test(is_superuser)
def merchant_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    merchants = Merchant.objects.all()
    
    if search_query:
        merchants = merchants.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(business_name__icontains=search_query)
        )
    
    if status_filter:
        merchants = merchants.filter(status=status_filter)
    
    paginator = Paginator(merchants, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'super_admin/merchant_list.html', context)

@login_required
@user_passes_test(is_superuser)
@csrf_protect
def merchant_add(request):
    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            try:
                # Create the user first
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=form.cleaned_data['password'],
                    is_staff=True  # Make them staff so they can access merchant dashboard
                )
                
                # Create the merchant profile
                merchant = form.save(commit=False)
                merchant.user = user
                merchant.save()
                
                messages.success(request, f'Merchant {user.get_full_name()} added successfully!')
                return redirect('sneat_app:merchant_list')
            except Exception as e:
                messages.error(request, f'Error creating merchant: {str(e)}')
    else:
        form = MerchantForm()
    
    return render(request, 'super_admin/merchant_form.html', {'form': form, 'title': 'Add Merchant'})

@login_required
@user_passes_test(is_superuser)
@csrf_protect
def merchant_edit(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)
    
    if request.method == 'POST':
        form = MerchantForm(request.POST, instance=merchant)
        if form.is_valid():
            try:
                # Update the user information
                user = merchant.user
                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                
                # Update password if provided
                if form.cleaned_data['password']:
                    user.set_password(form.cleaned_data['password'])
                
                user.save()
                
                # Update the merchant information
                form.save()
                
                messages.success(request, f'Merchant {user.get_full_name()} updated successfully!')
                return redirect('sneat_app:merchant_list')
            except Exception as e:
                messages.error(request, f'Error updating merchant: {str(e)}')
    else:
        form = MerchantForm(instance=merchant)
    
    return render(request, 'super_admin/merchant_form.html', {'form': form, 'merchant': merchant, 'title': 'Edit Merchant'})

@login_required
@user_passes_test(is_superuser)
@csrf_protect
def merchant_delete(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)
    
    if request.method == 'POST':
        merchant.delete()
        messages.success(request, 'Merchant deleted successfully!')
        return redirect('sneat_app:merchant_list')
    
    return render(request, 'super_admin/merchant_confirm_delete.html', {'merchant': merchant})

@login_required
@user_passes_test(is_superuser)
def merchant_toggle_status(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)
    merchant.status = 'inactive' if merchant.status == 'active' else 'active'
    merchant.save()
    
    status_text = 'activated' if merchant.status == 'active' else 'deactivated'
    messages.success(request, f'Merchant {status_text} successfully!')
    return redirect('sneat_app:merchant_list')

@login_required
@user_passes_test(is_superuser)
def transaction_list(request):
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    
    transactions = Transaction.objects.all()
    
    if search_query:
        transactions = transactions.filter(
            Q(merchant__user__username__icontains=search_query) |
            Q(merchant__business_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if type_filter:
        transactions = transactions.filter(type=type_filter)
    
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'type_filter': type_filter,
    }
    return render(request, 'super_admin/transaction_list.html', context)

@login_required
@user_passes_test(is_superuser)
@csrf_protect
def transaction_add(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('sneat_app:transaction_list')
    else:
        form = TransactionForm()
    
    return render(request, 'super_admin/transaction_form.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def reports(request):
    # Revenue statistics
    total_revenue = Transaction.objects.filter(type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_revenue = Transaction.objects.filter(
        type='credit',
        created_at__gte=timezone.now() - timedelta(days=30)
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Merchant statistics
    total_merchants = Merchant.objects.count()
    active_merchants = Merchant.objects.filter(status='active').count()
    inactive_merchants = Merchant.objects.filter(status='inactive').count()
    
    # Transaction statistics
    total_transactions = Transaction.objects.count()
    credit_transactions = Transaction.objects.filter(type='credit').count()
    debit_transactions = Transaction.objects.filter(type='debit').count()
    
    # Top merchants by revenue
    top_merchants = Merchant.objects.annotate(
        total_revenue=Sum('transactions__amount', filter=Q(transactions__type='credit'))
    ).order_by('-total_revenue')[:10]
    
    context = {
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'total_merchants': total_merchants,
        'active_merchants': active_merchants,
        'inactive_merchants': inactive_merchants,
        'total_transactions': total_transactions,
        'credit_transactions': credit_transactions,
        'debit_transactions': debit_transactions,
        'top_merchants': top_merchants,
    }
    return render(request, 'super_admin/reports.html', context)

@login_required
@user_passes_test(is_superuser)
@csrf_protect
def settings_profile(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['current_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, 'Password changed successfully!')
                return redirect('sneat_app:settings_profile')
            else:
                form.add_error('current_password', 'Current password is incorrect.')
    else:
        form = ChangePasswordForm()
    
    return render(request, 'super_admin/settings_profile.html', {'form': form})

# Legacy views for UI templates
def dashboard(request):
    return redirect('sneat_app:unified_login')

def login_view(request):
    return redirect('sneat_app:unified_login')

def register_view(request):
    return redirect('sneat_app:register')
