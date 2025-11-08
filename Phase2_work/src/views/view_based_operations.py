from enum import Enum
from typing import Optional


class Role(Enum):
    USER = "user"
    ADMIN = "admin"


class Entity(Enum):
    USERS = "users"
    APPLICATION = "application"
    APPLICATION_DOCUMENTS = "application_documents"
    APPLICATION_DEADLINES = "application_deadlines"
    GRANTS = "grants"


class Permission:
    """Simple RBP permission checker"""
    
    @staticmethod
    def can_read(role: Role, entity: Entity, user_id: int, resource_owner_id: Optional[int] = None) -> bool:
        if role == Role.ADMIN:
            return True
        
        if role == Role.USER:
            if entity in [Entity.USERS, Entity.APPLICATION, Entity.APPLICATION_DOCUMENTS]:
                return user_id == resource_owner_id
            if entity in [Entity.APPLICATION_DEADLINES, Entity.GRANTS]:
                return True
        
        return False
    
    @staticmethod
    def can_create(role: Role, entity: Entity, user_id: int, resource_owner_id: Optional[int] = None) -> bool:
        if role == Role.ADMIN:
            return True
        
        if role == Role.USER:
            if entity in [Entity.APPLICATION, Entity.APPLICATION_DOCUMENTS]:
                return user_id == resource_owner_id
        
        return False
    
    @staticmethod
    def can_update(role: Role, entity: Entity, user_id: int, resource_owner_id: Optional[int] = None) -> bool:
        if role == Role.ADMIN:
            return True
        
        if role == Role.USER:
            if entity in [Entity.USERS, Entity.APPLICATION, Entity.APPLICATION_DOCUMENTS]:
                return user_id == resource_owner_id
        
        return False
    
    @staticmethod
    def can_delete(role: Role, entity: Entity, user_id: int, resource_owner_id: Optional[int] = None) -> bool:
        if role == Role.ADMIN:
            return True
        
        if role == Role.USER:
            if entity in [Entity.APPLICATION, Entity.APPLICATION_DOCUMENTS]:
                return user_id == resource_owner_id
        
        return False


def require_permission(action: str, entity: Entity):
    """Decorator to protect CRUD operations"""
    def decorator(func):
        def wrapper(role: Role, user_id: int, resource_owner_id: Optional[int] = None, *args, **kwargs):
            permission_check = {
                'read': Permission.can_read,
                'create': Permission.can_create,
                'update': Permission.can_update,
                'delete': Permission.can_delete
            }
            
            if permission_check[action](role, entity, user_id, resource_owner_id):
                return func(role, user_id, resource_owner_id, *args, **kwargs)
            else:
                raise PermissionError(f"User {user_id} with role {role.value} cannot {action} {entity.value}")
        
        return wrapper
    return decorator
