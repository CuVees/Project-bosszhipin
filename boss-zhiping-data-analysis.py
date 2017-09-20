
# coding: utf-8

# # **boss直聘网数据分析师岗位分析**

# ## 项目背景

# 本项目打算着重复习python数据分析相关的知识，主要包括numpy, pandas和matplotlib这几个库。

# ## 项目简介

# 要想从事数据分析师职业，就得对这个职业有充分的了解，最直观的方式就是从企业，公司获得需求分析，进而完善自己的知识储备和简历。
# 本次项目利用网络爬虫爬取boss直聘网有关数据分析师的这一岗位的信息，然后进行一些探索和分析。

# ## 数据来源和数据集

# 本次项目所有数据集均来自boss直聘网，是通过集搜客这一软件采集的。
# 本次爬取信息时，主要获得以下信息:
# * 岗位名称：       title
# * 月薪：          month_salary
# * 公司：          company
# * 所属行业：       industry
# * 规模：          scale
# * 融资阶段：       phase
# * 所在城市：       city
# * 经验要求：       experience
# * 学历要求：       education
# * 岗位描述和技能需求：description

# ## 目的

# 主要是希望针对实际的数据解答一些有关数据岗位的疑惑：
# 1. 数据分析师岗位需求的地域性分布
# 2. 整个群体中的薪酬分布情况
# 3. 不同城市数据分析师的薪酬是怎样的
# 4. 该岗位对工作经验的要求是怎样的
# 5. 不同经验的数据分析师薪酬是怎样变化的
# 6. 从用人角度看，数据分析师应该具备怎样的技能
# 7. 掌握不同技能是否对薪酬有影响，影响怎样

# ## 技术和工具

# 本项目主要分为两大部分，第一部分是数据爬取，采用的是集搜客网络爬虫工具。第二部分是数据分析，以python编程语言为基础。

# # 数据整理

# ### 加载和整理

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import jieba
import jieba.analyse
import random
from wordcloud import WordCloud
import pprint 
get_ipython().magic('matplotlib inline')


# In[2]:

# 由于matplotlib默认字体不是中文字体，在进行中文显示的时候只有一个框框，因此必须显式的指定字体文件
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# 有中文出现的情况，需要u'内容'


# In[3]:

df=pd.read_excel('C:/Users/zhou/Desktop/project_bosszhipin_data/list_bosszhipin.xlsx')

# 清理不需要的字段
df=df.drop([u'_clueid',u'_fullpath',u'_realpath',u'_theme',u'_middle',u'_createdate',u'_pageno',
              u'_actionno',u'_actionvalue',u'_prestamp',u'_currentstamp'],axis=1)

# 清理重复行
df=df.drop_duplicates(['company','title','description'])

print (df.info())


# 可以看到，经过处理后，数据集中为13个变量，数据记录为388条。除scale（规模）这一字段外，其余均没有缺失值。

# # 数据分析

# ## 地域性分布

# In[4]:

# 观察地域分布情况
city_group=df.groupby('city')['title'].count().sort_values(ascending=False)

# 绘图
fig=plt.figure(figsize=(36,20))
ax1=plt.subplot(111)
rect1=ax1.bar(range(len(city_group)),city_group.values,width=0.5)

# 设置x轴标签
def set_xtricks(rects,xtricks):
    x=[]
    for rect in rects:
        x.append(rect.get_x()+rect.get_width()/2)
    x=tuple(x)
    plt.xticks(x,xtricks)
    
set_xtricks(rect1,city_group.index)

# 设置数据标签
def set_tags(rects,data=None,offset=[0,0]):
    for rect in rects:
        try:
            height=rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2.4,1.1*height,'%s' % int(height))
        except AttributeError:
            x = range(len(data))
            y = data.values
            for i in range(len(x)):
                    plt.text(x[i]+offset[0],y[i]+0.05+offset[1],y[i])

set_tags(rect1)
ax1.set_title(u'不同城市需求量')


