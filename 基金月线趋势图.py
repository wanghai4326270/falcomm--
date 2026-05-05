# -*- coding: utf-8 -*-
# 基金月线趋势图绘制
from Ashare import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import pandas as pd
import matplotlib

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 获取上证指数月线数据（作为基金趋势参考）
df = get_price('sh000001', frequency='1M', count=24)  # 获取最近24个月数据

print('上证指数月线数据：')
print(df)

# 创建图表
fig, ax = plt.subplots(figsize=(16, 9))

# 绘制收盘价趋势线
ax.plot(df.index, df.close, color='#E74C3C', linewidth=2.5, marker='o', markersize=6, label='Close Price')

# 填充涨跌颜色
for i in range(len(df)-1):
    if df.close.iloc[i+1] >= df.close.iloc[i]:
        color = '#27AE60'  # 涨 - 绿色
    else:
        color = '#E74C3C'  # 跌 - 红色
    ax.plot(df.index[i:i+2], df.close.iloc[i:i+2], color=color, linewidth=3, alpha=0.7)

# 添加最高最低价区域
ax.fill_between(df.index, df.low, df.high, alpha=0.2, color='#3498DB', label='High-Low Range')

# 设置标题和标签（使用英文避免字体问题）
ax.set_title('Shanghai Composite Index Monthly Trend (Last 24 Months)', fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Index Points', fontsize=12)

# 设置x轴日期格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45, ha='right')

# 添加网格
ax.grid(True, linestyle='--', alpha=0.6, linewidth=0.5)

# 添加图例
ax.legend(loc='upper left', fontsize=11)

# 添加数据标签（显示最新值）
latest_close = df.close.iloc[-1]
latest_date = df.index[-1].strftime('%Y-%m-%d')
ax.annotate(f'Latest: {latest_close:.2f}\n{latest_date}', 
            xy=(df.index[-1], latest_close),
            xytext=(10, 20), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='red'),
            fontsize=11, fontweight='bold')

# 添加统计信息
max_price = df.high.max()
min_price = df.low.min()
avg_price = df.close.mean()
stats_text = f'Statistics:\nMax: {max_price:.2f}\nMin: {min_price:.2f}\nAvg: {avg_price:.2f}'
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('基金月线趋势图.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()

print('\nChart saved as: 基金月线趋势图.png')
