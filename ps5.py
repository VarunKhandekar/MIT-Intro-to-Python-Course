# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Varun Khandekar
# Collaborators: N/A
# Time: N/A

import os
os.chdir('C:\Python Code\MIT - Intro to Python\PSets\ps5')
    
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        guid (Globally Unique Identifier - GUID): a string
        title: a string
        description: a string
        link (a link to more content): a string
        pubdate: a datetime object
        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate
    
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        '''
        phrase: a string; no punctuation and each word is separated by one space, case insensitive
        '''
        self.phrase = phrase
    
    def is_phrase_in(self, text):
        check = False
        
        #make all text inputs as lowercase
        temp_text = text.lower()
        lowercase_phrase = self.phrase.lower()
        
        #swap all punctuation with spaces
        punctuation = string.punctuation
        for punc in punctuation:
            temp_text = temp_text.replace(punc, ' ')
        
        #remove start and end spaces to avoid our phrase not being picked up if it matches the beginning/end set of words in the text
        #split the text
        temp_text = temp_text.strip()
        temp_text = temp_text.split()
        
        #split the phrase to get its length
        lowercase_phrase_split = lowercase_phrase.split()
        phrase_length = len(lowercase_phrase_split)
        # if our phrase is longer than the text in question, return false
        if phrase_length > len(temp_text):
            return check
                
        #loop through this split list and join the first x words - x being phrase_length
        #do for len - phrase length + 1 so we don't try to join past the end word
        #CHECK LOGIC HERE..
        space = ' '
        for position in range(len(temp_text)- phrase_length + 1):
            testword_split = []
            
            #append to testword_split the number of words as there are in the phrase
            for count in range(phrase_length):
                testword_split.append(temp_text[position + count])
            testword = space.join(testword_split)
            
            if lowercase_phrase == testword:
                return not check
        
        #if we get to here, our phrase hasn't been found   
        return check
        
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
        phrase: a string; no punctuation and each word is separated by one space, case insensitive
        '''
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        alert = self.is_phrase_in(story.get_title())
        return alert
    
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
        phrase: a string; no punctuation and each word is separated by one space, case insensitive
        '''
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        alert = self.is_phrase_in(story.get_description())
        return alert
    
    
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, time):
        '''
        time: a string of the format 'DD MMM YYYY HH:MM:SS' e.g. '3 Oct 2016 17:00:10'. In EST.
        '''
        
        time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        self.time = time.replace(tzinfo=pytz.timezone("EST"))
        
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self,time):
        TimeTrigger.__init__(self, time)
    
    def evaluate(self, story):
        alert = False
        publishing_date = story.get_pubdate()
        publishing_date = publishing_date.replace(tzinfo=pytz.timezone("EST"))
        if publishing_date < self.time:
            return not alert
        else:
            return alert


class AfterTrigger(TimeTrigger):
    def __init__(self,time):
        TimeTrigger.__init__(self, time)
    
    def evaluate(self, story):
        alert = False
        publishing_date = story.get_pubdate()
        publishing_date = publishing_date.replace(tzinfo=pytz.timezone("EST"))
        if publishing_date > self.time:
            return not alert
        else:
            return alert
        

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        '''
        trigger: a trigger object
        
        '''
        self.trigger = trigger
    
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        '''
        trigger1: a trigger object
        trigger2: a trigger object
        
        '''
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
        
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        '''
        trigger: a trigger object
        
        '''
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    
    trigger_stories = []
    
    for story in stories:
        #add all those stories for which a trigger in triggerlist fires
        for trigger in triggerlist:
            if trigger.evaluate(story):
                trigger_stories.append(story)
                
    return trigger_stories


#======================
# User-Specified Triggers
#======================
# Problem 11

def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!
    
    #an empty list for all the triggers that get defined in the txt file
    defined_triggers = []
    
    #an empty list for all the triggers to actually be used
    trigger_list = []
    
    #a mapping dictionary for text combinations to the relevant trigger objects
    mapping_dict = {'TITLE': TitleTrigger,
                    'DESCRIPTION': DescriptionTrigger,
                    'BEFORE': BeforeTrigger,
                    'AFTER': AfterTrigger,
                    'NOT': NotTrigger,
                    'AND': AndTrigger,
                    'OR': OrTrigger}
    
    for line in lines:
        #split up each string i.e. line into its constituent comma separated parts
        clean_line = line.split(',')
        
        #ensure we only pick up lines here triggers are being defined
        if clean_line[0] != 'ADD':
            #a check for how many arguments are required for the class; this could be improved though..
            if len(clean_line) == 4:
                clean_line[0] = mapping_dict[clean_line[1]](clean_line[2], clean_line[3])
            else:
                clean_line[0] = mapping_dict[clean_line[1]](clean_line[2])
           
            #add this newly defined variable
            defined_triggers.append(clean_line[0])
        else:
            clean_line = clean_line[1:]
            for trig in clean_line:
                trigger_list.append(trig)
    
    return trigger_list    
    
    
    
SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Covid")
        t2 = DescriptionTrigger("Covid")
        t3 = DescriptionTrigger("covid")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

