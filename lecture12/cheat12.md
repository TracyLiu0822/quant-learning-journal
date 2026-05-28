# Lecture 12 VaR & 风险度量 Cheatsheet

## 快速公式速查

### 收益率与多期收益
- **日收益率**：$r_t = \frac{P_t - P_{t-1}}{P_{t-1}}$
- **多期复合收益**：$R_T = \prod_{t=1}^{T}(1+r_t) - 1$

### VaR 计算

| 方法 | 公式 | 优点 | 缺点 |
|------|------|------|------|
| **参数法** | $\text{VaR} = P \times (\mu - z\sigma)$ | 快速，只需 μ, σ | 依赖正态假设 |
| **历史法** | $\text{VaR} = P \times r_{(m)}$，$m=\lfloor n(1-\alpha)\rfloor$ | 无分布假设，捕捉极端值 | 样本敏感 |
| **Cornish-Fisher** | $\text{VaR} = P \times (\mu - t\sigma)$，$t = z + \frac{1}{6}(z^2-1)s + ...$ | 考虑偏度/峰度 | 复杂度高 |

其中：$z = \Phi^{-1}(1-\alpha)$ （99% VaR：$z \approx -2.33$）

### Expected Shortfall（ES）
$$\text{ES} = P \times \frac{1}{m}\sum_{i=1}^{m} r_{(i)}$$
> VaR 外的平均损失；ES > VaR

### 组合波动率
- **2资产**：$\sigma_p = \sqrt{w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\text{Cov}(r_1,r_2)}$
- **N资产**：$\sigma_p = \sqrt{\mathbf{w}^T\Sigma\mathbf{w}}$

---

## 核心概念

### 正态性检验
```python
# Shapiro-Wilk 检验（小样本）
stats.shapiro(ret)
# Anderson-Darling 检验
stats.anderson(ret)
```
> 若 p-value < 0.05，拒绝正态性 → 参数法可能低估风险

### 偏度 & 峰度
```python
s = stats.skew(ret)      # 偏度（<0 厚左尾）
k = stats.kurtosis(ret)  # 峰度（>0 厚尾）
```
> 股票收益特征：**负偏 + 高峰度** → 极端亏损更常见

---

## 代码快速参考

### 1. 参数法 VaR
```python
from scipy.stats import norm
z = norm.ppf(1 - 0.99)  # -2.33
ret = df['Adj Close'].pct_change().dropna()
position = n_shares * df['Adj Close'][-1]
var = position * (ret.mean() - z * ret.std())
```

### 2. 历史法 VaR
```python
ret_sorted = np.sort(ret)
m = int(len(ret_sorted) * 0.01)  # 1% tail
var = position * ret_sorted[m]
```

### 3. Cornish-Fisher 修正
```python
s = stats.skew(ret)
k = stats.kurtosis(ret)
t = z + (1/6)*(z**2-1)*s + (1/24)*(z**3-3*z)*k - (1/36)*(2*z**3-5*z)*s**2
var_cf = position * (ret.mean() - t * ret.std())
```

### 4. Expected Shortfall
```python
ret_sorted = np.sort(ret)
m = int(len(ret_sorted) * 0.01)
es = position * ret_sorted[:m].mean()
```

### 5. 多日收益（10天）
```python
df['ret_plus'] = df['Adj Close'].pct_change() + 1
# 按10天分组计算累积收益
ret_10d = df['ret_plus'].groupby(df.index // 10).prod() - 1
# 然后在 ret_10d 上计算 VaR
```

### 6. 2资产组合波动率
```python
def portfolio_vol_2(ret1, ret2, w1):
    s1, s2 = ret1.std(), ret2.std()
    cov = np.cov(ret1, ret2)[0,1]
    return np.sqrt(w1**2*s1**2 + (1-w1)**2*s2**2 + 2*w1*(1-w1)*cov)
```

### 7. N资产组合波动率
```python
def portfolio_vol_n(ret_matrix, weights):
    cov = np.cov(ret_matrix.T)
    w = np.array(weights)
    return np.sqrt(w.dot(cov).dot(w))
```

---

## 关键数值

| 置信水平 | 分位数 z | 对应 % |
|---------|---------|-------|
| 95% | -1.645 | 5% |
| 99% | -2.326 | 1% |
| 99.9% | -3.090 | 0.1% |

---

## 工作流程

1. **数据准备** → 计算日收益率
2. **正态性检验** → 判断是否能用参数法
3. **计算VaR** → 参数法 + 历史法对比
4. **若偏度/峰度显著** → 用 Cornish-Fisher 修正或仅信历史法
5. **计算ES** → 补充尾部风险信息
6. **组合分析** → 计算相关性 → 构建协方差矩阵 → 计算组合波动率

---

## 常见错误

❌ 只用参数法而不检验正态性  
✅ 先做 Shapiro 或 Anderson 检验

❌ 忽视偏度和峰度  
✅ 用 Cornish-Fisher 或历史法修正

❌ VaR 当作最大风险  
✅ VaR + ES 结合使用

❌ 多期 VaR 用简单加法  
✅ 多期收益用复合收益：$(1+r_1)(1+r_2)...-1$

---

> 对应 lecture12_2.ipynb 和 summary.md，快速查询时使用。
