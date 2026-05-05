# -*- coding:utf-8 -*-
# 沪深300和中证500指数对比分析
from Ashare import *
from MyTT import *
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas as pd

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

print("="*100)
print("沪深300 vs 中证500 指数对比分析报告")
print("="*100)
print()

# ========== 1. 获取数据 ==========
print("【1/5】正在获取指数历史数据...")
df_hs300 = get_price('sh000300', frequency='1d', count=250)  # 沪深300
df_zz500 = get_price('sh000905', frequency='1d', count=250)  # 中证500
print("✓ 数据获取完成")
print()

# ========== 2. 准备数据 ==========
print("【2/5】正在计算技术指标...")

# 沪深300数据
HS300_CLOSE = df_hs300.close.values
HS300_OPEN = df_hs300.open.values
HS300_HIGH = df_hs300.high.values
HS300_LOW = df_hs300.low.values
HS300_VOLUME = df_hs300.volume.values
HS300_DATES = df_hs300.index

# 中证500数据
ZZ500_CLOSE = df_zz500.close.values
ZZ500_OPEN = df_zz500.open.values
ZZ500_HIGH = df_zz500.high.values
ZZ500_LOW = df_zz500.low.values
ZZ500_VOLUME = df_zz500.volume.values
ZZ500_DATES = df_zz500.index

# 沪深300技术指标
HS300_MA5 = MA(HS300_CLOSE, 5)
HS300_MA20 = MA(HS300_CLOSE, 20)
HS300_MA60 = MA(HS300_CLOSE, 60)
HS300_UP, HS300_MID, HS300_LOWER = BOLL(HS300_CLOSE)
HS300_DIF, HS300_DEA, HS300_MACD = MACD(HS300_CLOSE)
HS300_K, HS300_D, HS300_J = KDJ(HS300_CLOSE, HS300_HIGH, HS300_LOW)
HS300_RSI12 = RSI(HS300_CLOSE, 12)
HS300_RSI24 = RSI(HS300_CLOSE, 24)

# 中证500技术指标
ZZ500_MA5 = MA(ZZ500_CLOSE, 5)
ZZ500_MA20 = MA(ZZ500_CLOSE, 20)
ZZ500_MA60 = MA(ZZ500_CLOSE, 60)
ZZ500_UP, ZZ500_MID, ZZ500_LOWER = BOLL(ZZ500_CLOSE)
ZZ500_DIF, ZZ500_DEA, ZZ500_MACD = MACD(ZZ500_CLOSE)
ZZ500_K, ZZ500_D, ZZ500_J = KDJ(ZZ500_CLOSE, ZZ500_HIGH, ZZ500_LOW)
ZZ500_RSI12 = RSI(ZZ500_CLOSE, 12)
ZZ500_RSI24 = RSI(ZZ500_CLOSE, 24)

print("✓ 技术指标计算完成")
print()

# ========== 3. 基础数据对比 ==========
print("【3/5】基础数据对比")
print("-"*100)
print(f"{'指标':<20} {'沪深300':>15} {'中证500':>15} {'差值':>15}")
print("-"*100)

hs300_current = HS300_CLOSE[-1]
zz500_current = ZZ500_CLOSE[-1]

print(f"{'最新收盘':<20} {hs300_current:>15.2f} {zz500_current:>15.2f} {hs300_current-zz500_current:>15.2f}")

hs300_1d_change = (HS300_CLOSE[-1] - HS300_CLOSE[-2]) / HS300_CLOSE[-2] * 100
zz500_1d_change = (ZZ500_CLOSE[-1] - ZZ500_CLOSE[-2]) / ZZ500_CLOSE[-2] * 100
print(f"{'1日涨跌幅':<20} {hs300_1d_change:>14.2f}% {zz500_1d_change:>14.2f}% {hs300_1d_change-zz500_1d_change:>14.2f}%")

hs300_20d_change = (HS300_CLOSE[-1] - HS300_CLOSE[-21]) / HS300_CLOSE[-21] * 100
zz500_20d_change = (ZZ500_CLOSE[-1] - ZZ500_CLOSE[-21]) / ZZ500_CLOSE[-21] * 100
print(f"{'20日涨跌幅':<20} {hs300_20d_change:>14.2f}% {zz500_20d_change:>14.2f}% {hs300_20d_change-zz500_20d_change:>14.2f}%")

