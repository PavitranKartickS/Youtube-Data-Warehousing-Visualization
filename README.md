# YouTube Data Harvesting and Warehousing using SQL, MongoDB, and Streamlit


# Introduction:
The title of this project is Youtube Data Harvesting and Warehousing. This project intends to provide a user friendly interface 
to common users which allows the accessing and retrieving the data of select youtube channels, and their respective data.
An easy to use environment has been created to serve this purpose with the help of softwares like MySQL, MongoDB, and Streamlit.
This project is designed using the python programming language.

# Technologies utilized:

1. Python: Python is a high-level, interpreted, interactive and object-oriented scripting language. 
			Python is designed to be highly readable. It uses English keywords frequently where as other languages use punctuation, and it 
			has fewer syntactical constructions than other languages.
2. Youtube API: YouTube API is an application programming interface that allows developers to incorporate functions normally executed on 
				the YouTube website into their own website or application.
3. MongoDB: MongoDB is an open-source document-oriented NoSQL database management program that uses collections and documents instead of 
			tables and rows to store and retrieve data.
4. SQL[MySQL]:SQL (Structured Query Language) is a programming language used to communicate with and manipulate databases.
				It is the standard language for relational database management systems and is used to perform tasks such as updating data 
				on a database or retrieving data from a database. MySQL is an open-source relational database management system (RDBMS) 
				that enables users to store, manage, and retrieve structured data efficiently. It is based on SQL.
5. Pandas: pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
			built on top of the Python programming language.
6.Streamlit: Streamlit is an open-source app framework for Machine Learning and Data Science teams. It can be used to make web applications 
			without prior web page development knowledge.

# Modules Imported in the project:

1. streamlit 
2. googleapiclient.discovery
3. pymongo
4. pandas
5. mysql.connector
6. re

# Project Overview:

The complete project can be modularized into 4 Major components:

1. Data Scrapping from Youtube using Youtube API.
	Data from youtube is sourced using the youtube API and is formatted to contain only the details we require for this project,
	in this case, 3 seperate embedded dictionaries namely the channel, comment and video dictionaries
2. Deploying retrieved data into MongoDB using python language.
	Using MongoDB, the previously recieved data is then altered to provide data sets that are interactable and can be used for further analysis.
	This data is converted into 3 documents of a single collection under a user created database in mongodb.
3. Migrating Data from MongoDB data lake into MySQL for visualization, querying and analysis.
	The data present in MongoDB data lake, despite being unrelated, is converted to suit the format of MySQL with the help of the pandas dataframe method.
	This newly formatted data is then migrated onto the respective SQL database under which individual tables for channels, videos and comments are created 
	and its values inserted.
4. Displaying formatted data and answering catered queries with the help of streamlit.
	With the help of SQL querying, dataframe creation and python programming, the Data is successfully analysed in MySQL and displayed
	onto  the streamlit web application as per the curated queries present in the problem statement.
	
# Setting Up and Installation:
	
1. Python: Install the compatible version of python on your device.
2. Libraries: Certain libraries as previously mentioned are necessary for the functioning of this project, and hence need to be installed onto your machine.
			 Required Libraries are mentioned previous as modules.
3. Google API: In order to obtain a google creator api, a Google API project has to be set up and the API credentials have to be obtained for accessing
			the youtube API
4. Database Configuration: The afformentioned Databases, both in MongoDB and MySQL have to be created in order to work in these technologies.
5. Program Configuration: The python code that is to be utilized has to have the configuration files and environment variables defined along with the 
						API credentials and the database details for uninterrupted functioning of the project.
6. Application: The Streamlit application can now be executed from your IDE terminal for hands on use of the project.

# Client User Guide:
In order to use the web application, follow the steps given below:

1. Enter the desired youtube Channel ID to retrieve its data and click on "Collect and store the data"
2. After all the data of the desired channels have been collected and stored one-by-one, click on "Migrate data to sql"
3. On the completion of Migration, the Data visualization container will display the table respective to the option chosen.
4. Scroll down further to view the results of the curated queries for the collected data depicted in an easy to understand and clean format.

# Features:
These are the featured offered in this YouTube Data Harvesting and Warehousing application:

1. Channel, video and comment data retrieval using youtube API
2. Data storage in MongoDB Data Lake
3. Migration of data from MongoDB to MySQL with skillful formatting
4. Data Retrieval and Searching operation possible in SQL Database
5. Data Analysis and Visualization through Streamlit.
6. Ability to handle multiple sets of data from different youtube channels.

# Points of Improvement:
This Application, while being highly efficient and foolproof has scope of development in some aspects, namely:

1. Security Authentication: User authentication implementation for secure access of application
2. Automated Data Harvesting: Pre-scheduling Data harvesting for designated youtube channels regularly.
3. Better Searching and Filtering options: Improving search functionality for advanced searching criteria and filtering options
4. Additional sources and analysis: Expand the scope of the project by inculcating similar processes for other social media platforms,
									along with applying advanced analytical methods and tools.
5. Exporting results: Analysed data can be further exported into visualization tools like PowerBI for in-depth visualization and analysis.


# Conclusion:

The web application of YouTube Data Harvesting and Warehousing project gives light to a powerful and capable tool for data retrieving 
and analysis process. Alongside the help of Software like SQL, MongoDB and Streamlit, it is possible to create a user friendly and creative
environment for analysis and visualization. This project boasts flexibility, scalability and visualization capabilities, allowing ordinary
users to be geared with fully functional data analysis tools.

References

- Streamlit Documentation: https://docs.streamlit.io/
- YouTube API Documentation: https://developers.google.com/youtube
- MongoDB Documentation: https://docs.mongodb.com/
- Python Documentation: https://docs.python.org/
- MySQL Documentation: https://dev.mysql.com/doc/
