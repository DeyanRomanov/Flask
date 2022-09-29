from enum import Enum


class UserRole(Enum):
    complainer = "Complainer"
    approver = "Approver"
    admin = "Admin"


class State(Enum):
    pending = 'Pending'
    approved = 'Approved'
    rejected = 'Rejected'