hs300_60d_change = (HS300_CLOSE[-1] - HS300_CLOSE[-61]) / HS300_CLOSE[-61] * 100
zz500_60d_change = (ZZ500_CLOSE[-1] - ZZ500_CLOSE[-61]) / ZZ500_CLOSE[-61] * 100
print(f"{'60日涨跌幅':<20} {hs300_60d_change:>14.2f}% {zz500_60d_change:>14.2f}% {hs300_60d_change-zz500_60d_change:>14.2f}%")

hs300_vol = np.mean(HS300_VOLUME[-5:])
zz500_vol = np.mean(ZZ500_VOLUME[-5:])
print(f"{'5日均量(亿)':<20} {hs300_vol/1e8:>14.2f} {zz500_vol/1e8:>14.2f} {(hs300_vol-zz500_vol)/1e8:>14.2f}")

hs300_ma20_pos = (hs300_current - HS300_LOWER[-1]) / (HS300_UP[-1] - HS300_LOWER[-1]) * 100
zz500_ma20_pos = (zz500_current - ZZ500_LOWER[-1]) / (ZZ500_UP[-1] - ZZ500_LOWER[-1]) * 100
print(f"{'布林带位置':<20} {hs300_ma20_pos:>14.1f}% {zz500_ma20_pos:>14.1f}% {hs300_ma20_pos-zz500_ma20_pos:>14.1f}%")

print()

# ========== 4. 技术指标对比 ==========
print("【4/5】技术指标对比")
print("-"*100)
print(f"{'指标':<20} {'沪深300':>15} {'中证500':>15} {'结论':>20}")
print("-"*100)

# 均线排列
hs300_ma_arrange = "多头" if HS300_MA5[-1] > HS300_MA20[-1] > HS300_MA60[-1] else "空头" if HS300_MA5[-1] < HS300_MA20[-1] < HS300_MA60[-1] else "震荡"
zz500_ma_arrange = "多头" if ZZ500_MA5[-1] > ZZ500_MA20[-1] > ZZ500_MA60[-1] else "空头" if ZZ500_MA5[-1] < ZZ500_MA20[-1] < ZZ500_MA60[-1] else "震荡"
print(f"{'均线排列':<20} {hs300_ma_arrange:>15} {zz500_ma_arrange:>15} {'偏强' if hs300_ma_arrange=='多头' and zz500_ma_arrange=='空头' else '偏强' if zz500_ma_arrange=='多头' and hs300_ma_arrange=='空头' else '相当'}")

# MACD
hs300_macd_gold = HS300_DIF[-1] > HS300_DEA[-1]
zz500_macd_gold = ZZ500_DIF[-1] > ZZ500_DEA[-1]
hs300_macd_bar = HS300_MACD[-1]
zz500_macd_bar = ZZ500_MACD[-1]
print(f"{'MACD柱体':<20} {hs300_macd_bar:>14.4f} {zz500_macd_bar:>14.4f} {'偏强' if abs(hs300_macd_bar) > abs(zz500_macd_bar) else '偏弱'}")

# KDJ
hs300_kdj_j = HS300_J[-1]
zz500_kdj_j = ZZ500_J[-1]
print(f"{'KDJ J值':<20} {hs300_kdj_j:>14.2f} {zz500_kdj_j:>14.2f} {'偏强' if hs300_kdj_j > zz500_kdj_j else '偏弱'}")

# RSI
hs300_rsi24 = HS300_RSI24[-1]
zz500_rsi24 = ZZ500_RSI24[-1]
print(f"{'RSI(24)':<20} {hs300_rsi24:>14.2f} {zz500_rsi24:>14.2f} {'偏强' if hs300_rsi24 > zz500_rsi24 else '偏弱'}")

print()

# ========== 5. 综合评分 ==========
print("【5/5】综合评分与投资建议")
print("-"*100)

