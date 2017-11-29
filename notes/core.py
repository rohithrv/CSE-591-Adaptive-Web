import sqlite3
import nltk
import nltk
import string
import collections
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from bs4 import BeautifulSoup
import html
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize

class CoreOps:
    def __init__(self):
        # init create a connection and a cursor object
        self.conn = sqlite3.connect("db.sqlite3")
        self.c = self.conn.cursor()

    def getTopFromCounter(self, li, top_no):
        result_list = []
        temp = Counter(li).most_common(top_no)
        for t in temp:
            result_list.append(t[0])
        return result_list


    def getTgasForAllNotes(self):
        res = self.c.execute("select noteid,content,title from notes_notes ").fetchall()
        for r in res:
            print(r)
            note_tags = self.getTagsFromString(r[1])
            tag_list = []
            print(str(r[0]) + " , '" + note_tags + "','"+r[2])
            title = r[2]
            title = title.replace("'","")
            title = "~".join(title.split())
            self.c.execute("insert or replace into notes_note_meta (note_id, tags, title) VALUES (" +str(r[0]) + " , '" + note_tags + "','"+title+"' )")
            self.conn.commit()
        #     call this only once


    def cleanup(self):
        # use this at the end of the program to close the connection to the database
        self.c.close()

    def getCBforNote(self, note_id):
        final_title_tags = []
        final_tags = []
        print("get notes with same tags as this one")
        title_tags, note_tags = self.getTagsForNote(note_id)
        res = self.c.execute("select * from notes_note_meta where note_id != "+str(note_id))
        for r in res:
            noteid = r[0]
            t_tags = r[2].split("~")
            tags = r[1].split("~")
            for t in title_tags:
                if t in t_tags:
                    final_title_tags.append(noteid)

            for t in note_tags:
                if t in tags:
                    final_tags.append(noteid)
        final_tags = self.getTopFromCounter(final_tags, 10)
        final_title_tags = self.getTopFromCounter(final_title_tags, 10)
        print(final_title_tags)
        print(list(set(final_tags)-set(final_title_tags)))
        return final_title_tags, list(set(final_tags)-set(final_title_tags))

    def getCBforUser(self, user_id):
        final_tags = []
        print("user recomendations coming right up")
        user_tags = self.getTagsForUser(user_id)
        res = self.c.execute("select * from notes_note_meta")
        for r in res:
            # print(r)
            noteid = r[0]
            if type(r[2]) != int:
                t_tags = r[2].split("~")
            tags = r[1].split("~")
            for t in user_tags:
                if t in tags:
                    final_tags.append(noteid)
                if type(r[2]) != int:
                    if t in t_tags:
                        final_tags.append(noteid)
                        final_tags.append(noteid)

        final_tags = self.getTopFromCounter(final_tags, 10)
        return final_tags




    def getCFforUser(self, user_id):
        print("get similar user and get thier public notes")

    def userOpenedNote(self,user_id, note_id):
        # call this function when the user opens a note , pass the user_id and note_id as argument
        tags = ""
        res = self.c.execute("select * from notes_user_meta WHERE user_id ="+str(user_id))
        if (len(res.fetchall())==0):
            print("this row doest exist yet let create it")
            self.c.execute("insert into notes_user_meta VALUES ("+str(user_id)+", '', '')")
            self.conn.commit()
        res = self.c.execute("select * from notes_user_meta WHERE user_id =" + str(user_id))
        # print(res)
        for r in res:
            print(r)
            tags = r[1]
            t_tags = r[2]

        title_tags, note_tags = self.getTagsForNote(note_id)
        # print(note_tags)
        tags = ','.join(note_tags)+"," + tags
        t_tags = ','.join(title_tags)+", " + t_tags

        tags = tags.replace(",","~")
        t_tags = t_tags.replace(",","~")
        print(tags)
        print(t_tags)
        self.c.execute("insert or replace into notes_user_meta (user_id, tags, titles) VALUES ('"+ str(user_id) + "', '" + tags + "','"+t_tags+"')")
        self.conn.commit()
    #     commits the values to the database, these tags can be used by calling getUserTags functiom



    def saveTheNote(self, note_id, note_text):
        # call this function when the note is created or existing note is edited
        print("getting the tags from the updated user note")
        note_tags = self.getTagsFromString(note_text)
        tag_list = []
        for tag in note_tags:
            # print(tag[1])
            tag_list.append(tag[1])
        temp_str = "', '".join(tag_list)
        if len(tag_list)<5:
            temp_str = temp_str ="'"+temp_str +"'"+(" ,'NA' "*(5 -len(tag_list)))
        else:
            temp_str ="'"+temp_str +"'"
        # print(str(note_id)+" , "+temp_str)
        self.c.execute("insert or replace into notes_note_meta (note_id, tag1, tag2, tag3, tag4, tag5) VALUES ("+str(note_id)+" , "+temp_str+" )")
        self.conn.commit()
    #     no return, just commits to the database


    def getTagsForNote(self, note_id):
        # call this funciton with note_id to get the tags associated with the note
        res = self.c.execute("select * from notes_note_meta where note_id = "+str(note_id))
        for r in res:
            print(r[1].split("~"))
            return list(r[2].split("~")), list(r[1].split("~"))
    #     returns a python list of all the tags associated with a note


    def getTagsForUser(self, user_id):
        # call this fucntion to get the tags that are associateaad to each user based on the notes he viewed
        print("getting tags for user")
        res = self.c.execute("select * from notes_user_meta WHERE user_id = "+str(user_id))
        tags=""
        for r in res:
            tags = r[1]+"~"+r[2]
        tags = tags.split("~")
        # print(tags)
        test = collections.Counter(tags).most_common(10)
        # print(test)
        top_tags = []
        for t in test:
            top_tags.append(t[0])
        print(top_tags)
        return top_tags
    # return the top 10 tags for the user, call this fucntion dynamically when you need to get the tags for an user

    def getTagsFromString(self, st):
        # this fucntion get tags from a particular post by comparing with all the other notes in the database
        # this will take time, avoid calling this fucntion unless a new note is created or updated
        token_list = []
        stop_words = set(stopwords.words('english'))
        # stop_words.clear()
        stop_words.update(
            ["-", '.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', 'geturl', 'logs', 'mouseover',
             'home', 'javatagged',
             '~', '&', '>', '<', "/", "''", 'name', 'data', "..."])
        soup = BeautifulSoup(st, "lxml")
        st = " ".join(soup.findAll(text=True))
        words = word_tokenize(st)
        for word in words:
            if word not in stop_words and (not word.isdigit()) and len(word) >2:
                token_list.append(word.lower())
        key_words = Counter(token_list).most_common(5)
        return_list = []
        for k in key_words:

            return_list.append(k[0])

        print(return_list)
        fin = '~'.join(return_list)
        fin = fin.replace("'","")
        print(fin)
        return fin

