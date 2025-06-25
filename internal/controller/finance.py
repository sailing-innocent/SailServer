# -*- coding: utf-8 -*-
# @file finance.py
# @brief The Finance Controller
# @author sailing-innocent
# @date 2025-05-21
# @version 1.0
# ---------------------------------

from __future__ import annotations
from litestar.dto import DataclassDTO
from litestar.dto.config import DTOConfig
from litestar import Controller, delete, get, post, put, Request
from litestar.exceptions import HTTPException

from internal.data.finance import AccountData, TransactionData
from internal.model.finance.account import (
    read_account_impl,
    read_accounts_impl,
    create_account_impl,
    update_account_balance_impl,
    recalc_account_balance_impl,
    fix_account_balance_impl,
    delete_account_impl,
)

from internal.model.finance.transaction import (
    read_transaction_impl,
    read_transactions_impl,
    create_transaction_impl,
    update_transaction_impl,
    delete_transaction_impl,
)
from sqlalchemy.orm import Session
from typing import Generator

# -------------
# Account
# -------------


class AccountDataWriteDTO(DataclassDTO[AccountData]):
    config = DTOConfig(exclude={"id", "balance", "ctime", "mtime"})


class AccountDataUpdateDTO(DataclassDTO[AccountData]):
    config = DTOConfig(exclude={"state", "ctime", "mtime", "prev_value"})


class AccountDataReadDTO(DataclassDTO[AccountData]):
    config = DTOConfig(exclude={"ctime", "state"})


class AccountController(Controller):
    dto = AccountDataWriteDTO
    return_dto = AccountDataReadDTO
    path = "/account"

    @get("/{account_id:int}")
    async def get_account(
        self,
        account_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> AccountData:
        """
        Get the account data.
        """
        try:
            db = next(router_dependency)
            account = read_account_impl(db, account_id)
            request.logger.info(f"Get account: {account}")
        except Exception as e:
            request.logger.error(f"Error getting account: {e}")
            return None
        if account is None:
            return None
        return account

    @get()
    async def get_account_list(
        self,
        router_dependency: Generator[Session, None, None],
        skip: int = 0,
        limit: int = 10,
    ) -> list[AccountData]:
        """
        Get the account data list.
        """
        db = next(router_dependency)
        accounts = read_accounts_impl(db, skip, limit)
        return accounts

    @post()
    async def create_account(
        self,
        data: AccountData,
        request: Request,
        router_dependency: Generator[Session, None, None],
    ) -> AccountData:
        """
        Create a new account data.
        """
        db = next(router_dependency)
        name = data.name.strip()  # only name is required
        if not name:
            request.logger.error("Account name cannot be empty.")
            raise HTTPException(status_code=400, detail="Account name cannot be empty.")
        if len(name) > 100:
            request.logger.error("Account name is too long.")
            raise HTTPException(status_code=400, detail="Account name is too long.")
        else:
            account = create_account_impl(db, AccountData(name=name))
        request.logger.info(f"Create account: {account}")
        if account is None:
            return None

        return account

    @get("/update_balance/{account_id:int}", dto=AccountDataUpdateDTO)
    async def update_account_balance(
        self,
        account_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> AccountData:
        """
        Update the account balance.
        """
        db = next(router_dependency)
        account = update_account_balance_impl(db, account_id)
        request.logger.info(f"Update account balance: {account}")
        if account is None:
            return None

        return account

    @get("/recalc_balance/{account_id:int}")
    async def recalc_account_balance(
        self,
        account_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> AccountData:
        """
        Recalculate the account balance.
        """
        db = next(router_dependency)
        account = recalc_account_balance_impl(db, account_id)
        request.logger.info(f"Recalculate account balance: {account}")
        if account is None:
            return None

        return account

    @post("/fix_balance", dto=AccountDataUpdateDTO)
    async def fix_account_balance(
        self,
        data: AccountData,
        request: Request,
        router_dependency: Generator[Session, None, None],
    ) -> AccountData:
        """
        Fix the account balance.
        """
        db = next(router_dependency)
        account = fix_account_balance_impl(db, data)
        request.logger.info(f"Fix account balance: {account}")
        if account is None:
            return None

        return account

    @delete("/{account_id:int}")
    async def delete_account(
        self,
        account_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> None:
        """
        Delete the account data.
        """
        db = next(router_dependency)
        account = delete_account_impl(db, account_id)
        request.logger.info(f"Delete account: {account}")
        return None


# -------------
# Transaction
# -------------


class TransactionDataWriteDTO(DataclassDTO[TransactionData]):
    config = DTOConfig(exclude={"id", "prev_value", "state", "ctime", "mtime"})


class TransactionDataReadDTO(DataclassDTO[TransactionData]):
    config = DTOConfig(exclude={"ctime", "prev_value", "state", "ctime", "mtime"})


class TransactionController(Controller):
    dto = TransactionDataWriteDTO
    return_dto = TransactionDataReadDTO
    path = "/transaction"

    @get("/{transaction_id:int}")
    async def get_transaction(
        self,
        transaction_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> TransactionData:
        """
        Get the transaction data.
        """
        try:
            db = next(router_dependency)
            transaction = read_transaction_impl(db, transaction_id)
            request.logger.info(f"Get transaction: {transaction}")
        except Exception as e:
            request.logger.error(f"Error getting transaction: {e}")
            return None
        if transaction is None:
            return None
        return transaction

    @get()
    async def get_transaction_list(
        self,
        router_dependency: Generator[Session, None, None],
        skip: int = 0,
        limit: int = 10,
    ) -> list[TransactionData]:
        """
        Get the transaction data list.
        """
        db = next(router_dependency)
        transactions = read_transactions_impl(db, skip, limit)
        return transactions

    @post()
    async def create_transaction(
        self,
        data: TransactionData,
        request: Request,
        router_dependency: Generator[Session, None, None],
    ) -> TransactionData:
        """
        Create a new transaction data.
        """
        db = next(router_dependency)
        transaction = create_transaction_impl(db, data)
        request.logger.info(f"Create transaction: {transaction}")
        if transaction is None:
            return None

        return transaction

    @put("/{transaction_id:int}")
    async def update_transaction(
        self,
        transaction_id: int,
        data: TransactionData,
        request: Request,
        router_dependency: Generator[Session, None, None],
    ) -> TransactionData:
        """
        Update the transaction data.
        """
        db = next(router_dependency)
        transaction = update_transaction_impl(db, transaction_id, data)
        request.logger.info(f"Update transaction: {transaction}")
        if transaction is None:
            return None

        return transaction

    @delete("/{transaction_id:int}")
    async def delete_transaction(
        self,
        transaction_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> None:
        """
        Delete the transaction data.
        """
        db = next(router_dependency)
        transaction = delete_transaction_impl(db, transaction_id)
        request.logger.info(f"Delete transaction: {transaction}")
        return None
