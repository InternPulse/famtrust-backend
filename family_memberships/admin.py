from django.contrib import admin
from .models import FamilyGroup, Membership

class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at', 'owner_id')
    search_fields = ('name', 'description')

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_id', 'user_id', 'family_group', 'joined_at')  # Make sure these fields exist in your Membership model
    search_fields = ('user_id', 'family_group__name')

admin.site.register(FamilyGroup, FamilyGroupAdmin)
admin.site.register(Membership, MembershipAdmin)
