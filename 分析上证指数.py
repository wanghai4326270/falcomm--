# -*- coding:utf-8 -*-
# 上证指数全面分析报告
from Ashare import *
from MyTT import *
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas as pd

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

print("="*80)
print("上证指数全面分析报告")
print("="*80)
print()

# ========== 1. 获取数据 ==========
print("【1/6】正在获取上证指数历史数据...")
df_daily = get_price('sh000001', frequency='1d', count=250)  # 近一年日线
df_weekly = get_price('sh000001', frequency='1w', count=100)  # 近两年周线
print("✓ 数据获取完成")
print()

# ========== 2. 准备数据 ==========
print("【2/6】正在计算技术指标...")
CLOSE = df_daily.close.values
OPEN = df_daily.open.values
HIGH = df_daily.high.values
LOW = df_daily.low.values
VOLUME = df_daily.volume.values
dates = df_daily.index

# 均线
MA5 = MA(CLOSE, 5)
MA10 = MA(CLOSE, 10)
MA20 = MA(CLOSE, 20)
MA60 = MA(CLOSE, 60)

# 布林带
up, mid, lower = BOLL(CLOSE)

# MACD
DIF, DEA, MACD_bar = MACD(CLOSE)

# KDJ
K, D, J = KDJ(CLOSE, HIGH, LOW)

# RSI
RSI6 = RSI(CLOSE, 6)
RSI12 = RSI(CLOSE, 12)
RSI24 = RSI(CLOSE, 24)

# 威廉指标
WR10, WR6 = WR(CLOSE, HIGH, LOW)

# CCI
CCI = CCI(CLOSE, HIGH, LOW)

# 成交量均线
VOL_MA5 = MA(VOLUME, 5)
VOL_MA20 = MA(VOLUME, 20)

print("✓ 技术指标计算完成")
print()

# ========== 3. 基础数据分析 ==========
print("【3/6】基础数据分析")
print("-"*80)
current_price = CLOSE[-1]
highest_250 = np.max(CLOSE)
lowest_250 = np.min(CLOSE)
current_pos = (current_price - lowest_250) / (highest_250 - lowest_250) * 100

print(f"最新收盘: {current_price:.2f}")
print(f"近一年最高: {highest_250:.2f}")
print(f"近一年最低: {lowest_250:.2f}")
print(f"当前位置分位: {current_pos:.1f}%")
print()

# 近期涨跌幅
change_1d = (CLOSE[-1] - CLOSE[-2]) / CLOSE[-2] * 100
change_5d = (CLOSE[-1] - CLOSE[-6]) / CLOSE[-6] * 100 if len(CLOSE) > 6 else 0
change_20d = (CLOSE[-1] - CLOSE[-21]) / CLOSE[-21] * 100 if len(CLOSE) > 21 else 0
change_60d = (CLOSE[-1] - CLOSE[-61]) / CLOSE[-61] * 100 if len(CLOSE) > 61 else 0

print("近期涨跌幅:")
print(f"  1日: {change_1d:+.2f}%")
print(f"  5日: {change_5d:+.2f}%")
print(f"  20日: {change_20d:+.2f}%")
print(f"  60日: {change_60d:+.2f}%")
print()

# 成交量分析
avg_vol_5 = np.mean(VOLUME[-5:])
avg_vol_20 = np.mean(VOLUME[-20:])
vol_ratio = avg_vol_5 / avg_vol_20 if avg_vol_20 > 0 else 1

print("成交量分析:")
print(f"  5日均量: {avg_vol_5/1e8:.2f}亿")
print(f"  20日均量: {avg_vol_20/1e8:.2f}亿")
print(f"  量比: {vol_ratio:.2f}")
print()

# ========== 4. 技术指标信号 ==========
print("【4/6】技术指标信号")
print("-"*80)

# 均线信号
ma5_above_ma20 = MA5[-1] > MA20[-1]
ma20_above_ma60 = MA20[-1] > MA60[-1]
golden_cross = CROSS(MA5, MA20)
death_cross = CROSS(MA20, MA5)

