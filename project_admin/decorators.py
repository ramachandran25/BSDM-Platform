from django.contrib.auth.decorators import user_passes_test

def is_project_admin(user):
    return user.is_authenticated and user.groups.filter(name='PROJECT_ADMIN').exists()
