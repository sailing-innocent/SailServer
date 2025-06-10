# -*- coding: utf-8 -*-
# @file money.py
# @brief My Personal Money Calculation Task
# @author sailing-innocent
# @date 2025-04-23
# @version 1.0
# ---------------------------------

import numpy as np
from internal.model.finance.account import AccountData, fix_account_balance_impl
from internal.model.finance.transaction import read_transactions_impl
from internal.data.finance import TransactionData, transactions_money_iter
import logging
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils.money import Money, sumup
from typing import List
from decimal import Decimal

# 配置matplotlib支持中文字体
plt.rcParams["font.sans-serif"] = [
    "SimHei",
    "Microsoft YaHei",
    "DejaVu Sans",
]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号

logger = logging.getLogger(__name__)


# 计算等额本息方法计价下，初始Q经过利率R和n期数的计算后，得到每月还款金额
def per_mon(Q, R, n):
    return R * (1 + R) ** n / ((1 + R) ** n - 1) * Q


def fix_account_balance(db_func, account_id: int, fix_value: float = 0.0):
    logger.info(
        f"Fixing account balance for account_id={account_id} with fix_value={fix_value}"
    )
    fix_data = AccountData(id=account_id, balance=fix_value)

    try:
        db = next(db_func())
        result = fix_account_balance_impl(db, fix_data)
        logger.info(f"Fixed account balance: {result}")
        return result
    except Exception as e:
        logger.error(f"Error fixing account balance: {e}")
        raise e


def read_transaction(db_func):
    db = next(db_func())
    start_date_literal = "2025-02-20"
    end_date_literal = "2025-05-30"
    start_date = datetime.datetime.strptime(start_date_literal, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_literal, "%Y-%m-%d")

    transactions = read_transactions_impl(
        db,
        from_time=start_date.timestamp(),
        to_time=end_date.timestamp(),
        skip=0,
        limit=1000,
    )

    logger.info(
        f"Read {len(transactions)} transactions from {start_date_literal} to {end_date_literal}"
    )

    return "Done"


def fetch_sum_by_tags(db_func, tags: List[str], start_date, end_date) -> Money:
    db = next(db_func())
    transactions = read_transactions_impl(
        db,
        from_time=start_date.timestamp(),
        to_time=end_date.timestamp(),
        skip=0,
        limit=1000,
        _tags=tags,
    )

    logger.info(f"Read {len(transactions)} transactions with tags: {tags}")

    return sumup(transactions_money_iter(transactions))


def analyze_transaction_per_period(
    db_func, start_date_literal: str, end_date_literal: str
):
    result = {
        "start_date": start_date_literal,
        "end_date": end_date_literal,
        "data": {},
    }
    start_date = datetime.datetime.strptime(start_date_literal, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_literal, "%Y-%m-%d")

    parent_tag = "日用消耗"
    sub_tags = [
        "零食",
        "正餐",
        "大宗电器",
        "交通",
        "衣物",
        "人际交往",
        "医药健康",
        "杂费",
    ]
    all_sum = fetch_sum_by_tags(db_func, [parent_tag], start_date, end_date)
    sub_sums = {
        tag: fetch_sum_by_tags(db_func, [parent_tag, tag], start_date, end_date)
        for tag in sub_tags
    }
    result["sum"] = all_sum.value_str
    logger.info(f"Total sum for {parent_tag}: {all_sum.value_str} {all_sum.currency}")
    for tag, sub_sum in sub_sums.items():
        logger.info(f"Sum for {tag}: {sub_sum.value_str} {sub_sum.currency}")
        result["data"][f"{tag}"] = sub_sum.value_str

    res = all_sum
    for sub_sum in sub_sums.values():
        res -= sub_sum
    logger.info(f"Sum for 其他日常消耗: {res.value_str} {res.currency}")
    result["data"]["other"] = res.value_str

    return result


def analyze_project(
    db_func, proj_name: str, start_date_literal: str, end_date_literal: str
):
    proj_res = analyze_transaction_per_period(
        db_func, start_date_literal, end_date_literal
    )
    logger.info(
        f"Analyzed transactions from {start_date_literal} to {end_date_literal}: {proj_res}"
    )
    labels = [f"{k}:{v}" for k, v in proj_res["data"].items()]
    sizes = [Decimal(value) for value in proj_res["data"].values()]
    colors = plt.cm.tab20c.colors[: len(labels)]  # Use a colormap for colors

    fig = plt.figure(figsize=(8, 8))
    ax = plt.gca()  # Get current axes
    # figure
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.3),
    )

    ax.set_title(
        f"Transaction Analysis for {proj_name}: {proj_res['start_date']} to {proj_res['end_date']}",
        fontfamily="Times New Roman",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.legend(
        wedges,
        labels,
        title="Transaction Categories",
        loc="center",
        bbox_to_anchor=(0.4, -0.05, 0.2, 1),
    )
    # 在左上角添加总计标签
    ax.text(
        0.32,
        0.7,  # 位置坐标 (x, y)
        f"日常支出总计: {proj_res['sum']}",
        fontsize=14,
        fontweight="bold",
        fontfamily="SimHei",  # 使用中文字体
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7),
        transform=ax.transAxes,
        verticalalignment="top",
        horizontalalignment="left",
    )
    # remove too small labels
    for i, label in enumerate(texts):
        sum_sizes = sum(sizes)

        if sizes[i] < 0.05 * float(sum_sizes):
            label.set_visible(False)
            autotexts[i].set_visible(False)

    plt.setp(autotexts, size=10, weight="bold", color="white")
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.tight_layout()
    plt.show()
    fig.savefig(
        f"data/mid/self/transaction_analysis_{proj_name}_{start_date_literal}_to_{end_date_literal}.png",
        bbox_inches="tight",
    )

    logger.info("Transaction analysis completed successfully.")
    # Return a summary message
    logger.info(
        f"Transaction analysis from {start_date_literal} to {end_date_literal} completed successfully."
    )


def analyze_transaction(db_func):
    proj_configs = [
        {
            "project_name": "HD-01",
            "start_date_literal": "2025-02-20",
            "end_date_literal": "2025-05-30",
        },
        {
            "project_name": "HD-02",
            "start_date_literal": "2025-06-05",
            "end_date_literal": "2025-09-12",
        },
        {
            "project_name": "February",
            "start_date_literal": "2025-02-01",
            "end_date_literal": "2025-02-28",
        },
        {
            "project_name": "March",
            "start_date_literal": "2025-03-01",
            "end_date_literal": "2025-03-31",
        },
        {
            "project_name": "April",
            "start_date_literal": "2025-04-01",
            "end_date_literal": "2025-04-30",
        },
        {
            "project_name": "May",
            "start_date_literal": "2025-05-01",
            "end_date_literal": "2025-05-31",
        },
        {
            "project_name": "June",
            "start_date_literal": "2025-06-01",
            "end_date_literal": "2025-06-30",
        },
    ]
    for config in proj_configs:
        project_name = config["project_name"]
        start_date_literal = config["start_date_literal"]
        end_date_literal = config["end_date_literal"]
        logger.info(
            f"Analyzing project {project_name} from {start_date_literal} to {end_date_literal}"
        )
        analyze_project(db_func, project_name, start_date_literal, end_date_literal)

    return "Done"
