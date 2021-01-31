# Lineup

## Streamlined Discord event queue management

Manage your events with lineup. Create events and hold more organized Q&A sessions among a group!

### **Administrator commands**

**These commands are only available to those in a server with the role "Host". Please ensure that all who'll need use of these functions have the "Host" role.**

**.begin** (*String [event_name]*)
Starts an event with name [*event_name*]

**.end** (*int [event_id], string [leave_message]*)
Ends event with id [*event_id*] and displays optional [*leave_message*]

**.clear** (*int [event_id]*)
Clears all questions in event with id [*event_id*]

**.resolve** (*int [question_index]*)
Resolves and removes question from queue with given index [*question_index*]

**.move** (*int [position_1] int [position_2]*)
Moves question in queue at [*position_1*] to [*position_2*]

**.ready** (*int [event_id]*)
Notifies the first user the in the queue of event at index [*event_index*] that the host is ready

 

### Universal commands

**These commands are available to anyone in the server**

**.help**
Displays all commands 

**.list_events**
Displays a list of all current events taking place on the server

**.queue** (*int [event_id]*)
Displays the queue of a given event with id [*event_id*]

**.enter** (*int [event_id]* *String [topic]*)
Enters given event with id [*event_id*] with optional topic [*topic*]

**.leave** (*int [event_id]* int[*question_index*])
Removes a topic asked by the user at index [*question_index*] of a given event with id [*event_id*] 

**.rename** (*int [event_id]* *int[question_index]* *String[renamed_question]*)
Renames a user's question at [*question_index*] in the given event with id [*event_id*] with [*renamed_string*]
