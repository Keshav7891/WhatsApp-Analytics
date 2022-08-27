from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':    #if we select a particular user
        df = df[df['user'] == selected_user]

    # number of messages
    num_messages = df.shape[0]

    # number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #number of media
    num_media_messages = df[df['message']=='<Media omitted>\n'].shape[0]

    #number of links
    links = []
    extractor = URLExtract() #creating object
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'Name', 'user': 'Contribution% '})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':    #if we select a particular user
        df = df[df['user'] == selected_user]
    # Remove Group Notifications
    temp = df[df['user'] != 'group_notification']

    # Remove Media Omiited
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Remove Stop Words
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500,min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':    #if we select a particular user
        df = df[df['user'] == selected_user]

    # Remove Group Notifications
    temp = df[df['user'] != 'group_notification']

    # Remove Media Omiited
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Remove Stop Words
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    # Top words used in chats
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df



