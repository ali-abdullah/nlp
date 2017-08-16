import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sklearn as sk
import re




BOW_df = pd.DataFrame(columns=['1','2','3','4','5'])
df = pd.read_csv("Reviews.csv")

words_set = {'.'}


#print(BOW_df.head())

def prepare_data(df):
    # This function should generate the train and test dataframe
    df = df.drop(['Id', 'ProductId', 'UserId', 'ProfileName', 'HelpfulnessNumerator', 'HelpfulnessDenominator','Time', 'Summary'] , axis = 1)
    #df['Score'] = df['Score'].map( { 1 : -1, 2 : -1, 3 : 0 , 4 : 1, 5 : 1} )
    print(df.head())
    return df

df = prepare_data(df).sample(frac = 1, random_state = 21)


train = df.iloc[:10000,:]
test  = df.iloc[20000:20020,:]



def Tokenizer(text):
#Returns a list of words in the text
    #remove new lines
    text.rstrip()
    # text = text.replace("<br", "")
    # text = text.replace("<Br", "")
    # text = text.replace("<a href", "")

    text = re.sub("(<[^>]*>)", " ", text)
    text = re.sub(r"[^\w\s]", "", text)  
    text = re.sub(r"\s+", " ", text)
    text = text.lower()
    words = text.split(" ")
    return words
    
for i, review in train.iterrows():
    text  = review['Text']
    score = review['Score']
    score -= 1
    tokenized_text = Tokenizer(text)
    for word in tokenized_text:
        if word not in words_set:
            words_set.add(word)
            BOW_df.loc[word] = [0,0,0,0,0]
            BOW_df.loc[word][score] += 1
        else:
            BOW_df.loc[word][score] += 1   


print(BOW_df)

for i, word_freq in BOW_df.iterrows():
    total = 0.0 
    total = word_freq['1'] + word_freq['2'] + word_freq['3'] + word_freq['4'] + word_freq['5']
    #print(total)
    #float(word_freq['1']) / float(total)
    if (word_freq['1'] > 1000) or (word_freq['2'] > 1000) or (word_freq['3'] > 1000) or (word_freq['4'] > 1000) or (word_freq['5'] > 1000) :
        word_freq['1'] = float(word_freq['1']) / float(total)
        word_freq['2'] = float(word_freq['2']) / float(total)
        word_freq['3'] = float(word_freq['3']) / float(total)
        word_freq['4'] = float(word_freq['4']) / float(total)
        word_freq['5'] = float(word_freq['5']) / float(total)
    else:
        word_freq['1'] = 0
        word_freq['2'] = 0
        word_freq['3'] = 0
        word_freq['4'] = 0
        word_freq['5'] = 0

    if (word_freq['1'] == 1) or (word_freq['2'] == 1) or (word_freq['3'] == 1) or (word_freq['4'] == 1) or (word_freq['5'] == 1) :
        word_freq['1'] = 0
        word_freq['2'] = 0
        word_freq['3'] = 0
        word_freq['4'] = 0
        word_freq['5'] = 0

BOW_df = BOW_df.sort_values(['5'] , ascending=[0])
positive_words = BOW_df.iloc[:400, 5:5]

BOW_df = BOW_df.sort_values(['1'] , ascending=[0])
negative_words = BOW_df.iloc[:400, 5:5]

correct_guesses = 0
incorrect_guesses = 0

for i, review in test.iterrows():
    text = review['Text']
    score = review['Score']
    print(text)
    print(score)
    tokenized_text = Tokenizer(text)
    postive_count  = 0
    negative_count = 0
    for word in tokenized_text:
        if word in positive_words.index.values :
            postive_count  += 1
        if word in negative_words.index.values:
            negative_count += 1
    total = postive_count - negative_count
    print("the total is")
    print(total)
    if (total > 0 and score == 4) or (total > 0 and score == 5) or (total < 0 and score == 2) or (total < 0 and score == 1) or (total == 0 and score == 3):
        correct_guesses += 1
    else :
        incorrect_guesses += 1
        
print("correct guesses") 
print(correct_guesses)
print("incorrect guesses")
print(incorrect_guesses)

score = float(correct_guesses) / float(correct_guesses + incorrect_guesses)     

print("Your score is: ")
print(score)

print(BOW_df)
print(positive_words)
print(negative_words)
    
