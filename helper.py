import re
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch(selected_user,df):
    emoji_list=[]
    words = []
    count=0
    links=[]
    extractor=URLExtract()
    if selected_user!='overall':
        df=df[df['user'] == selected_user]


    for i in df['message']:
        words.extend(i.split(' '))
        if 'omitted' in re.findall('omitted', i):
            count+=1
        emoji_list.extend([e['emoji'] for e in emoji.emoji_list(i)])
        links.extend(extractor.find_urls(i))
    emoji_df=pd.DataFrame(Counter(emoji_list).most_common(10))
    emoji_df.rename(columns=({0:'Emoji',1:'Emoji_count'}),inplace=True)
    return df.shape[0],len(words),count,len(links),emoji_df


def active(df):
    return df['user'].value_counts().head()

def create_wordcloud(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    l = []
    for i in df['message']:
        if 'omitted' not in i:
            l.extend(i.split(" "))

    wc=WordCloud(width=500, height=500, background_color='white',max_font_size=50)
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common(selected_user,df):
    if selected_user != 'overall':
        df=df[df['user'] == selected_user]
    temp=df[df['user']!='group_notification']
    common_words=[]
    for i in temp['message']:
        if 'omitted' not in i:
            common_words.extend(i.split(' '))
    return pd.DataFrame(Counter(common_words).most_common(20))


def month_timeline(selected_user,df):
    if selected_user != 'overall':
        df=df[df['user'] == selected_user]
    timeline= df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    t = []
    for i in range(timeline.shape[0]):
        t.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['xlabels'] = t

    timeline_date = df.groupby(['dates']).count()['message'].reset_index()
    return timeline,timeline_date

def busy_day(selected_user,df):
    if selected_user != 'overall':
        df=df[df['user'] == selected_user]
    return df.groupby(['day_name']).count()['message'].reset_index()

def busy_month(selected_user,df):
    if selected_user != 'overall':
        df=df[df['user'] == selected_user]
    return  df.groupby(['month']).count()['message'].reset_index()

def heatmap(selected_user,df):
    if selected_user != 'overall':
        df=df[df['user'] == selected_user]
    return pd.pivot_table(index='day_name', columns='period', values='message', aggfunc='count', data=df).fillna(0)

def ghost_finder(df):
    h = df.groupby(['year', 'month'])['message'].count().reset_index()
    g = (df.groupby(['year', 'month', 'user'])['message'].count() * 100).reset_index()

    ghost = g.merge(h, left_on=['year', 'month'], right_on=['year', 'month'])

    ghost['percentage'] = ghost['message_x'] / ghost['message_y']
    return ghost[ghost['percentage'] < 2].groupby(['user'])['percentage'].count().reset_index()