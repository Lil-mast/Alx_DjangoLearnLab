from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups(apps, schema_editor):
    # Get content type for Book model
    content_type = ContentType.objects.get_for_model(apps.get_model('bookshelf', 'Book'))
    
    # Get permissions
    can_view = Permission.objects.get(codename='can_view', content_type=content_type)
    can_create = Permission.objects.get(codename='can_create', content_type=content_type)
    can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
    can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)

    # Create groups
    viewers = Group.objects.create(name='Viewers')
    viewers.permissions.add(can_view)

    editors = Group.objects.create(name='Editors')
    editors.permissions.add(can_view, can_create, can_edit)

    admins = Group.objects.create(name='Admins')
    admins.permissions.add(can_view, can_create, can_edit, can_delete)

class Migration(migrations.Migration):
    dependencies = [
        ('bookshelf', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]