print("均线系统:")
print(f"  MA5: {MA5[-1]:.2f} {'(向上)' if MA5[-1] > MA5[-2] else '(向下)'}")
print(f"  MA20: {MA20[-1]:.2f} {'(向上)' if MA20[-1] > MA20[-2] else '(向下)'}")
print(f"  MA60: {MA60[-1]:.2f} {'(向上)' if MA60[-1] > MA60[-2] else '(向下)'}")
print(f"  排列: {'多头' if ma5_above_ma20 and ma20_above_ma60 else '空头' if not ma5_above_ma20 and not ma20_above_ma60 else '震荡'}")
print()

# MACD信号
macd_gold = DIF[-1] > DEA[-1]
macd_bar_pos = MACD_bar[-1] > 0
macd_divergence = (CLOSE[-1] < CLOSE[-5] and DIF[-1] > DIF[-5]) if len(CLOSE) > 5 else False

print("MACD指标:")
print(f"  DIF: {DIF[-1]:.4f}")
print(f"  DEA: {DEA[-1]:.4f}")
print(f"  MACD: {MACD_bar[-1]:.4f}")
print(f"  状态: {'金叉' if macd_gold else '死叉'}")
print(f"  柱体: {'正' if macd_bar_pos else '负'}")
print()

# KDJ信号
kdj_k = K[-1]
kdj_d = D[-1]
kdj_j = J[-1]
kdj_overbought = kdj_k > 80
kdj_oversold = kdj_k < 20
kdj_gold = kdj_k > kdj_d

print("KDJ指标:")
print(f"  K: {kdj_k:.2f}")
print(f"  D: {kdj_d:.2f}")
print(f"  J: {kdj_j:.2f}")
print(f"  超买超卖: {'超买' if kdj_overbought else '超卖' if kdj_oversold else '中性'}")
print(f"  交叉: {'金叉' if kdj_gold else '死叉'}")
print()

# RSI信号
rsi_current = RSI24[-1]
rsi_overbought = rsi_current > 70
rsi_oversold = rsi_current < 30

print("RSI指标(24日):")
print(f"  RSI: {rsi_current:.2f}")
print(f"  状态: {'超买' if rsi_overbought else '超卖' if rsi_oversold else '中性'}")
print()

# 布林带信号
boll_position = (CLOSE[-1] - lower[-1]) / (up[-1] - lower[-1]) * 100
boll_upper_touch = CLOSE[-1] >= up[-1]
boll_lower_touch = CLOSE[-1] <= lower[-1]

print("布林带指标:")
print(f"  上轨: {up[-1]:.2f}")
print(f"  中轨: {mid[-1]:.2f}")
print(f"  下轨: {lower[-1]:.2f}")
print(f"  当前位置: {boll_position:.1f}%")
print(f"  触及: {'上轨' if boll_upper_touch else '下轨' if boll_lower_touch else '未触及'}")
print()

# ========== 5. 综合评分 ==========
print("【5/6】综合趋势评分")
print("-"*80)

score = 50

# 均线评分
if ma5_above_ma20 and ma20_above_ma60:
    score += 15
elif not ma5_above_ma20 and not ma20_above_ma60:
    score -= 15

# MACD评分
if macd_gold and macd_bar_pos:
    score += 10
elif not macd_gold and not macd_bar_pos:
    score -= 10

# KDJ评分
if not kdj_overbought and kdj_gold:
    score += 8
elif kdj_overbought and not kdj_gold:
    score -= 8

# RSI评分
if 30 <= rsi_current <= 70:
    score += 5
elif rsi_current < 30:
    score += 10
elif rsi_current > 70:
    score -= 10

# 成交量评分
if vol_ratio > 1.2:
    score += 5
elif vol_ratio < 0.8:
    score -= 5

# 布林带位置
if 20 <= boll_position <= 80:
    score += 5
elif boll_position < 20:
    score += 8
elif boll_position > 80:
    score -= 8

score = max(0, min(100, score))

print(f"综合趋势评分: {score}/100")
if score >= 70:
    print("趋势判断: 强势看涨")
elif score >= 55:
    print("趋势判断: 偏多震荡")
elif score >= 45:
    print("趋势判断: 中性震荡")
elif score >= 30:
    print("趋势判断: 偏空震荡")
else:
    print("趋势判断: 弱势看跌")
print()

# ========== 6. 风险提示与建议 ==========
print("【6/6】风险提示与投资建议")
print("-"*80)

risks = []
suggestions = []

if score < 40:
    risks.append("整体趋势偏弱，注意控制仓位")
    suggestions.append("建议观望为主，等待明确信号")
