import win32evtlog as evt


server_name = "localhost"
source_name = "System"

# Ask windows for a connection to event log
hand = evt.OpenEventLog(server_name, source_name)

# Read the event from newest to oldest in sequential order
flags = evt.EVENTLOG_BACKWARDS_READ | \
        evt.EVENTLOG_SEQUENTIAL_READ

# Read the events
events = evt.ReadEventLog(hand, flags, 0)


print(f"{'Event ID':<10} {'Source Name':<30} {'Event Type':<12} {'Time Generated':<25} {'Computer Name':<20}")

for event in events:
    print(
        f"{event.EventID:<10} "
        f"{event.SourceName:<30} "
        f"{event.EventType:<12} "
        f"{str(event.TimeGenerated):<25} "
        f"{event.ComputerName:<20}"
    )
