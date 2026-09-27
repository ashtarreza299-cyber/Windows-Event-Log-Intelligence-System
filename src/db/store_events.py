
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "collector"))

from event_collector import collect_events
from db_connection import connect_db

def store_events():

    # collect events
    events = collect_events()

    print(F"Collected {len(events)} events")

    # database conntection
    connection = connect_db()
    cursor = connection.cursor()

    sql = """
        INSERT INTO 
            EventLog(EventID, SourceName, EventType, TimeGenerated, ComputerName, UserName, Message)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            
        """

    for event in events:

        # Try to insert data
        try: 
            cursor.execute(
                    sql, 
                    event["EventID"], 
                    event["SourceName"], 
                    event["EventType"],
                    event["TimeGenerated"],
                    event["ComputerName"],
                    event["UserName"],
                    event["Message"]
                    
                    )
        # Any exception ?
        except: 
            print(F"Error inserting event")

    # Successfully inserted
    connection.commit();
    print("Successfully inserted data")

    # Release resources
    cursor.close()
    connection.close()

if __name__ == "__main__":

    store_events()