# 在boss直聘网上，全国有34个城市的企业邮数据分析师的人才需求，其中将近一半需求产生在北京市，需求量全国第一。排在前5的分别是：北京、上海、杭州、深圳、广州。

# 数据分析这一职业大量集中在北上广深四大一线城市，以及杭州这个互联网和电子商务企业的聚集地。

# 总而言之，可以得出一个清晰的结论：**数据分析这一岗位，有大量的工作机会集中在北上广深以及杭州**，期待往这个方向发展的同学还是要到这些城市去多多尝试。当然，从另一个方面说，这些城市也都集中了大量的各行业人才，竞争压力想必也是很大的。

# ## 总体薪酬情况

# In[5]:

#查看薪酬分布
#由于拉勾网上的薪酬分布是个区间范围，并且多有重叠部分，不便于量化分析
#因此将此数据进行清理，取区间的均值作为薪酬值
def salary_avg(salary):
    #该函数传入一个薪酬区间字符串，并将其转换成区间均值并返回
    try:
        s_list = salary.split('-')
        s_min = int(s_list[0][:-1])
        s_max = int(s_list[1][:-1])
        s_avg = float(s_min + s_max)/2
    except UnicodeEncodeError:
        s_list = salary.split('k')
        s_avg = float(int(s_list[0][:-1]))
    return s_avg
                      
df['salary_avg']=df['month_salary'].apply(salary_avg)

fig = plt.figure(figsize =  (8,5))
ax2 = plt.subplot(111)
rect2=ax2.hist(df['salary_avg'],bins=30)
ax2.set_title(u'薪酬分布')
ax2.set_xlabel(u'K/月')
plt.xticks(range(5,100,5))


# 大多数人的收入集中在5k-20k每月，只有少数人能够获得更高的薪酬，但有极少数人薪酬极高.需要说明的是，boss直聘网上的薪酬值是一个区间值，并且相互之间互有重叠，为了便于分析，我取区间的中值作为代表值进行的分析。因此，实际的薪酬分布情况可能会比图中的情况更好一些。总是有人能够拿到薪酬的上限。

# 综合来看，数据分析师的薪酬收入整体还是可观的，从这方面说，选择这个职业还是不错的。

# ## 不同城市薪酬情况

# In[6]:

#观察分城市的薪酬分布箱线图
count_by_city_salary = df.groupby(['city'])['salary_avg']
    
#取前6个城市的数据
six_data_by_city = city_group[0:6]

# 许多城市的数据太少，因此着重分析前六个城市的数据
data = []
for group in six_data_by_city.index:
    v = count_by_city_salary.get_group(group).values
    data.append(v)

fig = plt.figure(figsize = (8,5))
ax3 = plt.subplot(111)
rect3 = ax3.boxplot(data)

#设置标签
ax3.set_xticklabels(six_data_by_city.index)
plt.yticks(range(0,60,5))
ax3.set_title(u'不同薪酬分布')
ax2.set_xlabel(u'K/月')


# 忽略掉那些人才需求量比较小的城市，我重点关注排名前六的城市。从图上看，这六大城市的薪酬分布情况总体来说都比较集中，这和我们前面看到的全国的薪酬总体情况分布是一致的。杭州市薪酬分布中位数大约在19k,居全国首位。其次是北京，约155k，之后是上海和深圳。

# **从待遇上看，数据分析师留在杭州发展是个不错的选择。**

# ## 工作经验需求

# In[7]:

# 观察工作经验分布
# 根据实际经验，‘经验不限’和‘应届毕业生’这两个描述，基本等同于工作经验要求1年以下
# 把这几个合并
for i in range(len(df['experience'])):
    if df['experience'].iloc[i] in [u'经验不限',u'应届生',]:
         df['experience'].iloc[i] = u'1年以内'
    
count_by_experience = df.groupby(['experience'])['title'].count()

#绘制条形图
fig = plt.figure(figsize = (8,4))
ax4 = plt.subplot(111)
rect4 = ax4.bar(np.arange(len(count_by_experience)), count_by_experience.values,width = 0.5)
set_xtricks(rect4,count_by_experience.index)
ax4.set_title(u'工作经验分布')


