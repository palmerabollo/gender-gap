import json
from collections import defaultdict

d_results = dict()
d_results_total = dict()

with open("./output.log") as f:
    for line in f:
        d = json.loads(line)

        if d_results.get(d["search"]) is None:
            d_results[d["search"]] = 0
        if d_results_total.get(d["search"]) is None:
            d_results_total[d["search"]] = 0

        if "female" in d["gender"]:
            d_results[d["search"]] += 1
            d_results_total[d["search"]] += 1
        elif "male" in d["gender"]:
            d_results_total[d["search"]] += 1

for i in d_results:
    d_results[i] = d_results[i] / d_results_total[i]

print(d_results)

##PLOT RESULTS
import pandas as pd
import seaborn as sns
import pylab as plt

#%matplotlib inline
sns.set_style("whitegrid")

df = pd.DataFrame(d_results,index=["Value"]).transpose().reset_index()

#Use 0 as 50-50
df["Value"] -= 0.5
#Make the value go between -100 and +100
df["Value"] *= 200

df = df.sort_values(by="Value")

plt.figure(figsize=(8,3))
sns.barplot(x="Value", y="index", data=df, color="gray")
plt.xlim(-100, 100)
plt.xlabel("Bias")
plt.ylabel("Trabajo/tecnología")
plt.savefig("gender_gap.pdf")