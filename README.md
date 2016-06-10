# Commands (prefix: ~)
* `courses`: Lists the available courses
* `load course`: Loads the given course to be run
* `setprofs <prof 1> <prof 2>`: Sets the professors for the course
    * Takes a list of users separated by spaces
* `profs`: Lists and pings the current professors
* `start`: Starts a class
* `pause`: Pauses the current class
* `resume`: Resumes the current class following a *pause* from where was left off
* `stop`: Stops the current class (starting again will start from beginning)

# General Formatting Guidelines
* Bold indicates a title of a SUBJECT or TOPIC
    * Subject: CHANNELS AND QUERIES
    * Topic: Joining a Channel
* Red and bold are IRC commands to be entered by users
    * `/ns group`
* Underline is a variable that must be set by the user in an IRC command
    * [brackets] are optional variables (the brackets should not be underlined
    * `/join #channel [key]`
    * Do not format tags <tagname variable=”value”>
* Green are messages sent by the bot
    * "The class has been started."
* Red text are error messages 
    * "A course must be loaded before you can start a class."

# Formatting with the Bot (may be nested, not listed are automatic)

## IRC Command: <cmd>Command here</cmd>
* Required variable: <req>Variable here</req>
* Optional variable: <opt>Variable here</opt>
* Example: <cmd>/join <req>#channel</req> <opt>key</opt></cmd>
   * `/join #channel [key]`
 
## Channel Notice: <notice>Notice here</notice>

## Professors
* @profs will be replaced by the list of profs and ping them
* Can be done in a notice or objective

## Bot instructions: <bot>ping OR pause</bot>
* ping will ping all professors set at the start of the lesson in the channel
* pause stops the class until resumed by a professor

## IRC Command: <irc>Command here</irc>
* Must be in raw IRC format, “/” format will not work
    * `MODE #classchan +m`
* Any command the bot has permission to run will work!
* Use #classchan for current channel
    * Do not replace #classchan with the actual name of the class channel - it will be done automatically by the bot when the class is run

# General File and Course Format

Files are in the XML format with the .sic extension (Snoonet IRC Course)


