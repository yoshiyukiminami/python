import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

np.random.seed(0)

scores = pd.Series(np.around(np.random.normal(25, 10, 45).clip(0, 60)))
print(scores)

bins = np.linspace(0, 60, 13)
print(bins)

freq = scores.value_counts(bins=bins, sort=False)
print(freq)

class_value = (bins[:-1] + bins[1:]) / 2  # 階級値
rel_freq = freq / scores.count()  # 相対度数
cum_freq = freq.cumsum()  # 累積度数
rel_cum_freq = rel_freq.cumsum()  # 相対累積度数

dist = pd.DataFrame(
    {
        "階級値": class_value,
        "度数": freq,
        "相対度数": rel_freq,
        "累積度数": cum_freq,
        "相対累積度数": rel_cum_freq,
    },
    index=freq.index
)
dist

dist.plot.bar(x="階級値", y="度数", width=1, ec="k", lw=2)

fig, ax1 = plt.subplots()
dist.plot.bar(x="階級値", y="度数", ax=ax1, width=1, ec="k", lw=2)

ax2 = ax1.twinx()
ax2.plot(np.arange(len(dist)), dist["相対累積度数"], "--o", color="k")
ax2.set_ylabel("累積相対度数")

import numpy as np
import pandas as pd

np.random.seed(0)


def get_sample():
    sex = np.random.choice(["男性", "女性"])
    if sex == "男性":
        height = np.random.normal(171, 5.7)
    else:
        height = np.random.normal(157, 5.5)

    return sex, height


df = pd.DataFrame([get_sample() for i in range(500)], columns=["性別", "身長"])
df.head()

ret = df.hist(bins=20, ec="k", lw=2, grid=False)

df[df["性別"] == "男性"].hist(bins=20, ec="k", lw=2, grid=False)
df[df["性別"] == "女性"].hist(bins=20, ec="k", lw=2, grid=False)
