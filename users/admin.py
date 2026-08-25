from django.contrib import admin
from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'city', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'paid_course', 'paid_lesson', 'amount', 'stripe_payment_status', 'created_at')
    list_filter = ('stripe_payment_status', 'created_at')
    search_fields = ('user__email', 'stripe_session_id')
    readonly_fields = ('stripe_session_id', 'payment_url')
