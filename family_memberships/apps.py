from django.apps import AppConfig

class FamilyMembershipsConfig(AppConfig):
    # Define the default field type for auto-incrementing primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    # Name of the application
    name = 'family_memberships'
