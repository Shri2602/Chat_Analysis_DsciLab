# 24 Hrs Format

# # Importing modules
# import re
# import pandas as pd

# # To convert text into data frame in desired form
# def preprocess(data):
    
#     # Regular expression
#     pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
#     # Split text file into messages & dates based on pattern
#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)
    
#     # Creating data frame
#     df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
#     # convert dates type
#     try:
#         df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
#     except:
#         df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
#     df.rename(columns={'message_date': 'date'}, inplace=True)

#     users = []
#     messages = []
#     for message in df['user_message']:# For each message in user_message
        
#         # Split message based on '([\w\W]+?):\s'
#         entry = re.split('([\w\W]+?):\s', message)
#         if entry[1:]: 
#             # User name
#             users.append(entry[1])
#             # Only message
#             messages.append(" ".join(entry[2:]))
#         else:
#             # Adding group notifications
#             users.append('group_notification')
            
#             # Null value
#             messages.append(entry[0])
    
#     # Creating new columns
#     df['user'] = users
#     df['message'] = messages
    
#     # Remove columns of no use
#     df.drop(columns=['user_message'], inplace=True)
    
#     # Extract date
#     df['only_date'] = df['date'].dt.date
    
#     # Extract year
#     df['year'] = df['date'].dt.year
    
#     # Extract month
#     df['month_num'] = df['date'].dt.month
    
#     # Extract month name
#     df['month'] = df['date'].dt.month_name()
    
#     # Extract day
#     df['day'] = df['date'].dt.day
    
#     # Extract day name
#     df['day_name'] = df['date'].dt.day_name()
    
#     # Extract hour
#     df['hour'] = df['date'].dt.hour
    
#     # Extract minute
#     df['minute'] = df['date'].dt.minute

#     # Remove entries having user as group_notification
#     df = df[df['user'] != 'group_notification']
    
#     # Returning preprocessed data frame
#     return df

# 12 Hrs Format
import re
import pandas as pd


def preprocess(data):
    # Pattern in chat ( Spliting DataTime and Msg)
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s"
    # pattern='\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)'     
    # All msgs we have
    message = re.split(pattern, data)[1:]
    # All date we have
    dates = re.findall(pattern, data)
    # Split Date and Time
    date = []
    times = []
    for i in dates:
        date.append(i.split(", ")[0])
        times.append(i.split(", ")[1])

    time = []
    for i in times:
        time.append(i.split("\u202f")[0])
    # Create DataFrame¶
    df = pd.DataFrame({
        'user_msg': message,
        'date': date,
        'time': time
    })
    # Spliting user name and msg
    user = []
    msg = []
    for i in df['user_msg']:
        x = re.split("([\w\W]+?):\s", i)
        if x[1:]:  # user name
            user.append(x[1])
            msg.append(x[2])
        else:
            user.append('Group Notification')
            msg.append(x[0])

    df['user'] = user
    df['message'] = msg
    df.drop(columns=['user_msg'], inplace=True)

    # Convert Date Column into DateTime format
    df['date'] = pd.to_datetime(df['date'])
    # df['only_date'] = df['date'].dt.year
    # df['year'] = df['date'].dt.year
    # df['month_num'] = df['date'].dt.month
    # df['month'] = df['date'].dt.month_name()
    # df['day'] = df['date'].dt.day
    # df['day_name'] = df['date'].dt.day_name()
    # df['hour'] = df['date'].dt.hour
    # df['minute'] = df['date'].dt.minute

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
   


    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df