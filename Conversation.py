__author__ = 'karthikwitty'

import pandas as pd
import os
import operator
import string
from natsort import natsorted
from ast import literal_eval

from collections import Counter,OrderedDict
import itertools


def word_count():
    try:
        dialogues=dict()

        file_location="/Users/karthikwitty/Desktop/Desktop/Interview/cornell movie-dialogs corpus"
        os.chdir(file_location)
        filename='movie_lines.txt'
        filename2='movie_conversations.txt'

        #Getting the data from file
        in_file=pd.read_csv(filename,sep='\+{3}\$\+{3}',engine='python',header=None)
        in1_file=pd.read_csv(filename2,sep='\+{3}\$\+{3}',engine='python',header=None)


        #Perform natural sorting to reduce time
        reply_id=[literal_eval(na.strip()) for na in in1_file[3]]
        reply_id=natsorted(reply_id)
        
        #Storing the LineId and Message Content inorder for fast accessing
        for line,content in zip(in_file[0],in_file[4]):
            line=line.strip()
            content=str(content).lower().strip()
            content=content.translate(str.maketrans('','',string.punctuation))
            dialogues[line]=content

        dialog_dict=Counter(dialogues.values())

        
        #Getting the most Frequent dialog up to 25
        dialog_dict=sorted(dialog_dict.items(),key=operator.itemgetter(1),reverse=True)
        whole_dialogs=dialog_dict[:25]

        dial_dict={}

        #Iterating the Top 25 Conversations to find the Most frequent Reply
        for item in whole_dialogs:
            q1,count=item
            values=natsorted([lineid for lineid,content in dialogues.items() if content==q1])
            dial_dict[q1]=values
            complete_list=list()
            count=0
            for val in values:
                count+=1
                for rep_id in reply_id:
                    if val in rep_id:

                        #Logic to find the reply to the current message
                        current_conv_id=rep_id.index(val)+1

                        #Logic to find the Dialog is end of the Converstation or not
                        if current_conv_id < len(rep_id):
                            complete_list.append(rep_id[current_conv_id])
                            break

                        #Go to the next value since dialog is an end of the conversation
                        else:
                            break
            # Creating the Dataframe for easy indexing with the LineIDs
            new_df=pd.DataFrame({'keys': list(dialogues.keys()),'replys': list(dialogues.values())})
            messages=list(new_df['replys'][new_df['keys'].isin(complete_list)])
            replys=Counter(messages)

            # Getting the frequent reply and sort it
            freq=sorted(replys.items(),key=operator.itemgetter(1),reverse=True)
            print(q1,freq[0])


    except Exception as e:
        print(e)

if __name__ == '__main__':
    word_count()