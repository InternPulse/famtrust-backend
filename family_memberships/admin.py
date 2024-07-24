from django.contrib import admin
from .models import FamilyGroup, FamilyMembership

class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at', 'owner_id')
    search_fields = ('name', 'description')

class FamilyMembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_id', 'user_id', 'family_group', 'joined_at')
    search_fields = ('user_id', 'family_group__name')

admin.site.register(FamilyGroup, FamilyGroupAdmin)
admin.site.register(FamilyMembership, FamilyMembershipAdmin)
