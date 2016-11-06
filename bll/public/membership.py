from bll.membership import MembershipProvider, Principal, Identity
from dal.public.membership import PublicMembershipStore


__all__ = ["PublicMembershipProvider", "PublicPrincipal", "PublicIdentity"]


class PublicMembershipProvider(MembershipProvider):
    """
    Represents a MembershipProvider for the public area of the website.
    """
    def get_membership_store(self):
        return PublicMembershipStore()

    def get_principal_type(self):
        return PublicPrincipal


class PublicPrincipal(Principal):
    """
    Represents a roro regular principal
    """
    def get_identity_type(self):
        return PublicIdentity


class PublicIdentity(Identity):
    """
    Represents a roro regular user.
    """