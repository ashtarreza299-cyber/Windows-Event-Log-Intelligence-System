import win32evtlog as evt
import win32evtlogutil as event_util
import win32security as security

def collect_events(server_name = 'localhost', source_name = 'System', max = 100):
    """Collect Windows Event Log entries and return them as a list of dicts."""


    # Ask windows for a connection to event log
    hand = evt.OpenEventLog(server_name, source_name)

    # Read the event from newest to oldest in sequential order
    flags = evt.EVENTLOG_BACKWARDS_READ | \
            evt.EVENTLOG_SEQUENTIAL_READ

    # Read the events
    events = evt.ReadEventLog(hand, flags, 0)

    # list of dict
    collected = []
    count = 0

    for event in events:

        if count >= max:
            break

        # Try to get the system UserName

        if event.Sid:

            name, domain, _ = security.LookupAccountSid(None, event.Sid)
            user_name = F"{domain}\\{name}"
        else:
            user_name = "N/A"

        collected.append({
                    "EventID": event.EventID,
                    "SourceName": event.SourceName,
                    "EventType": event.EventType,
                    "TimeGenerated": event.TimeGenerated,
                    "ComputerName": event.ComputerName,
                    "UserName": user_name,
                    "Message": event_util.SafeFormatMessage(event, source_name)
                })
        

        count+=1

    evt.CloseEventLog(hand)
    return collected

if __name__ == "__main__":

    events = collect_events()

    for event in events:

        print(event)