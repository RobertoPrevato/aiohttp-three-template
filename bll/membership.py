"""
 Copyright 2016, Roberto Prevato roberto.prevato@gmail.com

 This module contains core classes for authentication and authorization strategies, and session management.
"""
import random
import hashlib
import re
import datetime
import uuid
from collections import OrderedDict, namedtuple
from core import require_params
from core.collections.bunch import Bunch
from core.exceptions import ArgumentNullException, InvalidOperation


AuthenticationResult = namedtuple("AuthenticationResult", ["principal", "session"])


class Session:
    """
    Generic object used for session management.
    """
    def __init__(self, obj_id, guid, userkey, expiration, anonymous):
        self.id = obj_id
        self.guid = guid
        self.userkey = userkey
        self.expiration = expiration
        self.anonymous = anonymous

    @classmethod
    def from_dict(cls, data):
        """
        Returns an instance of Session, from a dictionary.

        :param data: session data in dictionary.
        :return: Session
        """
        return cls(data.get("id"),
                   data.get("guid"),
                   data.get("userkey"),
                   data.get("expiration_time"),
                   data.get("anonymous"))


class Principal:
    """
    The principal object represents the security context under which code is running.
    Applications that implement role-based security grant rights based on the role associated with a principal object.

    Generic security principal used to implement authentication.
    """
    def __init__(self, _id, identity_data, session, authenticated):
        self.id = _id
        self.identity = self.get_identity_type().from_dict(identity_data) \
            if identity_data is not None else AnonymousIdentity()
        self.culture = self.identity.culture
        self.session = session
        self.authenticated = authenticated

    def get_identity_type(self):
        """
        Returns the type of Identity used by this Principal.
        """
        return Identity

    def has_any_role(self, roles):
        """
        Returns true if the principal identity has any of the given roles, false otherwise.

        :param roles: roles to check
        :return: boolean
        """
        if not roles:
            raise ArgumentNullException("roles")
        if self.identity is None or self.identity.roles is None:
            return False
        return any(self.is_in_role(x) for x in roles)

    def has_all_role(self, roles):
        """
        Returns true if the principal identity has all of the given roles, false otherwise.

        :param roles: roles to check
        :return: boolean
        """
        if not roles:
            raise ArgumentNullException("roles")
        if self.identity is None or self.identity.roles is None:
            return False
        return all(self.is_in_role(x) for x in roles)

    def is_in_role(self, role):
        """
        Returns true if the principal identity has a role, false otherwise.

        :param role: string role name.
        :return: bool
        """
        if self.identity is None or self.identity.roles is None:
            return False
        return role in self.identity.roles


class Identity:
    """
    The identity object encapsulates information about the user or entity being validated.
    """
    def __init__(self,
                 _id,
                 email,
                 culture,
                 roles,
                 opts,
                 created_timestamp):
        self.id = _id
        self.email = email
        self.culture = culture
        self.roles = roles
        self.opts = opts
        self.created = created_timestamp
        pass

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("id"),
                   data.get("email"),
                   data.get("culture"),
                   data.get("roles"),
                   data.get("opts"),
                   data.get("timestamp"))


class AnonymousIdentity(Identity):
    """
    Generic anonymous identity
    """
    def __init__(self):
        super().__init__(None, None, None, None, None, None)


