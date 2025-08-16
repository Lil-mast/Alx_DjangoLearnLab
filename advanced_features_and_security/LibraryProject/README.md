# Permission System Documentation

## Groups and Permissions

The application uses three main groups with the following permissions:

### Viewers
- `can_view`: Can view books

### Editors
- `can_view`: Can view books
- `can_create`: Can create new books
- `can_edit`: Can edit existing books

### Admins
- All permissions (view, create, edit, delete)

## How to Use

1. **Assign users to groups** via Django admin or programmatically:
   ```python
   user.groups.add(Group.objects.get(name='Editors'))