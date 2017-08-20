import gensim 
import logging 
import os.path

class LineCorpus(gensim.corpora.textcorpus.TextCorpus):
	# Creates the corpus object that reads the document line by line
    def get_texts(self):
        with open(self.input) as f:
            for l in f:
                yield l.split()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if os.path.isfile('lda_model'):  
	# Check if the model has previously been created
	# if it has load the model and print out the different topics
	print("lda model was found")
	model = gensim.models.LdaModel.load('lda_model')
	print("number of topics : ")
	print(model.num_topics)
	for i in range(0,model.num_topics - 1):
		print("topic number : ")
		print(i)
		print(model.print_topic(i))
	doc = ['wonderful', 'action', 'packed', 'movie', 'steven', 'seagal', 'five', 'star']
	bow = model.id2word.doc2bow(doc)
	topic_analysis = model[bow]
	print(topic_analysis)
else:
	corpus = LineCorpus('reviews.txt')
	print("creating lda model")
	model = gensim.models.LdaModel(corpus, id2word=corpus.dictionary, alpha='auto', num_topics=10, passes=5)
	model.save('lda_model')

