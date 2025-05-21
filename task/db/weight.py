# -*- coding: utf-8 -*-
# @file read_weight.py
# @brief Read weight from the database
# @author sailing-innocent
# @date 2025-04-23
# @version 1.0
# ---------------------------------

from internal.model.health import (
    read_weights_impl,
    read_weight_record_impl,
    update_weight_record_impl,
    create_weight_record_impl,
)
from internal.data.health import WeightData, WeightRecordData
import logging

logger = logging.getLogger(__name__)
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
import datetime
from utils.sampler import TimeValueSampler


def read_weight(db_func):
    logger.info("Reading weight from the database")
    db = next(db_func())
    weights = read_weights_impl(db)  # [(id, value, htime)]
    # weights = weights[300:]  # skip first 300 records
    logger.info(f"Read {len(weights)} weights from the database")

    x = np.array([w.htime for w in weights])
    y = np.array([float(w.value) for w in weights])

    xmin = np.min(x)
    xmax = np.max(x)
    start_time = datetime.datetime.fromtimestamp(xmin).strftime("%Y-%m-%d %H:%M:%S")

    logger.info(f"Start time: {start_time}")
    curr_time = datetime.datetime.fromtimestamp(xmax).strftime("%Y-%m-%d %H:%M:%S")
    # days from start_time to curr_time in 'yyyy-mm-dd' format
    days = (
        datetime.datetime.fromtimestamp(xmax) - datetime.datetime.fromtimestamp(xmin)
    ).days
    logger.info(f"Days: {days}")
    # all_date_per_days = ['2020-11-01', '2020-11-02']
    all_date_per_days = [(xmin + 86400 * i, i) for i in range(days + 1)]
    # logger.info(f"All date per days: {all_date_per_days}")
    all_date_per_weeks = [(xmin + 604800 * i, i) for i in range(days // 7 + 1)]
    logger.info(all_date_per_weeks)

    y_filtered = savgol_filter(y, 5, 2)
    # plt.scatter(x, y)
    # plt.plot(x, ysp, color="red")
    # plt.title("Weight")
    # plt.xlabel("Time")
    # plt.ylabel("Weight")
    # plt.xlim(0, xmax - xmin)
    # plt.ylim(ymin, np.max(y) + 5)
    # plt.show()
    time_reqs = [xsp for xsp, _ in all_date_per_days]
    logging.info(f"Time reqs: {time_reqs}")
    logging.info(f"Time reqs len: {len(time_reqs)}")
    time_values = [(x[i], y_filtered[i]) for i in range(len(x))]
    logging.info(f"Time values: {time_values}")
    get_tv_func = lambda: time_values
    sampler = TimeValueSampler(
        time_reqs=time_reqs,
        influence=3 * 86400,  # 3 days
        get_time_value_func=get_tv_func,
    )
    res = sampler.sample()
    logging.info(f"Sampled values: {res}")
    logging.info(f"Number of sampled values: {len(res)}")

    # plt.scatter(time_reqs, res)
    # plt.title("Weight")
    # plt.xlabel("Time")
    # plt.ylabel("Weight")
    # plt.xticks(rotation=45)
    # plt.grid()
    # plt.show()

    # post-process

    wrs = [
        WeightRecordData(
            value=str(round(res[i], 2)),
            htime=time_reqs[i],
            tag="daily,"
            + datetime.datetime.fromtimestamp(time_reqs[i]).strftime("%Y-%m-%d"),
        )
        for i in range(len(res))
    ]
    logger.info(f"Weight records: {wrs}")
    for wr in wrs:
        # search for the same tag
        weight_record = read_weight_record_impl(db, _tag=wr.tag)
        if weight_record is not None:
            logger.info(f"Weight record {weight_record.id} already exists, updating...")
            update_weight_record_impl(
                db,
                weight_record.id,
                WeightRecordData(
                    value=wr.value,
                    htime=wr.htime,
                    tag=wr.tag,
                ),
            )
        else:
            # create weight record
            logger.info(f"Creating weight record: {wr}")
            create_weight_record_impl(db, wr)

    return "Done"