def calc_score(CLOSE, MA5, MA20, MA60, DIF, DEA, MACD_bar, K, D, J, RSI24, UP, MID, LOWER):
    score = 50
    
    # 均线评分
    ma5_above_ma20 = MA5[-1] > MA20[-1]
    ma20_above_ma60 = MA20[-1] > MA60[-1]
    if ma5_above_ma20 and ma20_above_ma60:
        score += 15
    elif not ma5_above_ma20 and not ma20_above_ma60:
        score -= 15
    
    # MACD评分
    macd_gold = DIF[-1] > DEA[-1]
    macd_bar_pos = MACD_bar[-1] > 0
    if macd_gold and macd_bar_pos:
        score += 10
    elif not macd_gold and not macd_bar_pos:
        score -= 10
    
    # KDJ评分
    kdj_k = K[-1]
    kdj_gold = kdj_k > D[-1]
    kdj_overbought = kdj_k > 80
    kdj_oversold = kdj_k < 20
    if not kdj_overbought and kdj_gold:
        score += 8
    elif kdj_overbought and not kdj_gold:
        score -= 8
    
    # RSI评分
    if 30 <= RSI24[-1] <= 70:
        score += 5
    elif RSI24[-1] < 30:
        score += 10
    elif RSI24[-1] > 70:
        score -= 10
    
    # 布林带位置
    boll_pos = (CLOSE[-1] - LOWER[-1]) / (UP[-1] - LOWER[-1]) * 100
    if 20 <= boll_pos <= 80:
        score += 5
    elif boll_pos < 20:
        score += 8
    elif boll_pos > 80:
        score -= 8
    
    return max(0, min(100, score))

hs300_score = calc_score(HS300_CLOSE, HS300_MA5, HS300_MA20, HS300_MA60, HS300_DIF, HS300_DEA, HS300_MACD, HS300_K, HS300_D, HS300_J, HS300_RSI24, HS300_UP, HS300_MID, HS300_LOWER)
zz500_score = calc_score(ZZ500_CLOSE, ZZ500_MA5, ZZ500_MA20, ZZ500_MA60, ZZ500_DIF, ZZ500_DEA, ZZ500_MACD, ZZ500_K, ZZ500_D, ZZ500_J, ZZ500_RSI24, ZZ500_UP, ZZ500_MID, ZZ500_LOWER)

def get_trend(score):
    if score >= 70:
        return "强势看涨", "积极"
    elif score >= 55:
        return "偏多震荡", "适度"
    elif score >= 45:
        return "中性震荡", "谨慎"
    elif score >= 30:
        return "偏空震荡", "防御"
    else:
        return "弱势看跌", "观望"

hs300_trend, hs300_strategy = get_trend(hs300_score)
zz500_trend, zz500_strategy = get_trend(zz500_score)

print(f"{'指数':<10} {'综合评分':>10} {'趋势判断':>15} {'操作策略':>15}")
print("-"*100)
print(f"{'沪深300':<10} {hs300_score:>10} {hs300_trend:>15} {hs300_strategy:>15}")
print(f"{'中证500':<10} {zz500_score:>10} {zz500_trend:>15} {zz500_strategy:>15}")
print()

# ========== 6. 投资建议 ==========
print("投资建议")
print("-"*100)

if hs300_score > zz500_score:
    print(f"✓ 相对强度: 沪深300 ({hs300_score}分) > 中证500 ({zz500_score}分)")
    print("  沪深300表现更强，权重股占优")
else:
    print(f"✓ 相对强度: 中证500 ({zz500_score}分) > 沪深300 ({hs300_score}分)")
    print("  中证500表现更强，中小盘占优")

print()

# 风险评估
risks = []
suggestions = []

# 沪深300风险
if hs300_score < 40:
    risks.append("沪深300整体趋势偏弱")
elif hs300_score > 60:
    suggestions.append("沪深300可适当提高仓位")

# 中证500风险
if zz500_score < 40:
    risks.append("中证500整体趋势偏弱")
elif zz500_score > 60:
    suggestions.append("中证500可适当提高仓位")

# 成交量
hs300_vol_ratio = np.mean(HS300_VOLUME[-5:]) / np.mean(HS300_VOLUME[-20:]) if np.mean(HS300_VOLUME[-20:]) > 0 else 1
zz500_vol_ratio = np.mean(ZZ500_VOLUME[-5:]) / np.mean(ZZ500_VOLUME[-20:]) if np.mean(ZZ500_VOLUME[-20:]) > 0 else 1

if hs300_vol_ratio < 0.8:
    risks.append("沪深300成交量萎缩")
if zz500_vol_ratio < 0.8:
    risks.append("中证500成交量萎缩")

# 布林带
hs300_boll_pos = (hs300_current - HS300_LOWER[-1]) / (HS300_UP[-1] - HS300_LOWER[-1]) * 100
zz500_boll_pos = (zz500_current - ZZ500_LOWER[-1]) / (ZZ500_UP[-1] - ZZ500_LOWER[-1]) * 100