obj = CoreOps()
# obj.getCBforNote(419)
print(obj.getCBforUser(12))
# obj.getTagsForNote(419)
# obj.userOpenedNote(12, 419)
# obj.getTagsForUser(12)
# obj.getTgasForAllNotes()
# print(st)

        # final_result = []
        # def tokenize(text):
        #     tokens = nltk.word_tokenize(text)
        #     stems = []
        #     for item in tokens:
        #         stems.append(PorterStemmer().stem(item))
        #     return stems

        # all_notes = self.c.execute("select * from notes_notes")
        # for note in all_notes:
        #     # print(note[7])
        #     text = note[2]+" "+note[3]
        #     soup = BeautifulSoup(text, "lxml")
        #     text = ' '.join(soup.findAll(text=True))
        #     # print(all_text)

            # token_dict[note[7]] = text.lower()

        # tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words= stop_words)
        # tfidf = TfidfVectorizer(tokenizer=tokenize)
        # tfs = tfidf.fit_transform(token_dict.values())

        # response = tfidf.transform([st])

        # feature_names = tfidf.get_feature_names()
        # for col in response.nonzero()[1]:
        #     res = [response[0, col], feature_names[col]]
            # return res
            # print(res)
            # final_result.append(res)

        # print(sorted(final_result, key=lambda x:x[0])[::-1][:5])
        # test = final_result[:5]
        # test = sorted(final_result, key=lambda x:x[0])[::-1][:5]
        # for t in range(0,len(test)):
        #     test[t][1] = test[t][1].replace("'", "")
        #     test[t][1] = test[t][1].replace(",", "")

            # print(test[t][1])
        # return test
#     returns a python list with tf-idf values in asceding order



