import sqlalchemy as sa
from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.schema import ForeignKey
from dal.membership import MembershipStore

__all__ = ["app_user_session", "choice"]

meta = sa.MetaData()

# declares database entities to work with SqlAlchemy

account = sa.Table(
    "admin_user_account", meta,
    Column("id", sa.Integer, primary_key=True),
    Column("email", sa.String(50), nullable=False, unique=True),
    Column("username", sa.String(50), nullable=False, unique=True),
    Column("hashed_password", sa.String(68), nullable=False),
    Column("salt", sa.String(50), nullable=False),
    Column("creation_time", sa.DateTime, nullable=False),
    Column("password_reset_key", sa.String(36), nullable=True),
    Column("confirmation_key", sa.String(36), nullable=True),
    PrimaryKeyConstraint("id", name="admin_user_account_pkey"))


login_attempt = sa.Table(
    "admin_user_login_attempt", meta,
    Column("id", sa.Integer, primary_key=True),
    Column("user_id", sa.Integer, ForeignKey("admin_user_account.id"), nullable=False),
    Column("creation_time", sa.DateTime, nullable=False),
    Column("client_ip", sa.String(50), nullable=False),
    Column("client_info", sa.String, nullable=False),
)


session = sa.Table(
    "admin_user_session", meta,
    Column("id", sa.Integer, primary_key=True),
    Column("guid", sa.String, nullable=False),
    Column("user_id", sa.Integer, ForeignKey("admin_user_account.id"), nullable=True),
    Column("anonymous", sa.Boolean, nullable=False),
    Column("creation_time", sa.DateTime, nullable=False),
    Column("expiration_time", sa.DateTime, nullable=False),
    Column("client_ip", sa.String, nullable=False),
    Column("client_info", sa.String, nullable=False),
    sa.PrimaryKeyConstraint("id", name="admin_user_session_pkey"))


class AdminMembershipStore(MembershipStore):
    """
    A membership store for the public area of the web application.
    """
    session = session
    account = account
    login_attempt = login_attempt

