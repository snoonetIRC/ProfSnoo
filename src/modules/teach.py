import os
import lxml
import time
import hook
from lxml import etree
from time import sleep

datadir = bot.config.get('course_dir')

tags  = [
    'subject',
    'topic',
    'objective',
    'notice',
    'irc',
    'cmd',
    'bot',
    'req',
    'opt'
]
        
def format_irc(output):
    
    out = output
    
    formats = {
        '<b>' : '\x02',
        '</b>' : '\x02',
        '<cmd>' : '\x02\x034',
        '</cmd>' : '\x03\x02',
        '<u>' : '\x1F',
        '</u>' : '\x1F',
        '<req>' : '\x1F',
        '</req>' : '\x1F',
        '<opt>' : '[\x1F',
        '</opt>' : '\x1F]'
    }
    
    for form in formats:
        out = out.replace(form, formats.get(form))
        
    for tag in tags:
        out = out.replace('<' + tag + '>', ''); out = out.replace('</' + tag + '>', '')
        
    return out

class Course():
    
    profs = list()
    file = None
    is_teaching = False
    is_paused = True
    was_stopped_early = False
    
    def start(self, chan):
        if not Course.file:
            bot.say(chan, '\x034You must load a lesson before you can begin.\x03')
        else:
            if not Course.is_teaching:
                if not Course.profs:
                    bot.say(chan, "\x034No professors are set for this class.\x034")
                else:
                    Course.is_teaching = True; Course.is_paused = False; Course.was_stopped_early = False
                    out = 'Class starting with professors:'
                    for prof in Course.profs:
                        out += ' ' + prof
                    bot.say(chan, out + '\x03', notice=True)
                    self.teach(chan)
            else:
                bot.say(chan, '\x034Class is already in session.')
        
    def pause(self, chan):
        if Course.is_teaching:
            if not Course.is_paused:
                Course.is_paused = True
                bot.say(chan, '\x033Class paused.\x03')
            else:
                bot.say(chan, '\x034Class already paused.\x03')
        else:
            bot.say(chan, '\x034No class in session.\x03')
        
    def resume(self, chan):
        if Course.is_teaching:
            if Course.is_paused:
                bot.say(chan, '\x033Class resumed.\x03')
                Course.is_paused = False
            else:
                bot.say(chan, '\x034Class arleady running.\x03')
        else:
            bot.say(chan, '\x034No class in session.\x03')
                
    def stop(self, chan):
        if Course.is_teaching:
            Course.is_teaching = False
            Course.was_stopped_early = True
            bot.say(chan, '\x033Class ended.\x03')
        else:
            bot.say(chan, '\x034No class in session.\x03')
        
    def teach(self, chan):
        tree = etree.parse(Course.file)
        i = 0; j = 0; k = 0
        for item in tree.iter(tags):
            if not Course.is_teaching:
                break
            
            if Course.is_paused:
                while Course.is_paused:
                    sleep(0.1)
                    
            if item.tag == 'subject':
                i += 1; j = 0
                bot.say(chan, '\x02SECTION ' + str(i) + ':\x02 ' + item.get('name').upper() + ' (' + str(i) + ')'); sleep(5)
            elif item.tag == 'topic':
                j += 1; k = 0
                bot.say(chan, '\x02' + item.get('name').title() + '\x02' + ' (' + str(i) + '.' + str(j) + ')'); sleep(3)
            elif item.tag == 'objective':
                k += 1
                out = (etree.tostring(item).strip()).decode(); out = format_irc(out)
                out = out.replace('@profs', ', '.join(Course.profs))
                bot.say(chan, out + ' (' + str(i) + '.' + str(j) + '.' + str(k) + ')'); sleep((len(out.split()) / 250) * 60)
            elif item.tag == 'irc':
                raw = format_irc((etree.tostring(item).strip()).decode())
                raw = raw.replace('#classchan', chan)
                bot.do(raw)
            elif item.tag == 'notice':
                out = (etree.tostring(item).strip()).decode(); out = format_irc(out)
                out = out.replace('@profs', ', '.join(Course.profs))
                bot.say(chan, out, notice=True)
            elif item.tag == 'bot':
                cmd = format_irc((etree.tostring(item).strip()).decode())
                if cmd == 'pause':
                    self.pause(chan)
                elif cmd == 'ping':
                    self.show_profs(chan)
                    
        if not Course.was_stopped_early:
            bot.say(chan, '\x033Course complete.\x03')
            Course.is_teaching = False
    
    def load(self, chan, file):
        if not Course.is_teaching:
            try:
                file[0]
            except IndexError:
                bot.say(chan, '\x034You must specify a file name.\x03')
            else:
                try:
                    open(datadir + file[0] + '.sic', 'r')
                except IOError:
                    bot.say(chan, '\x034Invalid course name. Use ~courses for a list of available courses.\x03')
                else:
                    Course.file = datadir + file[0] + '.sic'
                    bot.say(chan, '\x033Course \x02' + file[0] + '\x02 successfully loaded.\x03')
        else:
            bot.say(chan, '\x034There is already a class in session.\x03')
    
    def show_profs(self, chan):
        out = ''
        for prof in Course.profs:
            out += prof + ' '
        bot.say(chan, out)

course = Course()
 
@hook.command('start', flags='@')  
def start(prefix, chan, params):
    course.start(chan)
    
@hook.command('pause', flags='@')  
def pause(prefix, chan, params):
    course.pause(chan)
    
@hook.command('resume', flags='@')  
def resume(prefix, chan, params):
    course.resume(chan)
 
@hook.command('stop', flags='@')  
def stop(prefix, chan, params):
    course.stop(chan)
         
@hook.command('load', flags='@')
def load(prefix, chan, params):
    course.load(chan, params)
 
@hook.command('courses', flags='@')
def courses(prefix, chan, params):
    out = '\x033Course List:\x03 '
    for course in os.listdir(datadir):
        out += course.replace('.sic', '') + ' '
    bot.say(chan, out)
 
@hook.command('profs', flags='@')
def profs(prefix, chan, params):
    course.show_profs(chan)
            
@hook.command('setprofs', flags='@')
def set_profs(prefix, chan, params):
    Course.profs = params
    bot.say(chan, '\x033Professors successfully set.\x03')
    
@hook.command('test', flags='@')
def test(prefix, chan, params):
    Course.profs = ['Apple', 'Orange', 'Banana']
    course.load(chan, ['test'])
    course.start(chan)