# 不出所料,工作1-3年经验的熟手需求量最大，其次是3-5年工作经验的资深分析师。工作经验不足1年的新人，市场需求量比较少。另外，工作经验要5-10年的需求量非常稀少。

# 从这个分布我们大致可以猜测出：
# 1. **数据分析是个年轻的职业方向，大量的工作经验需求集中在1-3年**；
# 2. **对于数据分析师来说，5年是个瓶颈期，如果在5年之内没有转型或者质的提升，大概以后的竞争压力会比较大。**

# ## 不同工作经验的薪酬分布

# In[8]:

# 不同工作经验的薪酬分布
group_by_exp=df.groupby(['experience'])['salary_avg']

data=[]
for group in count_by_experience.index:
    v=group_by_exp.get_group(group).values
    data.append(v)
    
fig=plt.figure(figsize=(10,5))
ax5=plt.subplot(111)
rect5=ax5.boxplot(data)

ax5.set_xticklabels(count_by_experience.index)
ax5.set_title(u'不同经验的薪酬分布')
ax5.set_ylabel(u'K/月')


# 毫无疑问的，随着经验的提升，数据分析师的薪酬也在不断提高。另外，从现有数据来看，**数据分析师似乎是个常青的职业方向，在10年内大概不会因为年龄的增长导致收入下降**。

# ## 职业技能关键词

# In[21]:

#首先抽取关键词
def key_word(text):
    key_words = jieba.analyse.extract_tags(text, topK=20, withWeight=False, allowPOS=())
    return key_words
    
df['key_words'] = df['description'].apply(key_word)
    
#启用自定义字典
jieba.load_userdict('C:/Users/zhou/Desktop/project_bosszhipin_data/userdict.txt')
jieba.suggest_freq('office', False)
    
#创建一个文本，将关键词列表全部写入该文本
def write_to_text(word_list):
    f = open('C:/Users/zhou/Desktop/project_bosszhipin_data/word_list_text.txt','a')
    for word in word_list:
            f.writelines(word+',')
    f.close()
    
df['key_words'].apply(write_to_text)
    
text = open('C:/Users/zhou/Desktop/project_bosszhipin_data/word_list_text.txt','r').read()

# 只提取英文字符
import re
text=re.sub('[^a-zA-Z],','',text)

#通过wordcloud提供的接口，读入文本文件后自动根据词频绘制词云
word=WordCloud(width=800,height=400,background_color='white').generate(text)

fig=plt.figure(figsize=(20,15))
plt.imshow(word)


# 对于数据分析师这一岗位，企业需求频率最高的技能并不是Python语言和R语言等如今非常时髦的数据分析语言，而是ppt和Excel。这一点需要各位小伙伴注意，另外SAS和SPSS的需求量也多。

# 从词云上看出，数据分析师技能需求频率排在前列的有：**Excel, SAS，SPSS,SQL， Python, Hadoop和MySQL等。另外，Java, PPT, BI软件等属于第二梯队**。

# # 分析结论

# 通过上面的分析，我们可以得到的结论有这些：
# 1. 数据分析这一岗位，有大量的工作机会集中在北上广深以及杭州。
# 2. 大多数据分析师的收入集中在5k-20k每月，只有少数人能够获得更高的薪酬。
# 3. 从待遇上看，数据分析师留在杭州发展是个不错的选择，其次是北京、上海。
# 4. 数据分析是个年轻的职业方向，大量的工作经验需求集中在1-3年。
# 5. 对于数据分析师来说，5年似乎是个瓶颈期，如果在5年之内没有转型或者质的提升，大概以后的竞争压力会比较大。
# 6. 随着经验的提升，数据分析师的薪酬也在不断提高，10年以上工作经验的人，能获得相当丰厚的薪酬。
# 7. 数据分析师需求频率排在前列的技能有：PPT，Excel, SAS，SPSS,SQL, Python, Hadoop和MySQL等，其中PPT和Excel简直可以说是必备技能。
