import pandas as pd
import re
from datetime import datetime


def preprocessor(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM)\]\s'  # pattern to identify date and time in the chat
    message = re.split(pattern, data)[1:]  # splitting the data based on tHe pattern
    user = []
    dm = []
    for i in message:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            user.append(entry[1])
            dm.append(entry[2])
        # else:
        #     user.append('group_notification')
        #     dm.append(entry[0])

    dates = re.findall(pattern, data)
    a = [i.replace('[', '') for i in dates]
    a = [i.replace(']', '').strip().replace(" ", " ") for i in a]

    d = []
    for i in a:
        dt = datetime.strptime(i, "%d/%m/%y, %I:%M:%S %p")
        d.append(dt.strftime('%Y-%m-%d, %H:%M'))

    df = pd.DataFrame({'date': d,
                       'user': user,
                       'message': dm})
    if len(df['user'].unique())>2:
        group_name = df.iloc[0]['user']
        df = df[df['user'] != group_name]
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['dates'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()

    hours = []
    for i in df['hour']:
        if i == 23:
            hours.append(str(i) + '-' + str('0'))
        elif i == 0:
            hours.append(str('0') + '-' + str(i + 1))
        else:
            hours.append(str(i) + '-' + str(i + 1))
    df['period'] = hours

    return df