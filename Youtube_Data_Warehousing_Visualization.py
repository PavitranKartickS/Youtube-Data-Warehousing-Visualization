import streamlit as st
from googleapiclient.discovery import build
from pprint import pprint
import pymongo
import mysql.connector
import pandas as pd
import re



api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyDbHi0fSjAAOpyRybADYOmcmy9u-i57mPU"


def get_channel_data(channel_id):
    youtube = build(
            api_service_name, api_version, developerKey = api_key)

    request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id = channel_id
    )
    channel_response = request.execute()
    channel_data = {
        'channel_id': channel_id,
        'channel_name': channel_response['items'][0]['snippet']['title'],
        'channel_description': channel_response['items'][0]['snippet']['description'],
        'channel_views': channel_response['items'][0]['statistics']['viewCount'],
        'channel_subscribers': channel_response['items'][0]['statistics']['subscriberCount'],
        'channel_vid_count': channel_response['items'][0]['statistics']['videoCount'],
    }
    return channel_data

def get_video_ids(channel_id):
    video_ids = []
    youtube = build(
            api_service_name, api_version, developerKey = api_key)
    response = youtube.channels().list(
        id = channel_id,
        part='contentDetails').execute()
    Playlist_Id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token=None

    while True:
        response1=youtube.playlistItems().list(
                                            part='snippet',
                                            playlistId=Playlist_Id,
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token=response1.get('nextPageToken')
        
        if next_page_token is None:
            break
    return video_ids
        

def get_video_data(video_ids):
    video_data = []
    youtube = build(
            api_service_name, api_version, developerKey = api_key)
    for video_id in video_ids:
        response2 = youtube.videos().list(
            part = 'snippet,contentDetails,statistics',
            id = video_id
        ).execute()

        for item in response2['items']:
            data=dict(
                channel_id=item['snippet']['channelId'],
                channel_name=item['snippet']['channelTitle'],
                Video_Id=item['id'],
                Title=item['snippet']['title'],
                Description=item['snippet'].get('description'),
                Published_date=datetrim(item['snippet']['publishedAt']),
                Duration=timecalc(str(item['contentDetails']['duration'])),
                Views=item['statistics'].get('viewCount'),
                Likes=item['statistics'].get('likeCount'),
                Comments=item['statistics'].get('commentCount'),
                Favorite_count=item['statistics']['favoriteCount'],
                Caption_status=item['contentDetails']['caption'],
                Thumbnail=item['snippet']['thumbnails']['default']['url']
                     )
        video_data.append(data)
    return video_data

def datetrim(published_date):
    date=''
    for i in published_date:
        result=published_date.split("T")
        date=result[0]
    return date

def timecalc(duration_str):
    # Define a regular expression pattern
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')

    # Use re.match to extract groups
    match = pattern.match(duration_str)

    if match:
        # Extract hours, minutes, and seconds from groups
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0

        # Convert to seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    else:
        print("Invalid duration format")
        return 0


def get_comment_data(video_ids):
    comment_data=[]
    youtube = build(
            api_service_name, api_version, developerKey = api_key)
    for video_id in video_ids:
        request=youtube.commentThreads().list(
            part="snippet",
            videoId= video_id,
            maxResults=100
        )
        response=request.execute()

        for item in response['items']:
            data=dict(comment_id=item['snippet']['topLevelComment']['id'],
                        Video_id=item['snippet']['topLevelComment']['snippet']['videoId'],
                        Comment_Text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        Comment_Author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        Comment_published=datetrim(item['snippet']['topLevelComment']['snippet']['publishedAt']))

            comment_data.append(data)
    return comment_data

#Connecting to mongo db
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient['YtubeData']

def channel_collection(channel_id):
    cha_details = get_channel_data(channel_id)
    vid_ids = get_video_ids(channel_id)
    vid_details = get_video_data(vid_ids)
    com_details = get_comment_data(vid_ids)
        
    
    col = db['Channel_Details']
    col.insert_one({"channel_information":cha_details,
                        "video_information":vid_details,
                        "comment_information":com_details})
         
    return "Channel uploaded successfully"
    
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345"
)
mycursor = mydb.cursor()
try:
    query = "create database Ytube_Data"
    mycursor.execute(query)
