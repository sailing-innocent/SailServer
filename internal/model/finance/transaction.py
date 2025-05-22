from internal.data.finance import (
    Account,
    Transaction,
    AccountState,
    TransactionData,
    AccountData,
    TransactionState,
)
from internal.data.finance import _acc, _acc_inv, _htime
from internal.model.finance.account import read_from_account
from utils.money import Money

import time
import logging

logger = logging.getLogger(__name__)


def clean_all_impl(db):
    db.query(Transaction).delete()
    db.commit()


def validate_account_exists(db, account_id: int) -> bool:
    return db.query(Account).filter(Account.id == account_id).first() is not None


def trans_from_create(create: TransactionData):
    htime = _htime(create)
    init_state = TransactionState(0)
    from_acc_id = _acc(create.from_acc_id)
    to_acc_id = _acc(create.to_acc_id)
    return Transaction(
        from_acc_id=from_acc_id,
        to_acc_id=to_acc_id,
        prev_value="0.0",  # default
        value=create.value,
        description=create.description,
        tags=create.tags,
        state=init_state.value,
        htime=htime,
        ctime=time.time(),
        mtime=time.time(),
    )


def read_from_trans(trans: Transaction):
    tags = ""
    if trans.tags is not None:
        tags = trans.tags
    return TransactionData(
        id=trans.id,
        from_acc_id=_acc_inv(trans.from_acc_id),
        to_acc_id=_acc_inv(trans.to_acc_id),
        value=trans.value,
        prev_value=trans.prev_value,
        description=trans.description,
        tags=tags,
        state=trans.state,
        htime=trans.htime,
        ctime=trans.ctime,
        mtime=trans.mtime,
    )


def validate_transaction_impl(db, transaction_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    state = TransactionState(transaction.state)
    from_acc_id = _acc_inv(transaction.from_acc_id)
    to_acc_id = _acc_inv(transaction.to_acc_id)

    if db.query(Account).filter(Account.id == from_acc_id).first() is not None:
        state.set_from_acc_valid()
    else:
        state.unset_from_acc_valid()
    if db.query(Account).filter(Account.id == to_acc_id).first() is not None:
        state.set_to_acc_valid()
    else:
        state.unset_to_acc_valid()

    transaction.state = state.value
    db.commit()


def validate_transactions_impl(db):
    transactions = db.query(Transaction).all()
    for transaction in transactions:
        state = TransactionState(transaction.state)
        from_acc_id = _acc_inv(transaction.from_acc_id)
        to_acc_id = _acc_inv(transaction.to_acc_id)

        if db.query(Account).filter(Account.id == from_acc_id).first() is not None:
            state.set_from_acc_valid()
        else:
            state.unset_from_acc_valid()
        if db.query(Account).filter(Account.id == to_acc_id).first() is not None:
            state.set_to_acc_valid()
        else:
            state.unset_to_acc_valid()

        transaction.state = state.value
    db.commit()


def create_transaction_impl(db, transaction_create: TransactionData):
    transaction = trans_from_create(transaction_create)
    db.add(transaction)
    db.commit()
    # validate transaction
    validate_transaction_impl(db, transaction.id)
    db.refresh(transaction)
    return read_from_trans(transaction)


def read_transactions_impl(db, skip: int = 0, limit: int = 10):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.state != 0)
        .order_by(Transaction.htime.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [read_from_trans(transaction) for transaction in transactions]


def read_transaction_impl(db, transaction_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    return read_from_trans(transaction)


def read_transactions_by_label_impl(db, label: str, from_time: int, to_time: int):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.htime >= from_time)
        .filter(Transaction.htime <= to_time)
        .filter(Transaction.state != 0)
        .filter(Transaction.tags.like(f"%{label}%"))
        .order_by(Transaction.htime.desc())
        .all()
    )
    return [read_from_trans(transaction) for transaction in transactions]


def read_transactions_by_desp_impl(db, desp: str, from_time: int, to_time: int):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.htime >= from_time)
        .filter(Transaction.htime <= to_time)
        .filter(Transaction.state != 0)
        .filter(Transaction.description.like(f"%{desp}%"))
        .order_by(Transaction.htime.desc())
        .all()
    )
    return [read_from_trans(transaction) for transaction in transactions]


def label_transaction_impl(db, transaction_id: int, label: str, positive: bool = True):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    tags = transaction.tags
    if tags is None:
        tags = ""
    tags = tags.split(",")
    if positive:
        if label not in tags:
            tags.append(label)
    else:
        if label in tags:
            tags.remove(label)
    transaction.tags = ",".join(tags)

    db.commit()
    db.refresh(transaction)
    return


def delete_transaction_impl(db, transaction_id: int = None):
    if transaction_id is None:
        return None
    # db.query(Transaction).filter(Transaction.id == transaction_id).delete()
    # mark deprecate here
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    state = TransactionState(transaction.state)

    if state.is_from_acc_valid():
        state.unset_from_acc_valid()
        state.set_from_acc_deprecated()
    if state.is_to_acc_valid():
        state.unset_to_acc_valid()
        state.set_to_acc_deprecated()
    state.unset_from_acc_updated()
    state.unset_to_acc_updated()
    state.unset_from_acc_changed()
    state.unset_to_acc_changed()

    transaction.state = state.value
    db.commit()
    db.refresh(transaction)
    return read_from_trans(transaction)


