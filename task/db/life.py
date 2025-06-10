# -*- coding: utf-8 -*-
# @file life.py
# @brief Life Script
# @author sailing-innocent
# @date 2025-06-10
# @version 1.0
# ---------------------------------

import numpy as np
from internal.model.finance.transaction import read_transactions_impl
from internal.data.finance import transactions_money_iter
import logging
import datetime
from internal.model.health import read_weights_impl

import matplotlib.pyplot as plt
from utils.money import sumup
from utils.stat.regression import linear_regression_1d
from scipy.signal import correlate

logger = logging.getLogger(__name__)


def analyze_snack_weight_rel(db_func):
    """
    Analyze the relationship between snack outcome and weight increase
    """

    # Calcuate the Increase Rate of Weight for each period
    # Sumup the snack outcome for each period

    db = next(db_func())
    start_date_literal = "2025-02-20"
    end_date_literal = "2025-05-30"
    start_date = datetime.datetime.strptime(start_date_literal, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_literal, "%Y-%m-%d")
    # read daily result
    weights = read_weights_impl(
        db,
        start_time=start_date.timestamp(),
        end_time=end_date.timestamp(),
        _tag="daily",
    )
    logger.info(f"Read {len(weights)} daily weights from the database")
    x = np.array([w.htime for w in weights])
    y = np.array([float(w.value) for w in weights])
    # calcuate the gradient of y
    # plot data
    dydx = np.gradient(y, x)
    # normalize dydx
    dydx = dydx / np.max(np.abs(dydx)) * 100  # Normalize to percentage

    one_day = datetime.timedelta(days=1)
    sy = []
    for t in x:
        dt = datetime.datetime.fromtimestamp(t)

        transactions = read_transactions_impl(
            db,
            from_time=dt.timestamp(),
            to_time=(dt + one_day).timestamp(),
            _tags=["零食"],
        )
        sy.append(float(sumup(transactions_money_iter(transactions)).value))
        # sum up
    # normalize sy
    sy = sy / np.max(sy) * 100  # Normalize to percentage

    plt.figure(figsize=(10, 5))
    # plt.plot(x, y, label="Weight", color="blue")
    plt.plot(x, dydx, label="Weight Increase Rate", color="orange")
    plt.plot(x, sy, label="Snack Outcome", color="red", marker="x")
    plt.xlabel("Time")
    # the show format x -> timestamp -> %Y-%m-%d
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.xticks(rotation=45)
    plt.title("Weight and Weight Increase Rate Over Time")
    plt.legend()
    plt.grid()
    plt.show()  # for each day, get the snack outcome and weight increase rate pair
    pairs = []
    for i in range(len(x)):
        pairs.append((sy[i], dydx[i]))  # Perform correlation analysis
    logger.info("=== 相关性分析结果 ===")

    # 1. 线性相关系数
    correlation_coeff = np.corrcoef(sy, dydx)[0, 1]
    logger.info(f"皮尔逊相关系数: {correlation_coeff:.4f}")

    # 2. 线性回归分析
    try:
        k, b = linear_regression_1d(np.array(sy), np.array(dydx))
        logger.info(f"线性回归方程: dydx = {k:.4f} * sy + {b:.4f}")

        # 计算R²决定系数
        y_pred = k * np.array(sy) + b
        ss_res = np.sum((dydx - y_pred) ** 2)
        ss_tot = np.sum((dydx - np.mean(dydx)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        logger.info(f"R² 决定系数: {r_squared:.4f}")

    except Exception as e:
        logger.error(f"线性回归分析失败: {e}")
        k, b = 0, 0

    # 3. 滞后相关性分析 (Cross-correlation)
    logger.info("=== 滞后相关性分析 ===")

    # 计算互相关
    cross_corr = correlate(dydx, sy, mode="full")
    lags = np.arange(-len(sy) + 1, len(sy))

    # 标准化互相关
    cross_corr_normalized = cross_corr / (np.std(sy) * np.std(dydx) * len(sy))

    # 找到最大相关性及其对应的滞后
    max_corr_idx = np.argmax(np.abs(cross_corr_normalized))
    max_lag = lags[max_corr_idx]
    max_corr_value = cross_corr_normalized[max_corr_idx]

    logger.info(f"最大相关性: {max_corr_value:.4f}")
    logger.info(f"对应滞后: {max_lag} 天")
    if max_lag > 0:
        logger.info("零食支出滞后于体重变化")
    elif max_lag < 0:
        logger.info("零食支出领先于体重变化")
    else:
        logger.info("零食支出与体重变化同步")

    # 4. 可视化分析结果
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # 子图1: 散点图和线性回归
    axes[0, 0].scatter(sy, dydx, alpha=0.6, color="blue")
    if k != 0 or b != 0:
        sy_range = np.linspace(min(sy), max(sy), 100)
        regression_line = k * sy_range + b
        axes[0, 0].plot(
            sy_range,
            regression_line,
            "r--",
            label=f"y = {k:.4f}x + {b:.4f}\\nR² = {r_squared:.4f}",
        )
    axes[0, 0].set_xlabel("零食支出 (归一化)")
    axes[0, 0].set_ylabel("体重增长率 (归一化)")
    axes[0, 0].set_title(f"散点图 (相关系数: {correlation_coeff:.4f})")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # 子图2: 时间序列对比
    time_days = np.arange(len(x))
    axes[0, 1].plot(time_days, sy, "r-", label="零食支出", marker="o", markersize=3)
    axes[0, 1].plot(time_days, dydx, "b-", label="体重增长率", marker="s", markersize=3)
    axes[0, 1].set_xlabel("时间 (天)")
    axes[0, 1].set_ylabel("归一化值")
    axes[0, 1].set_title("时间序列对比")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # 子图3: 互相关函数
    # 只显示合理范围的滞后
    display_range = min(30, len(sy) // 2)
    display_mask = (lags >= -display_range) & (lags <= display_range)
    axes[1, 0].plot(lags[display_mask], cross_corr_normalized[display_mask], "g-")
    axes[1, 0].axvline(
        x=max_lag, color="r", linestyle="--", label=f"最大相关滞后: {max_lag}天"
    )
    axes[1, 0].axhline(y=0, color="k", linestyle="-", alpha=0.3)
    axes[1, 0].set_xlabel("滞后 (天)")
    axes[1, 0].set_ylabel("标准化互相关")
    axes[1, 0].set_title("互相关函数")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # 子图4: 残差分析
    if k != 0 or b != 0:
        residuals = dydx - (k * np.array(sy) + b)
        axes[1, 1].scatter(sy, residuals, alpha=0.6, color="purple")
        axes[1, 1].axhline(y=0, color="r", linestyle="--")
        axes[1, 1].set_xlabel("零食支出 (归一化)")
        axes[1, 1].set_ylabel("残差")
        axes[1, 1].set_title("残差分析")
        axes[1, 1].grid(True, alpha=0.3)
    else:
        axes[1, 1].text(
            0.5,
            0.5,
            "无法进行残差分析",
            transform=axes[1, 1].transAxes,
            ha="center",
            va="center",
        )
        axes[1, 1].set_title("残差分析")

    plt.tight_layout()
    plt.show()

    # 5. 输出统计摘要
    logger.info("=== 统计摘要 ===")
    logger.info(f"零食支出统计: 均值={np.mean(sy):.2f}, 标准差={np.std(sy):.2f}")
    logger.info(f"体重增长率统计: 均值={np.mean(dydx):.2f}, 标准差={np.std(dydx):.2f}")
    logger.info(f"数据点数量: {len(sy)}")

    # 相关性强度判断
    abs_corr = abs(correlation_coeff)
    if abs_corr >= 0.7:
        strength = "强"
    elif abs_corr >= 0.4:
        strength = "中等"
    elif abs_corr >= 0.2:
        strength = "弱"
    else:
        strength = "很弱或无"

    direction = "正" if correlation_coeff > 0 else "负"
    logger.info(f"相关性强度: {strength}{direction}相关")

    return "Done"
