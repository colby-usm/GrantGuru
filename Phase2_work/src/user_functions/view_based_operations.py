'''
    File: view_based_operations.py
    Version: 8 November 2025
    Author: Colby Wirth
    Description:
        - Enforces RBAC
        - Defines Roles that can be held
        - Permission Class holds static methdos that dedices access
        - require_permission is a decorator function that can be attached to CRUD functions to enforce auto permission checks
        - Generated with the help of AI tools
'''
from enum import Enum
from typing import Optional


class Role(Enum):
    """Defines possible user roles in the system."""
    USER = "user"
    ADMIN = "admin"


class Entity(Enum):
    """Defines the core database entities for RBAC checks."""
    USERS = "users"
    RESEARCH_FIELDS = "research_fields"
    APPLICATION = "application"
    APPLICATION_DOCUMENTS = "application_documents"
    APPLICATION_DEADLINES = "application_deadlines"
    GRANTS = "grants"


class Permission:
    """Implements role-based permission checks for CRUD operations."""
    
    @staticmethod
    def can_read(role: Role, entity: Entity, user_id: str, resource_owner_id: Optional[str] = None) -> bool:
        """Check if the given role can read a resource."""
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
        """Check if the given role can create a resource."""
        if role == Role.ADMIN:
            return True
        
        if role == Role.USER:
            if entity in [Entity.APPLICATION, Entity.APPLICATION_DOCUMENTS]:
                return user_id == resource_owner_id
        
        return False
    
    @staticmethod
    def can_update(role: Role, entity: Entity, user_id: int, resource_owner_id: Optional[int] = None) -> bool:
        """Check if the given role can update a resource."""
        if role == Role.ADMIN:
            return True
        
        if role == Role.USER:
            if entity in [Entity.USERS, Entity.APPLICATION, Entity.APPLICATION_DOCUMENTS]:
                return user_id == resource_owner_id
        
        return False
    
    @staticmethod
    def can_delete(role: Role, entity: Entity, user_id: int, resource_owner_id: Optional[int] = None) -> bool:
        """Check if the given role can delete a resource."""
        if role == Role.ADMIN:
            return True
        
        if role == Role.USER:

            # Allow self-delete of their own user account
            if entity == Entity.USERS:
                return user_id == resource_owner_id
            # Allow deleting their own applications or documents
            if entity in [Entity.APPLICATION, Entity.APPLICATION_DOCUMENTS]:
                return user_id == resource_owner_id
        
        return False


def require_permission(action: str, entity: Entity):
    """Decorator to enforce RBAC before executing a CRUD operation.
    
    Args:
        action: One of 'read', 'create', 'update', 'delete'.
        entity: The Entity type being accessed.
    """
    def decorator(func):
        def wrapper(role: Role, user_id: str, resource_owner_id: Optional[int] = None, *args, **kwargs):
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