elif score > 60:
    suggestions.append("可适当提高仓位，关注强势板块")

if rsi_current > 70 or kdj_overbought:
    risks.append("短期技术指标超买，可能面临回调")
    suggestions.append("追高需谨慎，可考虑分批止盈")

if rsi_current < 30 or kdj_oversold:
    suggestions.append("短期超卖，可关注反弹机会")

if vol_ratio < 0.8:
    risks.append("成交量萎缩，市场活跃度不足")
    suggestions.append("关注量能变化，放量确认趋势")

if boll_position > 80:
    risks.append("价格触及布林带上轨，压力较大")
elif boll_position < 20:
    suggestions.append("价格接近布林带下轨，支撑区域")

if len(risks) > 0:
    print("⚠️ 风险提示:")
    for i, risk in enumerate(risks, 1):
        print(f"  {i}. {risk}")
    print()

if len(suggestions) > 0:
    print("💡 投资建议:")
    for i, sug in enumerate(suggestions, 1):
        print(f"  {i}. {sug}")
    print()

# ========== 7. 绘制图表 ==========
print("正在生成分析图表...")

fig = plt.figure(figsize=(16, 20))
gs = fig.add_gridspec(4, 1, hspace=0.3)

# 主图：价格和均线
ax1 = fig.add_subplot(gs[0])
ax1.plot(dates, CLOSE, label='收盘价', linewidth=2, color='#333333')
ax1.plot(dates, MA5, label='MA5', color='#FF6B6B', alpha=0.8)
ax1.plot(dates, MA20, label='MA20', color='#4ECDC4', alpha=0.8)
ax1.plot(dates, MA60, label='MA60', color='#45B7D1', alpha=0.8)
ax1.fill_between(dates, up, lower, alpha=0.15, color='#96CEB4', label='布林带')
ax1.plot(dates, up, color='#96CEB4', linewidth=0.5, alpha=0.5)
ax1.plot(dates, lower, color='#96CEB4', linewidth=0.5, alpha=0.5)
ax1.set_title('上证指数 价格走势 & 均线系统', fontsize=16, fontweight='bold')
ax1.legend(loc='upper left', ncol=5)
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_locator(MultipleLocator(len(dates)//12))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# 成交量
ax2 = fig.add_subplot(gs[1], sharex=ax1)
ax2.bar(dates, VOLUME, label='成交量', color='#95A5A6', alpha=0.7)
ax2.plot(dates, VOL_MA5, label='VOL_MA5', color='#E67E22', linewidth=1.5)
ax2.plot(dates, VOL_MA20, label='VOL_MA20', color='#3498DB', linewidth=1.5)
ax2.set_title('成交量分析', fontsize=14, fontweight='bold')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)

# MACD
ax3 = fig.add_subplot(gs[2], sharex=ax1)
colors = ['#E74C3C' if x >= 0 else '#3498DB' for x in MACD_bar]
ax3.bar(dates, MACD_bar, label='MACD', color=colors, alpha=0.7)
ax3.plot(dates, DIF, label='DIF', color='#E67E22', linewidth=1.5)
ax3.plot(dates, DEA, label='DEA', color='#9B59B6', linewidth=1.5)
ax3.axhline(y=0, color='#333333', linestyle='--', linewidth=0.8)
ax3.set_title('MACD 指标', fontsize=14, fontweight='bold')
ax3.legend(loc='upper left')
ax3.grid(True, alpha=0.3)

# KDJ + RSI
ax4 = fig.add_subplot(gs[3], sharex=ax1)
ax4.plot(dates, K, label='K', color='#E74C3C', linewidth=1.2)
ax4.plot(dates, D, label='D', color='#3498DB', linewidth=1.2)
ax4.plot(dates, J, label='J', color='#9B59B6', linewidth=1, alpha=0.7)
ax4.axhline(y=80, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax4.axhline(y=20, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax4.set_ylim([-10, 110])
ax4.set_title('KDJ 指标', fontsize=14, fontweight='bold')
ax4.legend(loc='upper left')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('上证指数分析报告.png', dpi=150, bbox_inches='tight')
print("✓ 图表已保存为: 上证指数分析报告.png")
print()

print("="*80)
print("分析完成！")
print("="*80)
print()
print("提示: 以上分析仅供参考，不构成投资建议。")
print("股市有风险，投资需谨慎。")
