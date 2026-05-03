from django.contrib import admin
from .models import CustomUser, Profile, EmailOtp, ContactMessage



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_writer',
        'is_writer_requested',
        'consent_given',
        'date_joined'
    )

    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_writer', 'is_writer_requested', 'consent_given')

    readonly_fields = ('date_joined', 'consent_timestamp')

    inlines = [ProfileInline]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__email',)



@admin.register(EmailOtp)
class EmailOtpAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at')
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)