except:
    pass

def channels_table():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="Ytube_Data"
    )
    mycursor = mydb.cursor()
    drop_query = "drop table if exists channels"
    mycursor.execute(drop_query)
    mydb.commit()
    
    try:
        create_query = '''create table if not exists channels(
        channel_id varchar(100) primary key,
        channel_name varchar(200),
        channel_subscribers bigint,
        channel_views bigint,
        channel_vid_count bigint,
        channel_description text
        )'''
        mycursor.execute(create_query)
        mydb.commit()
    except:
        print("Table already exists")

    ch_list=[]
    db = myclient['YtubeData']
    col = db['Channel_Details']
    for chdata in col.find({},{"_id":0,"channel_information":1}):
        ch_list.append(chdata["channel_information"])
    df1=pd.DataFrame(ch_list)

    
    for index,row in df1.iterrows():
        insert_query='''insert into channels(channel_id,
                                             channel_name,
                                             channel_subscribers,
                                             channel_views,
                                             channel_vid_count,
                                             channel_description
                                             )

                                             values(%s,%s,%s,%s,%s,%s)'''
        values=(row['channel_id'],
                row['channel_name'],
                row['channel_subscribers'],
                row['channel_views'],
                row['channel_vid_count'],
                row['channel_description'],
                )
        try:
            mycursor.execute(insert_query,values)
            mydb.commit()
        except:
            print("Channel table values already inserted")


