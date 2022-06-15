# Import Models
from models.role import Role as RoleModel, Module as ModuleModel, Permissions as PermissionsModel

# Import Utilities
from faker import Faker

modules = [
    {
        'name': 'dashboard',
        'label': 'Dashboard',
        'permissions': [
            {
                'name': 'read',
                'label': 'Read',
            }
        ]
    },
    {
        'name': 'role',
        'label': 'Dashboard',
        'permissions': [
            {
                'name': 'create',
                'label': 'Create',
            },
            {
                'name': 'read',
                'label': 'Read',
            },
            {
                'name': 'update',
                'label': 'Update',
            },
            {
                'name': 'delete',
                'label': 'Delete',
            }
        ]
    },
    {
        'name': 'admin',
        'label': 'Dashboard',
        'permissions': [
            {
                'name': 'create',
                'label': 'Create',
            },
            {
                'name': 'read',
                'label': 'Read',
            },
            {
                'name': 'update',
                'label': 'Update',
            },
            {
                'name': 'delete',
                'label': 'Delete',
            }
        ]
    },
    {
        'name': 'client',
        'label': 'Dashboard',
        'permissions': [
            {
                'name': 'create',
                'label': 'Create',
            },
            {
                'name': 'read',
                'label': 'Read',
            },
            {
                'name': 'update',
                'label': 'Update',
            },
            {
                'name': 'delete',
                'label': 'Delete',
            }
        ]
    },
    {
        'name': 'country',
        'label': 'Dashboard',
        'permissions': [
            {
                'name': 'create',
                'label': 'Create',
            },
            {
                'name': 'read',
                'label': 'Read',
            },
            {
                'name': 'update',
                'label': 'Update',
            },
            {
                'name': 'delete',
                'label': 'Delete',
            }
        ]
    },
    {
        'name': 'currency',
        'label': 'Dashboard',
        'permissions': [
            {
                'name': 'create',
                'label': 'Create',
            },
            {
                'name': 'read',
                'label': 'Read',
            },
            {
                'name': 'update',
                'label': 'Update',
            },
            {
                'name': 'delete',
                'label': 'Delete',
            }
        ]
    }
]


class Role:

    def __init__(self):
        self.modules = modules

    def get_modules(self) -> list:
        """
        Get All The Module Configuration
        :return self.module:
        """
        return self.modules

    def get_module(self, name) -> dict:
        return next((mod for mod in self.modules if mod['name'] == name), None)

    def get_permissions(self, name) -> list:
        return self.get_module(name)['permissions']

    def get_permission(self, module_name, name) -> dict:
        return next((permission for permission in self.get_permissions(module_name) if permission['name'] == name), None)

    def get_super_admin_role(self) -> RoleModel:
        module_list = list()

        for module in self.modules:
            m = ModuleModel(
                name=module['name'],
                permissions=PermissionsModel(
                    create=self.get_permission(module['name'], 'create') and True or False,
                    read=self.get_permission(module['name'], 'read') and True or False,
                    update=self.get_permission(module['name'], 'update') and True or False,
                    delete=self.get_permission(module['name'], 'delete') and True or False
                )
            )

            module_list.append(m)

        return RoleModel(
            name='Super Admin',
            modules=module_list
        )

    def get_random_role(self) -> RoleModel:
        module_list = list()
        fake = Faker()
        for module in self.modules:
            m = ModuleModel(
                name=module['name'],
                permissions=PermissionsModel(
                    create=self.get_permission(module['name'], 'create') and fake.pybool() or False,
                    read=self.get_permission(module['name'], 'read') and (module['name'] == 'dashboard' and True or fake.pybool()) or False,
                    update=self.get_permission(module['name'], 'update') and fake.pybool() or False,
                    delete=self.get_permission(module['name'], 'delete') and fake.pybool() or False
                )
            )

            module_list.append(m)

        return RoleModel(
            name=fake.job(),
            modules=module_list
        )

    def get_random_roles(self, number) -> [RoleModel]:
        roles = list()
        for _ in range(number):
            roles.append(self.get_random_role())
        return roles

