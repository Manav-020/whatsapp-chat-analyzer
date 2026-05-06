# import pandas as pd
# import re
# from datetime import datetime


# def preprocessor(data):
#     pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM)\]\s'  # pattern to identify date and time in the chat
#     message = re.split(pattern, data)[1:]  # splitting the data based on tHe pattern
#     user = []
#     dm = []
#     for i in message:
#         entry = re.split('([\w\W]+?):\s', i)
#         if entry[1:]:
#             user.append(entry[1])
#             dm.append(entry[2])
#         # else:
#         #     user.append('group_notification')
#         #     dm.append(entry[0])

#     dates = re.findall(pattern, data)
#     a = [i.replace('[', '') for i in dates]
#     a = [i.replace(']', '').strip().replace(" ", " ") for i in a]

#     d = []
#     for i in a:
#         dt = datetime.strptime(i, "%d/%m/%y, %I:%M:%S %p")
#         d.append(dt.strftime('%Y-%m-%d, %H:%M'))

#     df = pd.DataFrame({'date': d,
#                        'user': user,
#                        'message': dm})
#     if len(df['user'].unique())>2:
#         group_name = df.iloc[0]['user']
#         df = df[df['user'] != group_name]
#     df['date'] = pd.to_datetime(df['date'])
#     df['year'] = df['date'].dt.year
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute
#     df['dates'] = df['date'].dt.date
#     df['month_num'] = df['date'].dt.month
#     df['day_name'] = df['date'].dt.day_name()

#     hours = []
#     for i in df['hour']:
#         if i == 23:
#             hours.append(str(i) + '-' + str('0'))
#         elif i == 0:
#             hours.append(str('0') + '-' + str(i + 1))
#         else:
#             hours.append(str(i) + '-' + str(i + 1))
#     df['period'] = hours

#     return df


import pandas as pd
import re
from datetime import datetime


def preprocessor(data):

    # pattern to identify whatsapp date-time
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM)\]\s'

    # split messages
    messages = re.split(pattern, data)[1:]

    # extract dates
    dates = re.findall(pattern, data)

    users = []
    dm = []

    # extract users and messages
    for message in messages:

        entry = re.split(r'([\w\W]+?):\s', message)

        # normal messages
        if entry[1:]:

            user = entry[1].strip().lower()
            msg = entry[2].strip()

            # unwanted whatsapp notifications
            unwanted_notifications = [
                'pinned a message',
                'changed the group description',
                'changed this group',
                'joined using this group',
                'security code changed',
                'created group',
                'added',
                'left',
                'deleted this message',
                'missed voice call',
                'missed video call'
            ]

            skip = False

            # remove unwanted notifications
            for text in unwanted_notifications:
                if text in msg.lower():
                    skip = True
                    break

            # remove encryption/system messages
            if (
                not skip
                and 'end-to-end encrypted' not in msg.lower()
                and 'messages and calls are end-to-end encrypted' not in msg.lower()
            ):

                users.append(user)
                dm.append(msg)

        # ignore group notifications
        else:
            continue

    # clean dates
    cleaned_dates = []

    for i in dates:
        i = i.replace('[', '').replace(']', '').strip()

        dt = datetime.strptime(i, "%d/%m/%y, %I:%M:%S %p")

        cleaned_dates.append(dt.strftime('%Y-%m-%d, %H:%M'))

    # match lengths correctly
    cleaned_dates = cleaned_dates[:len(users)]

    # dataframe
    df = pd.DataFrame({
        'date': cleaned_dates,
        'user': users,
        'message': dm
    })

    # ---------------------------------------------------
    # REMOVE FAKE USER CREATED FROM GROUP NAME
    # ---------------------------------------------------

    # first user is usually group name/system name
    possible_group_name = df.iloc[0]['user']

    # remove that fake user completely
    df = df[df['user'] != possible_group_name]

    # remove invalid/fake users
    invalid_users = [
        '',
        'null',
        'messages and calls are end-to-end encrypted.'
    ]

    df = df[~df['user'].isin(invalid_users)]

    # ---------------------------------------------------

    # convert date column
    df['date'] = pd.to_datetime(df['date'])

    # date features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['dates'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()

    # create time periods for heatmap
    periods = []

    for hour in df['hour']:

        if hour == 23:
            periods.append('23-0')

        elif hour == 0:
            periods.append('0-1')

        else:
            periods.append(f'{hour}-{hour + 1}')

    df['period'] = periods

    return df