def videos_table():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="Ytube_Data"
    )
    mycursor = mydb.cursor()
    drop_query = "drop table if exists videos"
    mycursor.execute(drop_query)
    mydb.commit()

    try:
        create_query='''create table if not exists videos(channel_id varchar(100),
                                                      channel_name varchar(100),
                                                      Video_Id varchar(30) primary key,
                                                      Title varchar(150),
                                                      Description text,
                                                      Published_date date,
                                                      Duration varchar(100),
                                                      Views bigint,
                                                      Likes bigint,
                                                      Comments int,
                                                      Favorite_count int,
                                                      Caption_status varchar(50),
                                                      Thumbnail varchar(250)
                                                      )'''
        mycursor.execute(create_query)
        mydb.commit()
    except:
        print("Video table already created")

    vid_list=[]
    db = myclient['YtubeData']
    col = db['Channel_Details']
    for vidata in col.find({},{"_id":0,"video_information":1}):
        for i in range(len(vidata["video_information"])):
            vid_list.append(vidata["video_information"][i])   
    df2=pd.DataFrame(vid_list)

    for index,row in df2.iterrows():
            insert_query='''insert into videos(channel_id,
                                                  channel_name,
                                                  Video_Id,
                                                  Title,
                                                  Description,
                                                  Published_date,
                                                  Duration,
                                                  Views,
                                                  Likes,
                                                  Comments,
                                                  Favorite_count,
                                                  Caption_status,
                                                  Thumbnail
                                                 )

                                                 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            values=(row['channel_id'],
                    row['channel_name'],
                    row['Video_Id'],
                    row['Title'],
                    row['Description'],
                    row['Published_date'],
                    row['Duration'],
                    row['Views'],
                    row['Likes'],
                    row['Comments'],
                    row['Favorite_count'],
                    row['Caption_status'],
                    row['Thumbnail']
                   )
            mycursor.execute(insert_query,values)
            mydb.commit()


def comments_table():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="Ytube_Data"
    )
    mycursor = mydb.cursor()
    drop_query = "drop table if exists comments"
    mycursor.execute(drop_query)
    mydb.commit()
    
    try:
        create_query='''create table if not exists comments(comment_id varchar(100) primary key,
                                                        Video_id varchar(50),
                                                        Comment_Text text,
                                                        Comment_Author varchar(150),
                                                        Comment_published date
                                                        )'''

        mycursor.execute(create_query)
        mydb.commit()
    except:
        print("Comment Table already created")

    com_list = []
    db = myclient['YtubeData']
    col = db['Channel_Details']
    for comdata in col.find({},{"_id":0,"comment_information":1}):
        for i in range(len(comdata["comment_information"])):
            com_list.append(comdata["comment_information"][i])   
    df3 = pd.DataFrame(com_list)
    
    
    for index,row in df3.iterrows():
            insert_query='''insert into comments(comment_id,
                                                 Video_id,
                                                 Comment_Text,
                                                 Comment_Author,
                                                 Comment_published
                                                )

                                                 values(%s,%s,%s,%s,%s)'''
            values=(row['comment_id'],
                    row['Video_id'],
                    row['Comment_Text'],
                    row['Comment_Author'],
                    row['Comment_published']
                   )

            mycursor.execute(insert_query,values)
            mydb.commit()


def tables():
    channels_table()
    videos_table()
    comments_table()
    
    return "Tables have been created successfully"



def show_channel_tables():
    ch_list=[]
    db = myclient['YtubeData']
    col = db['Channel_Details']
    for chdata in col.find({},{"_id":0,"channel_information":1}):
        ch_list.append(chdata["channel_information"])
    df1 = pd.DataFrame(ch_list)

    return df1


def show_video_tables():
    vid_list=[]
    db = myclient['YtubeData']
    col = db['Channel_Details']
    for vidata in col.find({},{"_id":0,"video_information":1}):
        for i in range(len(vidata["video_information"])):
            vid_list.append(vidata["video_information"][i])   
    df2 = pd.DataFrame(vid_list)

    return df2


def show_comment_tables():
    com_list = []
    db = myclient['YtubeData']
    col = db['Channel_Details']
    for comdata in col.find({},{"_id":0,"comment_information":1}):
        for i in range(len(comdata["comment_information"])):
            com_list.append(comdata["comment_information"][i])   
    df3 = pd.DataFrame(com_list)

    return df3



# STREAMLIT
st.set_page_config(page_title="Youtube Data Harvesting and Warehousing using MongoDB and SQL", layout="wide")


#Title
st.title("Youtube Data Harvesting and Warehousing using MongoDB and SQL")

st.write("##")
with st.container():
    st.header("Skills Expressed :")

    st.write(
        """
        - Python Scripting  
        - Youtube API Data retrieval  
        - MongoDB Warehousing  
        - SQL warehousing 
        - Streamlit Use
        """
        )

with st.container():
    st.write("---")

with st.container():
    col1,col2 = st.columns([1,3])
    
    with col1:
        st.header("Data Scrapping")
        channel_id = st.text_input("Enter the channel ID whose data is to be retrieved:") 
        if st.button("Collect and store the data"):
            ch_ids=[]
            db = myclient['YtubeData']
            col = db['Channel_Details']
            for cha_data in col.find({},{"_id":0,"channel_information":1}):
                ch_ids.append(cha_data["channel_information"]["channel_id"])
        
            if channel_id in ch_ids:
                st.success("Channel Details of the given channel id already exists")
        
            else:
                insert=channel_collection(channel_id)
                st.success(insert)
        
        if st.button("Migrate Data to sql"):
            Table=tables()
            st.success(Table)

    with col2:
        st.header("Data Presentation")
        show_table=st.radio("Select the Table you wish to view",("Channels","Videos","Comments"))

        if show_table =="Channels":
            table1 = show_channel_tables()
            st.write(table1)

    
        elif show_table =="Videos":    
            table2 = show_video_tables()
            st.write(table2)    

        elif show_table =="Comments":    
            table3 = show_comment_tables()
            st.write(table3)


with st.container():
    st.write("---")

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="Ytube_Data"
    )
mycursor = mydb.cursor()

with st.container():
    question=st.selectbox("Select your Query",("1. What are the names of all the videos and their corresponding channels?",
                                               "2. Which channels have the most number of videos, and how many videos do they have?",
                                               "3. What are the top 10 most viewed videos and their respective channels?",
                                               "4. How many comments were made on each video, and what are their corresponding video names?",
                                               "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
                                               "6. What is the total number of likes , and what are their corresponding video names?",
                                               "7. What is the total number of views for each channel, and what are their corresponding channel names?", 
                                               "8. What are the names of all the channels that have published videos in the year 2022?",
                                               "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?", 
                                               "10. Which videos have the highest number of comments, and what are their corresponding channel names?"))
    
    
    if question=="1. What are the names of all the videos and their corresponding channels?":
        query1='''select title as videos,channel_name as channelname from videos'''
        mycursor.execute(query1)
        t1=mycursor.fetchall()
        df=pd.DataFrame(t1,columns=["video title","channel name"])
        st.write(df)

    elif question=="2. Which channels have the most number of videos, and how many videos do they have?":
        query2='''select channel_name as channelname,channel_vid_count as no_videos from channels
                order by channel_vid_count desc'''
        mycursor.execute(query2)
        t2=mycursor.fetchall()
        df2=pd.DataFrame(t2,columns=["channel name","No of videos"])
        st.write(df2)

    elif question=="3. What are the top 10 most viewed videos and their respective channels?":
        query3='''select views as views,channel_name as channelname,title as videotitle from videos
                where views is not null order by views desc limit 10'''
        mycursor.execute(query3)
        t3=mycursor.fetchall()
        df3=pd.DataFrame(t3,columns=["views","channel name","videotitle"])
        st.write(df3)
    
    elif question=="4. How many comments were made on each video, and what are their corresponding video names?":
        query4='''select comments as no_comments,title as videotitle from videos where comments is not null'''
        mycursor.execute(query4)
        t4=mycursor.fetchall()
        df4=pd.DataFrame(t4,columns=["no comments","videotitle"])
        st.write(df4)
    
    elif question=="5. Which videos have the highest number of likes, and what are their corresponding channel names?":
        query5='''select title as videotitle,channel_name as channelname,Likes as likecount
                    from videos where likes is not null order by Likes desc'''
        mycursor.execute(query5)
        t5=mycursor.fetchall()
        df5=pd.DataFrame(t5,columns=["videotitle","channelname","likecount"])
        st.write(df5)   
    
    elif question=="6. What is the total number of likes , and what are their corresponding video names?":
        query6='''select Likes as likecount,title as videotitle from videos'''
        mycursor.execute(query6)
        t6=mycursor.fetchall()
        df6=pd.DataFrame(t6,columns=["likecount","videotitle"])
        st.write(df6)
    
    elif question=="7. What is the total number of views for each channel, and what are their corresponding channel names?":
        query7='''select channel_name as channelname ,channel_views as totalviews from channels'''
        mycursor.execute(query7)
        t7=mycursor.fetchall()
        df7=pd.DataFrame(t7,columns=["likecount","videotitle"])
        st.write(df7)
    
    elif question=="8. What are the names of all the channels that have published videos in the year 2022?":
        query8='''select title as video_title,published_date as videorelease,channel_name as channelname from videos
            where extract(year from published_date)=2022'''
        mycursor.execute(query8)
        t8=mycursor.fetchall()
        df8=pd.DataFrame(t8,columns=["videotitle","published_date","channelname"])
        st.write(df8)
    
    elif question=="9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
        query9='''select channel_name as channelname,AVG(duration) as averageduration from videos group by channel_name'''
        mycursor.execute(query9)
        t9=mycursor.fetchall()
        df9=pd.DataFrame(t9,columns=["channelname","averageduration"])
        T9=[]
        for index,row in df9.iterrows():
            channel_title=row["channelname"]
            average_duration=row["averageduration"]
            average_duration_str=str(average_duration)
            T9.append(dict(channeltitle=channel_title,avgduration=average_duration_str))
            df1=pd.DataFrame(T9)
        st.write(df1)
        
    elif question=="10. Which videos have the highest number of comments, and what are their corresponding channel names?":
        query10='''select title as videotitle, channel_name as channelname, comments as comments from videos where comments is
                    not null order by comments desc'''
        mycursor.execute(query10)
        t10=mycursor.fetchall()
        df10=pd.DataFrame(t10,columns=["video title","channel name","comments"])
        st.write(df10)