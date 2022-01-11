# lineup
![Lineup graphic](https://github.com/AdiChops/lineup/blob/main/lineup_graphic.png?raw=true)
## Streamlined Discord event queue management

Manage your events with lineup. Create events and hold more organized Q&A sessions among a group! Our intuitive discord bot allows for the seemless creation of Q&A sessions facilitating for more efficient responses and management from Profs, TA's and event hosters alike!

We felt as if there is a great need, especially in times of online learning, for improved online tools regarding education and communication. Office hours, tutorials and general question sessions just aren't the same online and tend to become pretty chaotic. We hope to change that. Our bot can be integrated within multiple servers to serve multiple different communities, helping all of them manage their question sessions. This in turn allows for better engagement among attendee and host - a win win for all!

Some problems occurred. How can we have a bot store separate information across a multitude of servers all utilizing it at once? How would we use the discord.py API to create what we needed? What other object structures would need to be created for everything to work exactly the way we wanted it. We were able to devise away that would allow for the bot to keep track of each individual server's needs at once. Documentation and YouTube are everyone's best friend when it comes to learning new technologies, and we decided that storing questions and events as separate objects would be enough for what we needed!


Where do we want this to go? Everywhere. Classrooms, discussion boards, meetups, conferences, events. The applications, while simple, can be used endlessly across several different environments.

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

### Technologies
Uses the `discord.py` library and is deployed on Heroku.