if hs300_boll_pos > 80:
    risks.append("沪深300价格接近布林带上轨")
elif hs300_boll_pos < 20:
    suggestions.append("沪深300接近布林带下轨支撑")

if zz500_boll_pos > 80:
    risks.append("中证500价格接近布林带上轨")
elif zz500_boll_pos < 20:
    suggestions.append("中证500接近布林带下轨支撑")

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

# 组合建议
print("组合配置建议:")
if hs300_score > 55 and zz500_score > 55:
    print("  双方均偏强，可考虑均衡配置 6:4 或 5:5")
elif hs300_score > 55 and zz500_score < 45:
    print("  沪深300偏强，中证500偏弱，建议 7:3 配置")
elif hs300_score < 45 and zz500_score > 55:
    print("  中证500偏强，沪深300偏弱，建议 3:7 配置")
elif hs300_score < 45 and zz500_score < 45:
    print("  双方均偏弱，建议降低仓位，观望等待明确信号")
else:
    print("  双方处于震荡，建议 5:5 均衡配置，灵活调整")

print()

# ========== 7. 绘制图表 ==========
print("正在生成分析图表...")

fig = plt.figure(figsize=(20, 24))
gs = fig.add_gridspec(5, 2, hspace=0.3, wspace=0.2)

# 沪深300价格与均线
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(HS300_DATES, HS300_CLOSE, label='沪深300', linewidth=2, color='#E74C3C')
ax1.plot(HS300_DATES, HS300_MA5, label='MA5', color='#F39C12', alpha=0.8)
ax1.plot(HS300_DATES, HS300_MA20, label='MA20', color='#3498DB', alpha=0.8)
ax1.plot(HS300_DATES, HS300_MA60, label='MA60', color='#9B59B6', alpha=0.8)
ax1.fill_between(HS300_DATES, HS300_UP, HS300_LOWER, alpha=0.15, color='#2ECC71')
ax1.set_title(f'沪深300 指数走势 (评分: {hs300_score})', fontsize=14, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_locator(MultipleLocator(len(HS300_DATES)//12))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# 中证500价格与均线
ax2 = fig.add_subplot(gs[0, 1], sharex=ax1)
ax2.plot(ZZ500_DATES, ZZ500_CLOSE, label='中证500', linewidth=2, color='#3498DB')
ax2.plot(ZZ500_DATES, ZZ500_MA5, label='MA5', color='#F39C12', alpha=0.8)
ax2.plot(ZZ500_DATES, ZZ500_MA20, label='MA20', color='#E74C3C', alpha=0.8)
ax2.plot(ZZ500_DATES, ZZ500_MA60, label='MA60', color='#9B59B6', alpha=0.8)
ax2.fill_between(ZZ500_DATES, ZZ500_UP, ZZ500_LOWER, alpha=0.15, color='#2ECC71')
ax2.set_title(f'中证500 指数走势 (评分: {zz500_score})', fontsize=14, fontweight='bold')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_locator(MultipleLocator(len(ZZ500_DATES)//12))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

# 沪深300成交量
ax3 = fig.add_subplot(gs[1, 0], sharex=ax1)
ax3.bar(HS300_DATES, HS300_VOLUME, label='成交量', color='#95A5A6', alpha=0.7)
ax3.plot(HS300_DATES, MA(HS300_VOLUME, 5), label='VOL_MA5', color='#E74C3C', linewidth=1.5)
ax3.set_title('沪深300 成交量', fontsize=12)
ax3.legend(loc='upper left')
ax3.grid(True, alpha=0.3)

# 中证500成交量
ax4 = fig.add_subplot(gs[1, 1], sharex=ax1)
ax4.bar(ZZ500_DATES, ZZ500_VOLUME, label='成交量', color='#95A5A6', alpha=0.7)
ax4.plot(ZZ500_DATES, MA(ZZ500_VOLUME, 5), label='VOL_MA5', color='#3498DB', linewidth=1.5)
ax4.set_title('中证500 成交量', fontsize=12)
ax4.legend(loc='upper left')
ax4.grid(True, alpha=0.3)

# 沪深300 MACD
ax5 = fig.add_subplot(gs[2, 0], sharex=ax1)
colors1 = ['#E74C3C' if x >= 0 else '#3498DB' for x in HS300_MACD]
ax5.bar(HS300_DATES, HS300_MACD, label='MACD', color=colors1, alpha=0.7)
ax5.plot(HS300_DATES, HS300_DIF, label='DIF', color='#F39C12', linewidth=1.5)
ax5.plot(HS300_DATES, HS300_DEA, label='DEA', color='#9B59B6', linewidth=1.5)
ax5.axhline(y=0, color='#333333', linestyle='--', linewidth=0.8)
ax5.set_title('沪深300 MACD', fontsize=12)
ax5.legend(loc='upper left')
ax5.grid(True, alpha=0.3)

# 中证500 MACD
ax6 = fig.add_subplot(gs[2, 1], sharex=ax1)
colors2 = ['#3498DB' if x >= 0 else '#E74C3C' for x in ZZ500_MACD]
ax6.bar(ZZ500_DATES, ZZ500_MACD, label='MACD', color=colors2, alpha=0.7)
ax6.plot(ZZ500_DATES, ZZ500_DIF, label='DIF', color='#F39C12', linewidth=1.5)
ax6.plot(ZZ500_DATES, ZZ500_DEA, label='DEA', color='#9B59B6', linewidth=1.5)
ax6.axhline(y=0, color='#333333', linestyle='--', linewidth=0.8)
ax6.set_title('中证500 MACD', fontsize=12)
ax6.legend(loc='upper left')
ax6.grid(True, alpha=0.3)

# KDJ对比
ax7 = fig.add_subplot(gs[3, 0], sharex=ax1)
ax7.plot(HS300_DATES, HS300_K, label='沪深300-K', color='#E74C3C', linewidth=1.2)
ax7.plot(HS300_DATES, HS300_D, label='沪深300-D', color='#F39C12', linewidth=1.2)
ax7.plot(HS300_DATES, HS300_J, label='沪深300-J', color='#9B59B6', linewidth=1)
ax7.axhline(y=80, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax7.axhline(y=20, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax7.set_ylim([-10, 110])
ax7.set_title('KDJ 指标 (沪深300)', fontsize=12)
ax7.legend(loc='upper left')
ax7.grid(True, alpha=0.3)

ax8 = fig.add_subplot(gs[3, 1], sharex=ax1)
ax8.plot(ZZ500_DATES, ZZ500_K, label='中证500-K', color='#3498DB', linewidth=1.2)
ax8.plot(ZZ500_DATES, ZZ500_D, label='中证500-D', color='#1ABC9C', linewidth=1.2)
ax8.plot(ZZ500_DATES, ZZ500_J, label='中证500-J', color='#9B59B6', linewidth=1)
ax8.axhline(y=80, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax8.axhline(y=20, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax8.set_ylim([-10, 110])
ax8.set_title('KDJ 指标 (中证500)', fontsize=12)
ax8.legend(loc='upper left')
ax8.grid(True, alpha=0.3)

# RSI对比
ax9 = fig.add_subplot(gs[4, 0], sharex=ax1)
ax9.plot(HS300_DATES, HS300_RSI12, label='沪深300-RSI12', color='#E74C3C', linewidth=1.2)
ax9.plot(HS300_DATES, HS300_RSI24, label='沪深300-RSI24', color='#F39C12', linewidth=1.2)
ax9.axhline(y=70, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax9.axhline(y=30, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax9.set_ylim([-5, 105])
ax9.set_title('RSI 指标 (沪深300)', fontsize=12)
ax9.legend(loc='upper left')
ax9.grid(True, alpha=0.3)

ax10 = fig.add_subplot(gs[4, 1], sharex=ax1)
ax10.plot(ZZ500_DATES, ZZ500_RSI12, label='中证500-RSI12', color='#3498DB', linewidth=1.2)
ax10.plot(ZZ500_DATES, ZZ500_RSI24, label='中证500-RSI24', color='#1ABC9C', linewidth=1.2)
ax10.axhline(y=70, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax10.axhline(y=30, color='#333333', linestyle='--', linewidth=0.5, alpha=0.5)
ax10.set_ylim([-5, 105])
ax10.set_title('RSI 指标 (中证500)', fontsize=12)
ax10.legend(loc='upper left')
ax10.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('沪深300中证500对比分析.png', dpi=150, bbox_inches='tight')
print("✓ 图表已保存为: 沪深300中证500对比分析.png")
print()

print("="*100)
print("分析完成！")
print("="*100)
print()
print("提示: 以上分析仅供参考，不构成投资建议。")
print("股市有风险，投资需谨慎。")