def clear_invalid_trnasaction_impl(db):
    # invalid and not deprecated
    db.query(Transaction).filter(Transaction.state == 0).delete()
    db.commit()


def update_transaction_impl(
    db, transaction_id: int, transaction_update: TransactionData
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        return None

    # update state to changed
    state = TransactionState(transaction.state)

    # update state valid

    if state.is_from_acc_valid():
        if not state.is_from_acc_updated():
            # IF NOT UPDATE, update manually
            update_account_balance_impl(db, _acc_inv(transaction.from_acc_id))
        else:
            # IF UPDATED, unset for later update
            state.unset_from_acc_updated()
        state.set_from_acc_changed()

    if state.is_to_acc_valid():
        if not state.is_to_acc_updated():
            # IF NOT UPDATE, update manually
            update_account_balance_impl(db, _acc_inv(transaction.to_acc_id))
        else:
            # IF UPDATED, unset for later update
            state.unset_to_acc_updated()
        state.set_to_acc_changed()

    # if -1 means third party, write NULL
    htime = _htime(transaction_update)
    transaction.from_acc_id = _acc(transaction_update.from_acc_id)
    transaction.to_acc_id = _acc(transaction_update.to_acc_id)
    transaction.prev_value = transaction.value
    transaction.value = transaction_update.value
    transaction.description = transaction_update.description
    transaction.tags = transaction_update.tags
    transaction.state = state.value
    transaction.htime = htime
    transaction.mtime = int(time.time())
    db.commit()
    db.refresh(transaction)

    return read_from_trans(transaction)


# recalc account balance
def recalc_account_balance_impl(db, account_id: int) -> AccountData:
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None:
        return None

    balance_value = Money("0.0")
    for in_trans in account.in_transactions:
        state = TransactionState(in_trans.state)

        if not state.is_to_acc_valid():
            if state.is_to_acc_deprecated():
                continue
            else:
                state.set_to_acc_valid()

        balance_value += Money(in_trans.value)
        state.set_to_acc_updated()
        state.unset_to_acc_changed()
        in_trans.state = state.value

    for out_trans in account.out_transactions:
        state = TransactionState(out_trans.state)
        if not state.is_from_acc_valid():
            if state.is_from_acc_deprecated():
                continue
            else:
                state.set_from_acc_valid()
        balance_value -= Money(out_trans.value)
        state.set_from_acc_updated()
        state.unset_from_acc_changed()
        out_trans.state = state.value

    account.balance = balance_value.value_str
    account.mtime = int(time.time())
    db.commit()
    db.refresh(account)
    return read_from_account(account)


# update account balance via transaction
def update_account_balance_impl(db, account_id: int) -> AccountData:
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None:
        return None

    balance_value = Money(account.balance)
    for in_trans in account.in_transactions:
        state = TransactionState(in_trans.state)
        if state.is_to_acc_valid():
            if not state.is_to_acc_updated():
                balance_value += Money(in_trans.value)
                state.set_to_acc_updated()
            if state.is_to_acc_changed():
                balance_value -= Money(in_trans.prev_value)
            state.unset_to_acc_changed()
        else:
            if state.is_to_acc_deprecated():
                balance_value -= Money(in_trans.value)
                state.unset_to_acc_deprecated()
                # finally set to 0
        in_trans.state = state.value

    for out_trans in account.out_transactions:
        state = TransactionState(out_trans.state)
        if state.is_from_acc_valid():
            if not state.is_from_acc_updated():
                balance_value -= Money(out_trans.value)
                state.set_from_acc_updated()
            if state.is_from_acc_changed():
                balance_value += Money(out_trans.prev_value)
            state.unset_from_acc_changed()
        else:
            if state.is_from_acc_deprecated():
                balance_value += Money(out_trans.value)
                state.unset_from_acc_deprecated()
                # finally set to 0

        out_trans.state = state.value

    account.balance = balance_value.value_str
    account.mtime = int(time.time())

    db.commit()
    db.refresh(account)
    return read_from_account(account)


def fix_account_balance_impl(db, fix: AccountData) -> AccountData:
    logging.info(f"fixing account balance for account {fix.id}")
    id = fix.id
    balance = Money(fix.balance)
    # update balance before fix
    res = update_account_balance_impl(db, id)
    if res is None:
        return None
    account = db.query(Account).filter(Account.id == id).first()
    curr_balance = Money(account.balance)
    # fix balance
    to_fix = balance - curr_balance
    logger.info(f"fixing balance for account {id} by {to_fix.value_str}")
    # new transaction
    create_transaction_impl(
        db,
        TransactionData(
            from_acc_id=-1,
            to_acc_id=id,
            value=to_fix.value_str,
            description="balance fix",
            tags="",
            htime=1,
        ),
    )
    # update balance after fix
    update_account_balance_impl(db, id)
    db.refresh(account)
    return read_from_account(account)
