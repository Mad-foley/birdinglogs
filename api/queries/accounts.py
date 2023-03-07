from queries.db import pool
from models.accounts_model import (
    AccountIn,
    AccountOut,
    AccountOutWithPassword,
    Error,
)
from typing import List
from common.common import timestamp


class AccountQueries:
    def get_account_by_username(self, username: str) -> AccountOutWithPassword:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    result = cur.execute(
                        """
                        SELECT name, username, password, id
                        FROM users
                        WHERE username= %s;
                        """,
                        [username]
                    )
                    record = result.fetchone()
                    if record is None:
                        return {"message": "Could not get account"}
                    return AccountOutWithPassword(
                        name = record[0],
                        username=record[1],
                        hashed_password=record[2],
                        id=record[3]
                    )
        except Exception as e:
            return Error(message=str(e))


    def get_account_by_id(self, account_id: int) -> AccountOutWithPassword:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    result = cur.execute(
                        """
                        SELECT name, username, picture_url, created_on, id
                        FROM users
                        WHERE id = %s;
                        """,
                        [account_id]
                    )
                    record = result.fetchone()
                    print("*****GET BY ID**********", record)
                    if record is None:
                        return {"message": "Could not get account"}
                    return self.record_to_account_out(record)
        except Exception as e:
            return Error(message=str(e))

    def create_account(self, account: AccountIn, hashed_password: str) -> AccountOutWithPassword:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    result = cur.execute(
                        """
                        INSERT INTO users
                            (name, username, password, picture_url, created_on)
                        VALUES
                            (%s, %s, %s, %s, %s)
                        RETURNING id;
                        """,
                        [
                            account.name,
                            account.username,
                            hashed_password,
                            account.picture_url,
                            timestamp(),
                        ]
                    )
                    id = result.fetchone()[0]
                    return AccountOutWithPassword(
                        id = id,
                        name = account.name,
                        username=account.username,
                        hashed_password=hashed_password,
                        picture_url=account.picture_url,
                        created_on=timestamp(),
                    )
        except Exception as e:
            print(e)
            return Error(message=str(e))

    def delete_account(self, account_id: int) -> bool:
        try:
            with pool.connection () as conn:
                with conn.cursor() as cur:
                    result = cur.execute(
                        """
                        DELETE FROM users
                        WHERE id = $s;
                        """,
                        [account_id]
                    )
                    return True if result is not None else False

        except Exception as e:
            return Error(message=str(e))

    def record_to_account_out(self, record) -> AccountOutWithPassword:
        try:
            return AccountOutWithPassword(
                name=record[0],
                username=record[1],
                hashed_password=record[2],
                picture_url=record[3],
                created_on=record[4],
                id=record[5]
            )
        except Exception as e:
            return Error(message=str(e))