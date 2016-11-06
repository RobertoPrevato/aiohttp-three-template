"""
 Copyright 2016, Roberto Prevato roberto.prevato@gmail.com

 This module contains base classes for MembershipStore objects.
"""
import uuid
from datetime import datetime
from dal import get_client


class MembershipStore:
    """
    Provides methods to handle membership related data in the persistence layer.
    """
    session = None  # session entity
    account = None  # account entity

    async def get_account(self, account_id):
        account = self.account
        dbclient = get_client()
        async with dbclient.acquire() as conn:
            result = await conn.execute(
                account.select()
                .where(account.c.id == account_id))
            return await result.first()

    async def get_accounts(self, options):
        raise NotImplementedError

    async def create_account(self, userkey, hashedpassword, salt, data, roles=None):
        raise NotImplementedError

    async def update_account(self, userkey, data):
        raise NotImplementedError

    async def create_session(self, user_id, expiration, client_ip, client_info):
        """
        Creates a new session.

        :param user_id: user id
        :param expiration: expiration time
        :param client_ip: client ip
        :param client_info: information about the client software
        :return:
        """
        session = self.session
        data = dict(
            guid=uuid.uuid1(),
            user_id=user_id,
            anonymous=not user_id,
            expiration_time=expiration,
            client_ip=client_ip,
            client_info=client_info,
            creation_time=datetime.utcnow()
        )
        command = session.insert().values(**data)
        dbclient = get_client()
        async with dbclient.acquire() as conn:
            result = await conn.execute(command)
            id = await result.fetchone()
            data.update({
                "id": id[0]
            })
            return data

    async def destroy_session(self, sessionkey):
        raise NotImplementedError

    async def save_session_data(self, sessionkey, data):
        raise NotImplementedError

    async def get_session_data(self, sessionkey):
        raise NotImplementedError

    async def get_failed_login_attempts(self, userkey, start, end):
        """
        Gets the number of failed login attempts for a user with a given key, in the last minutes.

        :param userkey: key of the user for whom we are initializing the session
        :param start: start datetime to check for login attempts
        :param end: end datetime to check for login attempts
        :return:
        """
        raise NotImplementedError

    async def save_login_attempt(self, userkey, client_ip, time):
        """
        Stores a failed login attempt in database

        :param userkey: key of the user for whom the login attempt must be stored
        :param client_ip: ip of the client for which the method is invoked
        :param time: timestamp of the login attempt
        :return:
        """
        raise NotImplementedError

    async def get_session_by_guid(self, session_guid):
        session = self.session
        dbclient = get_client()
        async with dbclient.acquire() as conn:
            result = await conn.execute(
                session.select()
                .where(session.c.guid == session_guid))
            return await result.first()

    async def get_session(self, session_id):
        session = self.session
        dbclient = get_client()
        async with dbclient.acquire() as conn:
            result = await conn.execute(
                session.select()
                .where(session.c.id == session_id))
            return await result.first()