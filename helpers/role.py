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
        'label': 'Role',
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
        'label': 'Admin',
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
        'label': 'Client',
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
        'name': 'foreign_transaction',
        'label': 'Foreign Transaction',
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
        'name': 'local_transaction',
        'label': 'Local Transaction',
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
        'label': 'Country',
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
        'label': 'Currency',
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
        'name': 'account',
        'label': 'Account',
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
        'name': 'contact',
        'label': 'Contact',
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
        self.model = None

    def get_modules(self) -> list:
        """
        Get All The Module Configuration
        :return self.module:
        """
        return self.modules

    def get_module(self, name):
        return next((mod for mod in self.modules if mod['name'] == name), None)

    def get_permissions(self, name):
        return self.get_module(name)['permissions']

    def get_permission(self, module_name, name):
        return next((permission for permission in self.get_permissions(module_name) if permission['name'] == name), None)

    def get_permissions_from_model(self, name):
        permissions = name in self.model and self.model[name] or None
        return permissions

    def get_permission_from_model(self, module_name, name):
        permissions = self.get_permissions_from_model(module_name)
        permission = permissions is not None and name in permissions and permissions[name] or None
        return permission

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
            description='Some Description',
            status=True,
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
            description=fake.sentence(nb_words=10),
            status=fake.pybool(),
            modules=module_list
        )

    def get_prepared_modules_from_model(self, model):
        self.model = model
        module_list = list()
        for module in self.modules:
            m = ModuleModel(
                name=module['name'],
                permissions=PermissionsModel(
                    create=self.get_permission_from_model(module['name'], 'create') is not None and self.get_permission_from_model(module['name'], 'create') or False,
                    read=self.get_permission_from_model(module['name'], 'read') is not None and (module['name'] == 'dashboard' and True or self.get_permission_from_model(module['name'], 'read')) or False,
                    update=self.get_permission_from_model(module['name'], 'update') is not None and self.get_permission_from_model(module['name'], 'update') or False,
                    delete=self.get_permission_from_model(module['name'], 'delete') is not None and self.get_permission_from_model(module['name'], 'delete') or False
                )
            )

            module_list.append(m)
        return module_list

    def get_random_roles(self, number) -> [RoleModel]:
        roles = list()
        for _ in range(number):
            roles.append(self.get_random_role())
        return roles
