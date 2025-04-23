# -*- coding: utf-8 -*-
# @file money.py
# @brief My Personal Money Calculation Task
# @author sailing-innocent
# @date 2025-04-23
# @version 1.0
# ---------------------------------

import numpy as np 

# 计算等额本息方法计价下，初始Q经过利率R和n期数的计算后，得到每月还款金额
def per_mon(Q, R, n):
    return R * (1+R)**n / ((1+R)**n - 1) * Q

