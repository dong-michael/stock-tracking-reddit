from psaw import PushshiftAPI
from chart import *
import config
import datetime
import psycopg2
import psycopg2.extras

#Some code taken and modified from tutorial: https://github.com/hackingthemarkets 

class search_subreddit:

    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor2 = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    stocks = {}

    def __init__(self):

        rows = self.get_stock_tickers_from_table()
        for row in rows:
            self.stocks['$' + row['symbol']] = row['id']


    #query data from table and return stock tickers
    def get_stock_tickers_from_table(self):
        self.cursor.execute("""
            SELECT * FROM stock
                                """)
        return self.cursor.fetchall()

    #query data from table and return number of mentions, stock symbol, and stock id
    def get_mention_from_table(self):
        self.cursor2.execute("""
            SELECT count(*) as num_mention, stock_id, symbol
            FROM mention JOIN stock ON stock.id = mention.stock_id
            GROUP BY stock_id, symbol
            ORDER BY num_mention DESC;
                                    """)
        return self.cursor2.fetchall()

    #clears mention table, (data gathered so far)
    def clear_mention_table(self):
        self.cursor2.execute(""" DELETE FROM mention
                                                    """)

    #extracts data from subreddit for analysis
    def extract_data_from_subreddit(self):
        api = PushshiftAPI()

        start_time= int(datetime.datetime(2021, 5, 5).timestamp())

        submissions = api.search_submissions(after=start_time,
                                            subreddit='wallstreetbets',
                                            filter=['url','author', 'title', 'subreddit']
                                                    )

        for submission in submissions:

            words = submission.title.split()
            cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))

            if len(cashtags) > 0:
                print(cashtags)
                print(submission.title)

                for cashtag in cashtags:

                    submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()

                    try:
                        self.cursor.execute("""
                            INSERT INTO mention (dt, stock_id, message, source, url)
                            VALUES (%s, %s, %s, 'wallstreetbets', %s)
                        """, (submitted_time, self.stocks[cashtag], submission.title, submission.url))
                        self.connection.commit()

                    except Exception as e:
                        print(e)
                        self.connection.rollback()

    
                                    