class MembershipProvider:
    """
    Provides business logic to provide user authentication.

    It can be used to handle global authentication; or per-area authentication.
    Contains business logic for Login, Logout, ChangePassword.
    """

    defaults = {
        "host": None,  # the host used when generating emails
        "short_time_expiration": 1e3 * 60 * 20,
        "long_time_expiration": 1e3 * 60 * 60 * 24 * 365,
        "failed_login_attempts_limit": 4,
        "minutes_limit": 15,
        "requires_account_confirmation": False
    }

    def __init__(self):
        store = self.get_membership_store()
        options = self.get_options()
        require_params(store=store)
        if options is None:
            options = {}
        params = dict(self.defaults, **options)
        self.validate_store(store)
        self.store = store
        self.options = Bunch()
        self.options.merge(params)
        self.principal_type = self.get_principal_type()

    def get_membership_store(self):
        """
        Returns the membership store used by this membership provider.

        This method must be implemented in subclasses.
        """
        name = type(self).__name__
        raise NotImplementedError("{} does not implement 'get_membership_store'.".format(name))

    def get_options(self):
        """
        Returns options to override the default parameters.
        """
        return {}

    def get_principal_type(self):
        """
        Returns the membership store used by this membership provider.

        This method can be implemented to set specific Principal types by implementation.
        """
        return Principal

    @staticmethod
    def get_hash(password, salt):
        """
        Returns an hashed version of password, created using the given salt

        :param password: original password, to obfuscate with the given salt
        :param salt: salt to use to hash a password
        :return: hashed version of password
        """
        key = (password + salt).encode("utf-8")
        return hashlib.sha224(key).hexdigest()

    @staticmethod
    def get_new_salt():
        """
        Returns a new salt to be used to hash password

        :return: {String} new salt to be used to hash passwords
        """
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return ''.join(random.choice(alphabet) for _ in range(16))

    @staticmethod
    def validate_store(store):
        """
        Validates the store option passed when instantiating a MembershipProvider.
        :param store: store
        """
        # TODO: use abstract class!?
        req = ["get_account",
               "get_accounts",
               "get_session",
               "get_session_by_guid",
               "create_account",
               "update_account",
               "create_session",
               "destroy_session",
               "save_session_data",
               "get_session_data",
               "get_failed_login_attempts",
               "save_login_attempt"]
        for name in req:
            if not hasattr(store, name):
                raise Exception("The given store does not implement `" + name + "` member")

    def get_account(self, userkey):
        """
        Gets the account with the given key.
        :param userkey: key of the user (e.g. email or username)
        """
        data = self.store.get_account(userkey)
        if data is None:
            return None
        result = Bunch()
        result.merge(data)
        return result

    def get_account_by_id(self, account_id):
        """
        Gets the account details by id
        :param account_id: account id
        :return: account
        """
        data = self.store.get_account_by_id(account_id)
        if data is None:
            return None
        del data["salt"]
        del data["hash"]
        result = Bunch()
        result.merge(data)
        return result

    def get_accounts(self, options):
        """
        Gets the list of all application accounts.
        """
        # define searchable properties
        options["search_properties"] = ["email", "roles"]
        data = self.store.get_accounts(options)
        # NB !!!
        # Salt and hashed password must be kept private in this case.
        for item in data.subset:
            self.prepare_account_data(item)
        return data

    def get_sessions(self, options):
        """
        Gets the list of current user sessions.
        """
        # define searchable properties
        options["search_properties"] = ["email", "client_data.user_agent", "client_ip"]
        data = self.store.get_sessions(options)
        for o in data.subset:
            if o["client_data"]:
                o["user_agent"] = o["client_data"]["user_agent"]
            else:
                o["user_agent"] = ""
            del o["client_data"]
        return data

    def prepare_account_data(self, account):
        """
        Prepares account data, to share it outside of bll.
        Salt and hashed password must be never get out of bll.
        """
        del account["salt"]
        del account["hash"]
        if "roles" not in account:
            account["roles"] = []
        return account

    def validate_userkey(self, userkey):
        if userkey is None or re.match("^\s*$", userkey):
            return False
        return True

    def get_account_defaults(self):
        return {}

    def create_account(self, userkey, password, data=None, roles=None, lang="en"):
        """
        Creates a new user account.

        :param userkey: key of the user (e.g. email or username)
        :param password: account clear password (e.g. user defined password)
        :param data: dict, optional account data
        :return:
        """
        if not self.validate_userkey(userkey) or not self.validate_password(password):
            return False, "InvalidParameter"

        # verify that an account with the same key doesn't exist already
        account_data = self.store.get_account(userkey)
        if account_data is not None:
            return False, "AccountAlreadyExisting"
        if data is None:
            data = {}
        if roles is None:
            roles = []
        salt = self.get_new_salt()
        hashedpassword = self.get_hash(password, salt)
        data = dict(self.get_account_defaults(), **data)

        if self.options.requires_account_confirmation:
            # set a confirmation token inside the account data
            confirmation_token = str(uuid.uuid1())
            data["confirmation_token"] = confirmation_token

        account_data = self.store.create_account(userkey, hashedpassword, salt, data, roles)

        # TODO: if desired, implement send email logic
        return True, account_data

    def is_password_correct(self, account_id, password):
        require_params(account_id=account_id, password=password)

        if not self.validate_password(password):
            return False

        account_data = self.store.get_account_by_id(account_id)
        if account_data is None:
            raise ValueError("AccountNotFound")

        hsh = self.get_hash(password, account_data["salt"])
        if account_data["hash"] != hsh:
            return False
        return True

    def update_password(self, userkey, password):
        """
        Updates the password for the account with the given key.

        :param userkey: key of the user (e.g. email or username)
        :param password: account clear password (e.g. user defined password)
        :return:
        """
        if not self.validate_userkey(userkey) or not self.validate_password(password):
            return False, "InvalidParameter"

        account_data = self.store.get_account(userkey)
        if account_data is None:
            return False, "Account not found"
        salt = account_data["salt"]
        hashedpassword = self.get_hash(password, salt)
        self.store.update_account(userkey, {"hash": hashedpassword})
        return True, ""

    def delete_account(self, userkey):
        """
        Deletes the account with the given userkey
        :param userkey: the user key (email address or username)
        :return: success, error
        """
        account = self.store.get_account(userkey)
        if account is None:
            return False, "AccountNotFound"
        self.store.delete_account(userkey)
        return True, None

    def delete_account_with_validation(self, account_id, current_password, lang="en"):
        """
        Deletes the account with the given id, validating its password.
        :param account_id:
        :param current_password:
        :return:
        """
        account = self.store.get_account_by_id(account_id)
        if account is None:
            return False, "AccountNotFound"
        hsh = self.get_hash(current_password, account["salt"])
        if account.get("hash") != hsh:
            return False, "InvalidPassword"

        # delete the account
        deleted = self.store.delete_account_by_id(account_id)
        if not deleted:
            return False, "NoDocumentDeleted"

        # TODO: if desired, implement farewell email here
        return True, None

    def confirm_account(self, account_id, confirmation_token):
        """
        Confirms the account with the given id and using the given confirmation token.
        """
        if not account_id or account_id.isspace():
            raise ArgumentNullException("account_id")
        if not confirmation_token or confirmation_token.isspace():
            raise ArgumentNullException("confirmation_token")

        account_data = self.store.get_account_by_id(account_id)
        if not account_data:
            raise ValueError("Account not found")

        if account_data.get("confirmed") is True:
            return True

        if account_data.get("confirmation_token") != confirmation_token:
            raise ValueError("Invalid confirmation token for account `%s`" % account_id)

        self.store.update_account_by_id(account_id, {
            "confirmed": True
        }, unset_data={"confirmation_token": ""})
        return True

    def ban_account(self, userkey):
        """
        Bans the account with the given userkey.
        :param userkey: the user key (email address or username)
        :return: success, error
        """
        return self.update_account(userkey, {
            "banned": True
        })

    def update_account(self, userkey, data):
        """
        Updates the account with the given key; setting the data.
        :param userkey: the user key (email address or username)
        :param data: account data to update
        :return: self
        """
        account = self.store.get_account(userkey)
        if account is None:
            return False, "AccountNotFound"
        self.store.update_account(userkey, data)
        return True, None

    def try_login(self, userkey, password, remember, client_ip, client_data=None, check_password=True):
        """
        Tries to perform a login for the user with the given key (e.g. email or username); password;
        :param userkey: the user key (email address or username)
        :param password:
        :param remember: whether to have a longer expiration time or not
        :param client_ip: ip of the client for which the function has been called
        :param client_data: optional client data
        :param options: extra options
        :return:
        """
        # get account data
        account_data = self.get_account(userkey)
        if account_data is None:
            return False, "WrongCombo"

        login_attempts = self.get_failed_login_attempts(userkey)
        too_many_attempts = self.options.failed_login_attempts_limit <= login_attempts
        if too_many_attempts:
            # log information

            return False, "TooManyAttempts"
            # error: too many attempts in the last minutes, for this user

        if check_password:
            # generate hash of given password, appending salt
            hsh = self.get_hash(password, account_data.salt)
            if account_data.hash != hsh:
                # the key exists, but the password is wrong
                self.report_login_attempt(userkey, client_ip)
                # exit
                return False, "WrongCombo"

        # check if the account is confirmed
        if self.options.requires_account_confirmation and not account_data.confirmed:
            return False, "RequireConfirmation"

        # check if the account was banned
        if hasattr(account_data, "banned") and account_data.banned is True:
            return False, "BannedAccount"

        # get session expiration
        expiration = self.get_new_expiration(remember)
        # save session
        session = self.store.create_session(userkey, expiration, client_ip, client_data)
        session = Session.from_dict(session)

        del account_data.salt
        del account_data.hash
        principal = self.principal_type

        # TODO: if desired, implement sending of email here "new login from..."

        return True, AuthenticationResult(
            principal(account_data.id,
                      account_data,
                      session,
                      True),
            session
        )

    def report_login_attempt(self, userkey, client_ip):
        """
        Reports a login attempt, storing it in the persistence layer.

        :param userkey: the user key (email address or username)
        :param client_ip: ip of the client
        """
        now = datetime.datetime.utcnow()
        self.store.save_login_attempt(userkey, client_ip, now)
        return self

    def validate_password_reset_token(self, account_id, token):
        account_data = self.store.get_account_by_id(account_id)
        if account_data is None:
            return False, "AccountNotFound"

        password_reset_token = account_data.get("passwordResetToken")
        if not password_reset_token or password_reset_token.isspace():
            return False, "MissingPasswordResetToken"

        if password_reset_token != token:
            return False, "InvalidToken"

        return True, None

    def change_password(self, account_id, current_password, password_one, password_two):
        """
        This function is used when a user wants to change a password, using the current password
        """
        require_params(account_id=account_id,
                       current_password=current_password,
                       password_one=password_one,
                       password_two=password_two)

        account_data = self.store.get_account_by_id(account_id)
        if account_data is None:
            raise InvalidOperation("Account not found")

        # validate current password
        if not self.is_password_correct(account_id, current_password):
            raise ValueError("WrongPassword")

        # validate passwords
        valid_passwords, error = self.validate_passwords(password_one, password_two)
        if not valid_passwords:
            raise ValueError("Passwords are not valid: " + error)

        # update account password
        salt = self.get_new_salt()
        hashedpassword = self.get_hash(password_one, salt)
        # commit the change:
        self.store.change_password(account_id, hashedpassword, salt)
        return True, None

    def commit_password_reset(self, account_id, token, password_one, password_two):
        """
        This function is used when a user requested a password change, using a token that was sent by email.
        It validates a token that was set previously.

        :param account_id: id of the account of which the password should be changed
        :param token: password reset token
        :param password_one: first password
        :param password_two: password repetition
        :return:
        """
        require_params(account_id=account_id,
                       token=token,
                       password_one=password_one,
                       password_two=password_two)

        account_data = self.store.get_account_by_id(account_id)
        if account_data is None:
            raise InvalidOperation("Account not found")

        password_reset_token = account_data.get("passwordResetToken")
        if not password_reset_token or password_reset_token.isspace():
            raise InvalidOperation("Password reset token not initialized")

        if password_reset_token != token:
            raise ValueError("Invalid password reset token")

        # validate passwords
        valid_passwords, error = self.validate_passwords(password_one, password_two)
        if not valid_passwords:
            raise ValueError("Passwords are not valid: " + error)

        salt = self.get_new_salt()
        hashedpassword = self.get_hash(password_one, salt)
        # commit the change:
        self.store.change_password(account_id, hashedpassword, salt)
        return True

    def get_failed_login_attempts(self, userkey):
        """
        Gets the number of failed login attempts for a userkey in the amount of minutes defined by MinutesLimit option.
        :param userkey: the user key (email address or username)
        """
        now = datetime.datetime.utcnow()
        ms = self.options.minutes_limit * 60 * 1e3
        start = now - datetime.timedelta(milliseconds=ms)
        count = self.store.get_failed_login_attempts(userkey, start, now)
        return count

    async def try_login_by_session_key(self, sessionkey):
        """
        Tries to perform login by user session key.
        :param sessionkey:
        :return: boolean, session, account
        """
        # returns bool, principal
        if sessionkey is None:
            return False, None

        session = await self.store.get_session_by_guid(sessionkey)
        if session is None:
            return False, None

        # convert into a class
        session = Session.from_dict(session)

        now = datetime.datetime.utcnow()
        if session.expiration < now:
            return False, None
        principal_type = self.principal_type
        if session.anonymous:
            return True, AuthenticationResult(
                principal_type(None,
                               None,
                               session,
                               False),
                session
            )

        # get account data
        account = await self.store.get_account(session.userkey)

        if account is None:
            return False, None

        # return session and account data
        principal_type = self.principal_type
        return True, AuthenticationResult(
            principal_type(account["id"],
                           account,
                           session,
                           True),
            session
        )

    async def initialize_anonymous_session(self, client_ip, client_data):
        """
        Initializes a session for an anonymous user.

        :param client_ip: ip of the client
        :param client_data: information about the client software
        :return:
        """
        expiration = self.get_new_expiration(True)
        user_id = None
        session_data = await self.store.create_session(user_id, expiration, client_ip, client_data)
        session = Session.from_dict(session_data)
        principal_type = self.principal_type
        return AuthenticationResult(
            principal_type(None, None, session, False),
            session
        )

    def get_new_expiration(self, remember=None):
        """
        Returns the expiration for a new session, based on the provider settings and if the user wants to be remembered.
        for longer or not.

        :param remember: boolean
        :return: datetime
        """
        if remember is None:
            remember = False
        now = datetime.datetime.utcnow()
        ms = self.options.long_time_expiration if remember else self.options.short_time_expiration
        expiration = now + datetime.timedelta(milliseconds=ms)
        return expiration

    def save_session_data(self, sessionkey, data):
        """
        Stores session data in the database.
        :param sessionkey: the key of the session
        :param data: dictionary of data to store in database
        :return:
        """
        self.store.save_session_data(sessionkey, data)
        return self

    def get_session_data(self, sessionkey):
        """
        Gets the data associated with the given session, in database.
        :param sessionkey: the key of the session
        :return: dict
        """
        return self.options.get_session_data(sessionkey)

    def destroy_session(self, sessionkey):
        """
        Destroys the session with the given key.
        :param sessionkey: key of the session to destroy.
        :return: self
        """
        self.store.destroy_session(sessionkey)
        return self

    def validate_new_passwords(self, pass_one, pass_two):
        if pass_one != pass_two:
            return False
        if not self.validate_password(pass_one):
            return False
        return True

    def validate_passwords(self, password_one, password_two):
        """
        Validates the two given passwords.

        :param password_one: first password written by user.
        :param password_two: password confirmation.
        :return: success, error
        """
        if not password_one or not password_two:
            return False, "missing password"
        if password_one != password_two:
            return False, "password mismatch"
        v = password_two
        valid = self.validate_password(v)
        if not valid:
            return False, "password too weak"
        return True, None

    def validate_password(self, password):
        """
        Validates a single value to see if it's suitable for a password.

        :param password: value to validate.
        """
        if not password or password.isspace():
            return False
        l = len(password)
        if l < 6:
            # too simple, either way
            return False

        if l > 50:
            # too long: the interface allows maximum 50 chars
            return False

        keys = OrderedDict.fromkeys(password).keys()
        keys_length = len(keys)

        if keys_length < 3:
            # the password is too weak, it contains less than 3 different types of character
            return False

        forbidden = {"password", "qwerty", "123456", "1234567"}
        if password.lower() in forbidden:
            return False
        return True