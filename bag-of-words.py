import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sklearn as sk
import re




BOW_df = pd.DataFrame(columns=['1','0','-1'])
df = pd.read_csv("Reviews.csv")

BOW_df.loc['first'] = [0,0,0]
BOW_df.loc['first']['1'] +=1

words_set = {'.'}



print(BOW_df.head())
def prepare_data(df):
    # This function should generate the train and test dataframe
    df = df.drop(['Id', 'ProductId', 'UserId', 'ProfileName', 'HelpfulnessNumerator', 'HelpfulnessDenominator','Time', 'Summary'] , axis = 1)
    df['Score'] = df['Score'].map( { 1 : -1, 2 : -1, 3 : 0 , 4 : 1, 5 : 1} )
    print(df.head())
    return df

df = prepare_data(df).sample(frac = 1, random_state = 21)

train = df.iloc[:500,:]
test  = df.iloc[20000:,:]



def Tokenizer(text):
#Returns a list of words in the text
    #remove new lines
    text.rstrip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower()
    words = text.split(" ")
    return words
    
for i, review in train.iterrows():
    text  = review['Text']
    score = review['Score']
    tokenized_text = Tokenizer(text)
    for word in tokenized_text:
        if word not in words_set:
            words_set.add(word)
            BOW_df.loc[word] = [0,0,0]
            BOW_df.loc[word][score] += 1
        else:
            BOW_df.loc[word][score] += 1    

# BOW_df.sort('1',ascending=false)
# positive_words = BOW_df.head(50)

# BOW_df.sort('0',ascending=false)
# neutral_words = BOW_df.head(50)

# BOW_df.sort('-1',ascending=false)
# negative_words = BOW_df.head(50)

print(BOW_df)

    
