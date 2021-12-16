import seaborn as sns
import pandas as pd
import re
import glob 
import os
import matplotlib.pyplot as plt
from collections import Counter

Times = []
Flips = []
Errors = []
Subjects = []
#Read in all log files, combine into dataset
for file in glob.glob("Logs_ToUse/*.log"):
    with open(os.path.join(os.getcwd(), file), 'r') as f:
        content = f.readlines()
        Times.append(re.search('[0-9]+', content[2]).group(0))
        Flips.append(re.search('[0-9]+', content[3]).group(0))
        Subjects.append(re.sub('\n', '', content[0].split(":: ",1)[1])) 
        text = re.search('\[(.*?)\]+', content[5]).group(1)
        text = text.split(", ")
        Number = Counter(text)
        err = 0
        for n in Number.values():
            if n>2:
                err = err + (n-2)
        Errors.append(err)


data = pd.DataFrame(list(zip(Subjects, Times, Flips, Errors)), columns =['Subjects', 'Times', 'Flips', 'Errors'])
data.Times = pd.to_numeric(data.Times)
data.Flips = pd.to_numeric(data.Flips)

#Plot histograms for Times and Flips
fig, axes = plt.subplots(1, 3)
data.hist('Times', ax=axes[0])
data.hist('Flips', ax=axes[1])
data.hist('Errors', ax=axes[2])
plt.show()