# Importing modules
import streamlit as st
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

# Object
extract = URLExtract()

# -1 => Negative
# 0 => Neutral
# 1 => Positive

def fetch_stats(selected_user,data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    # fetch the number of messages
    num_messages = data.shape[0]

    # fetch the total number of words
    words = []
    for message in data['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = data[data['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in data['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)


# Will return count of messages of selected user per day having k(0/1/-1) sentiment
def week_activity_map(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    return df['day_name'].value_counts()


# Will return count of messages of selected user per month having k(0/1/-1) sentiment
def month_activity_map(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    return df['month'].value_counts()

# Will return hear map containing count of messages having k(0/1/-1) sentiment
def activity_heatmap(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    
    period = []
    for hour in df['hour']:
        if hour == 11:
            period.append(str(hour) + " AM" + "-" + str('12 PM'))
        elif hour == 12:
            period.append(str('12 PM') + "-" + str('1 PM'))
        elif hour == 23:
            period.append(str('11 PM') + "-" + str('12 AM'))
        elif hour == 0:
            period.append(str('12 AM') + "-" + str('1 AM'))
        elif hour < 11:
            period.append(str(hour) + " AM" + "-" + str(hour + 1) + " AM")
        elif hour > 12:
            period.append(str(hour - 12) + " PM" + "-" + str(hour - 11) + " PM")
        else:
            period.append(str(hour) + " PM" + "-" + str(hour + 1) + " PM")
    
    df['period'] = period

    # Set the order of periods explicitly
    period_order = [
        '12 AM-1 AM', '1 AM-2 AM', '2 AM-3 AM', '3 AM-4 AM',
        '4 AM-5 AM', '5 AM-6 AM', '6 AM-7 AM', '7 AM-8 AM',
        '8 AM-9 AM', '9 AM-10 AM', '10 AM-11 AM', '11 AM-12 PM',
        '12 PM-1 PM', '1 PM-2 PM', '2 PM-3 PM', '3 PM-4 PM',
        '4 PM-5 PM', '5 PM-6 PM', '6 PM-7 PM', '7 PM-8 PM',
        '8 PM-9 PM', '9 PM-10 PM', '10 PM-11 PM', '11 PM-12 AM'
    ]

    # Creating heat map
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count', fill_value=0)
    user_heatmap = user_heatmap.reindex(columns=period_order)
    return user_heatmap


# Will return count of messages of selected user per date having k(0/1/-1) sentiment
def daily_timeline(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value']==k]
    # count of message on a specific date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


# Will return count of messages of selected user per {year + month number + month} having k(0/1/-1) sentiment
def monthly_timeline(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value']==-k]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

# Will return percentage of message contributed having k(0/1/-1) sentiment
def percentage(df,k):
    df = round((df['user'][df['value']==k].value_counts() / df[df['value']==k].shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return df

# Return wordcloud from words in message
def create_wordcloud(selected_user,df,k):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Remove entries of no significance
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    # Remove stop words according to text file "stop_hinglish.txt"
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    # Dimensions of wordcloud
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    
    # Actual removing
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'][temp['value'] == k]
    
    # Word cloud generated
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

# Return set of most common words having k(0/1/-1) sentiment
def most_common_words(selected_user,df,k):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message'][temp['value'] == k]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    # Creating data frame of most common 20 entries
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

