import pandas as pd


data = pd.read_csv("data.csv") 
title_list = data["title"]
clean_title_list =[]
for index,x in enumerate(title_list):
    if(index == 689):
        import pdb;pdb.set_trace();
    if x.strip() != "":
        clean_title_list.append(x.strip())
pd.Series(clean_title_list).to_csv("title.txt",index=False,header=None)
