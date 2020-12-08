import sys
import re
import os
import csv
import nltk
import string
from os import listdir
from itertools import product
from os.path import isfile, join
from stemming.porter2 import stem
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

def tokenize(text):
	'''Tokenize and Stem words for tf-idf'''
	tokens = nltk.word_tokenize(text)
	stems = []
	for item in tokens:
		stems.append(PorterStemmer().stem(item))
	return stems

def get_token_dict(folder_path, folder_names):
	'''Create token dictionary for tf-idf'''
	token_dict = {}

	for var in range(len(folder_names)):
		path = folder_path + folder_names[var] + "\\"
		for dirpath, dirs, files in os.walk(path):
			for f in files:
				fname = os.path.join(dirpath, f)
				
				with open(fname) as pearl:
					text = pearl.read()
					token_dict[f] = text.lower().translate(string.punctuation)

	return token_dict

def collectFeatures():
	'''Read the email and collect features like words, bigrams, trigrams'''
	w = []
	subd, wordsd = {}, {}
	digramsd={}
	trigramsd={}
	numbers=[]
	dollars=[]
	urls=[]
	emails=[]
	count_number=[]
	count_dollar=[]
	count_mail=[]
	count_url=[]
	stop=stopwords.words("english")
	counter=0

	# for each folder/category
	for loop_var in range(len(folder_names)):
		mypath = join(folder_path, folder_names[loop_var])
		os.chdir(mypath)
		# fp = open(current_path + 'features_' + str(loop_var) + '.txt', 'w') # write features into features.txt file
		# for each email
		for fo in listdir(mypath):
			if isfile(join(mypath,fo)):
				count_number.append(0)
				f=open(fo,"r")
				fr=f.read()
				subl=[]

				# read and collect features in subject line
				match=re.search('subject:(.+)\n',fr.lower())
				if match:
					subl=subl+[w for w in re.split('\W',match.group(1)) if w]
					
					for i in subl:
						if i.isdigit():
							count_number[counter]+=1

					for i in subl:
						if i in stop:
							subl.remove(i)

					for i,j in zip(subl,subl[1:]):
						i=stem(i)
						j=stem(j)
						if i+" "+j in digramsd:
							digramsd[i+" "+j]+=1
						else:
							digramsd[i+" "+j]=1

					for i,j,k in zip(subl,subl[1:],subl[2:]):
						i=stem(i)
						j=stem(j)
						k=stem(k)
						if i+" "+j+" "+k in trigramsd:
							trigramsd[i+" "+j+" "+k]+=1
						else:
							trigramsd[i+" "+j+" "+k]=1

					for elements in subl:
						element=stem(elements)
						if element in subd:
							subd[element]+=1
						else:
							subd[element]=1
				f.close()               
				
				# read and collect features in email content
				f=open(fo,"rU")
				flag=0
				wordsl=[]
				for line in f:
					if flag==0 and not re.search(r'x-filename',line.lower()):
						continue
					elif flag==0 and re.search(r'x-filename',line.lower()):
						flag=1
						continue
					elif not ( re.search(r'forwarded by',line.lower()) or re.search(r'original message',line.lower()) ):
				   
						wordsl=wordsl+[w for w in re.split('\W',line.lower()) if w]
					elif re.search(r'forwarded by',line.lower()) or re.search(r'original message',line.lower()):
						break
				
				for i in wordsl:
					if i.isdigit():
						count_number[counter]+=1

				for i in wordsl:
					if i in stop:
						wordsl.remove(i)

				for i,j in zip(wordsl,wordsl[1:]):
					i=stem(i)
					j=stem(j)
					if i+" "+j in digramsd:
						digramsd[i+" "+j]+=1
					else:
						digramsd[i+" "+j]=1

				for i,j,k in zip(wordsl,wordsl[1:],wordsl[2:]):
					i=stem(i)
					j=stem(j)
					k=stem(k)
					if i+" "+j+" "+k in trigramsd:
						trigramsd[i+" "+j+" "+k]+=1
					else:
						trigramsd[i+" "+j+" "+k]=1

				for elements in wordsl:
					element=stem(elements)
					if element in wordsd:
						wordsd[element]+=1
					else:
						wordsd[element]=1
				f.close()

				# collect features like email-ids and urls
				f=open(fo,"rU")
				count_mail.append(0)
				count_url.append(0)
				emails=[]
				urls=[]
				for line in f:
					if not ( re.search(r'forwarded by',line.lower()) or re.search(r'original message',line.lower()) ):
						emails=[]
						urls=[]
						emails = emails + re.findall(r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+',line)
						urls = urls + re.findall(r'www.',line)
						for email in emails:
							count_mail[counter]+=1
						for url in urls:
							count_url[counter]+=1
					else:
						break
				counter+=1
				f.close()
					
				# write into features.txt
				# for p in subd.items():
				#         fp.write(f.name+":%s:%s\n" % p)
				# for p in wordsd.items():
				#         fp.write(f.name+":%s:%s\n" % p)

	return subd, wordsd, digramsd, trigramsd, count_number, count_mail, count_url

def makefiles(workfilename, wordfilename):
	'''Write collected features into workfiles with names workfilename and wordfilename'''
	w = []
	fw = open(folder_path + workfilename, 'w') # open workfile
	words_file = open(folder_path + wordfilename, 'w') # open wordfile
	counter=0
	stop=stopwords.words("english")
	
	# Perform tf-idf
	token_dict = get_token_dict(folder_path, folder_names)
	tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
	tfs = tfidf.fit_transform(token_dict.values())

	# for each folder/category
	for loop_var in range(len(folder_names)):
		mypath = folder_path + folder_names[loop_var]
		os.chdir(mypath)
		# write all the feature words into wordfile
		if loop_var == 0:
			for elements in wordsd:
				if wordsd[elements] > cut_off:
					words_file.write(elements+',')
			words_file.write('`~1,')
			for elements in subd:
				if subd[elements] > cut_off:
					words_file.write(elements+',')
			words_file.write('`~2,')
			for elements in digramsd:
				if digramsd[elements] > 1:
					words_file.write(elements+',')
			words_file.write('`~3,')
			# to avoid last extra comma ','
			first = True
			for elements in trigramsd:
				if trigramsd[elements] > 1:
					if first:
						words_file.write(elements)
						first = False
					else:
						words_file.write(','+elements)
			words_file.write('\n')
			words_file.close()

		# for each email
		for fo in listdir(mypath):
			if isfile(join(mypath,fo)):
				subd_temp={}
				wordsd_temp={}
				digramsd_temp={}
				trigramsd_temp={}
				f=open(fo,"rU")
				fr=f.read()
				fr=fr.lower()
				subl=[]
				response = tfidf.transform([fr])
				feature_names = tfidf.get_feature_names()
				# read and collect features in subject line
				match=re.search('subject:(.+)\n',fr)
				if match:
					subl=subl+[w for w in re.split('\W',match.group(1)) if w]

					for i in subl:
						if i in stop:
							subl.remove(i)

					for i,j in zip(subl,subl[1:]):
						i=stem(i)
						j=stem(j)
						if i+" "+j in digramsd_temp:
							digramsd_temp[i+" "+j]+=1
						else:
							digramsd_temp[i+" "+j]=1

					for i,j,k in zip(subl,subl[1:],subl[2:]):
						i=stem(i)
						j=stem(j)
						k=stem(k)
						if i+" "+j+" "+k in trigramsd_temp:
							trigramsd_temp[i+" "+j+" "+k]+=1
						else:
							trigramsd_temp[i+" "+j+" "+k]=1

					for elements in subl:
						element=stem(elements)
						if element in subd:
							if element in subd_temp:
								subd_temp[element]+=1
							else:
								subd_temp[element]=1

				# read and collect features in email content
				f.close()
				f=open(fo,"rU")
				flag=0
				wordsl=[]
				for line in f:
					if flag==0 and not re.search(r'x-filename',line.lower()):
						continue
					elif flag==0 and re.search(r'x-filename',line.lower()):
						flag=1
						continue
					elif not ( re.search(r'forwarded by',line.lower()) or re.search(r'original message',line.lower()) ):
						wordsl=wordsl+[w for w in re.split('\W',line.lower()) if w]
					elif re.search(r'forwarded by',line.lower()) or re.search(r'original message',line.lower()):
						break

				for i in wordsl:
						if i in stop:
							wordsl.remove(i)

				for i,j in zip(wordsl,wordsl[1:]):
						i=stem(i)
						j=stem(j)
						if i+" "+j in digramsd_temp:
							digramsd_temp[i+" "+j]+=1
						else:
							digramsd_temp[i+" "+j]=1

				for i,j,k in zip(wordsl,wordsl[1:],wordsl[2:]):
						i=stem(i)
						j=stem(j)
						k=stem(k)
						if i+" "+j+" "+k in trigramsd_temp:
							trigramsd_temp[i+" "+j+" "+k]+=1
						else:
							trigramsd_temp[i+" "+j+" "+k]=1

				for elements in wordsl:
					element=stem(elements)
					if element in wordsd:
						if element in wordsd_temp:
							wordsd_temp[element]+=1
						else:
							wordsd_temp[element]=1

				for word in wordsd:
					if wordsd[word] > cut_off:
						if word in wordsd_temp:
							if word in feature_names:
								fw.write(str(wordsd_temp[word]*response[0,feature_names.index(word)]))
								fw.write(',')
							else:
								fw.write(str(wordsd_temp[word]))
								fw.write(',')
							
						else:
							fw.write('0,')

				for subject_word in subd:
					if subd[subject_word] > cut_off:
						if subject_word in subd_temp:
							if subject_word in feature_names:
								fw.write(str(subd_temp[subject_word]*response[0,feature_names.index(subject_word)]*subject_weight))
								fw.write(',')
							else:
								fw.write(str(subd_temp[subject_word]*subject_weight))
								fw.write(',')
						else:
							fw.write('0,')

				for digram_word in digramsd:
					if digramsd[digram_word] > 1:
						if digram_word in digramsd_temp:
							fw.write(str(digramsd_temp[digram_word]))
							fw.write(',')
						else:
							fw.write('0,')
							
				
				for trigram_word in trigramsd:
					if trigramsd[trigram_word] > 1:
						if trigram_word in trigramsd_temp:
							fw.write(str(trigramsd_temp[trigram_word]))
							fw.write(',')
						else:
							fw.write('0,')
							
				fw.write(str(count_url[counter]))
				fw.write(',')

				fw.write(str(count_mail[counter]))
				fw.write(',')

				fw.write(str(count_number[counter]))
				fw.write(',')

				counter+=1

				fw.write(str(loop_var) + '\n')

def loadTrainingset(current_path, workfilename, wordfilename, trainingSet):
	'''Load training set and training words from specified files in the given current_path'''
	# load training set
	with open(current_path + workfilename, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(len(dataset)):
			for y in range(len(dataset[x])):			
				dataset[x][y] = float(dataset[x][y])
			trainingSet.append(dataset[x])
	csvfile.close()

	# load training words
	with open(current_path + wordfilename, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		
		index1 = dataset[0].index('`~1')
		index2 = dataset[0].index('`~2')
		index3 = dataset[0].index('`~3')

		wordsd = dataset[0][:index1]
		subd = dataset[0][index1+1:index2]
		digramsd = dataset[0][index2+1:index3]
		trigramsd = dataset[0][index3+1:]
				
	return wordsd, subd, digramsd, trigramsd

def loadTestset(folder_path, folder_names, wordsd, subd, digramsd, trigramsd):
	'''Load test set for new emails'''
	w = []
	testSet = []
	numbers=[]
	dollars=[]
	urls=[]
	emails=[]
	count_number=[]
	count_dollar=[]
	count_mail=[]
	count_url=[]
	all_files = []
	counter=0	
	subject_weight = 4
	similarity_cutoff = 0.8
	stop=stopwords.words("english")

	# tf-idf
	token_dict = get_token_dict(folder_path, folder_names)
	tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
	tfs = tfidf.fit_transform(token_dict.values())
	
	# for each folder/category (incase where new emails are a test set)
	for loop_var in range(len(folder_names)):
		mypath = folder_path + folder_names[loop_var]
		os.chdir(mypath)

		# for each email
		for fo in listdir(mypath):
			if isfile(join(mypath,fo)):
				all_files.append(mypath + '/' + fo)
				temp_list = []
				subd_temp={}
				wordsd_temp={}
				digramsd_temp={}
				trigramsd_temp={}
				f=open(fo,"rU")
				fr=f.read()
				fr=fr.lower()
				subl=[]
				count_number.append(0)
				
				response = tfidf.transform([fr])
				feature_names = tfidf.get_feature_names()

				# read and collect features in subject line
				match=re.search('subject:(.+)\n',fr)
				if match:
					subl=subl+[w for w in re.split('\W',match.group(1)) if w]
					
					for i in subl:
						if i.isdigit():
							count_number[counter]+=1

					for i in subl:
						if i in stop:
							subl.remove(i)

					for i,j in zip(subl,subl[1:]):
						i=stem(i)
						j=stem(j)
						if i+" "+j in digramsd_temp:
							digramsd_temp[i+" "+j]+=1
						else:
							digramsd_temp[i+" "+j]=1

					for i,j,k in zip(subl,subl[1:],subl[2:]):
						i=stem(i)
						j=stem(j)
						k=stem(k)
						if i+" "+j+" "+k in trigramsd_temp:
							trigramsd_temp[i+" "+j+" "+k]+=1
						else:
							trigramsd_temp[i+" "+j+" "+k]=1

					for elements in subl:
						element=stem(elements)
						if element in subd_temp:
							subd_temp[element]+=1
						else:
							subd_temp[element]=1
				f.close()

				# read and collect features in email content
				f=open(fo,"rU")
				flag=0
				wordsl=[]
				for line in f:
					if flag==0 and not re.search(r'x-filename',line.lower()):
						continue
					elif flag==0 and re.search(r'x-filename',line.lower()):
						flag=1
						continue
					elif not ( re.search(r'forwarded by',line.lower()) or re.search(r'original message',line.lower()) ):
						wordsl=wordsl+[w for w in re.split('\W',line.lower()) if w]
					elif re.search(r'forwarded by',line.lower()) or re.search(r'original message',line.lower()):
						break

				for i in wordsl:
					if i.isdigit():
						count_number[counter]+=1

				for i in wordsl:
						if i in stop:
							wordsl.remove(i)

				for i,j in zip(wordsl,wordsl[1:]):
						i=stem(i)
						j=stem(j)
						if i+" "+j in digramsd_temp:
							digramsd_temp[i+" "+j]+=1
						else:
							digramsd_temp[i+" "+j]=1

				for i,j,k in zip(wordsl,wordsl[1:],wordsl[2:]):
						i=stem(i)
						j=stem(j)
						k=stem(k)
						if i+" "+j+" "+k in trigramsd_temp:
							trigramsd_temp[i+" "+j+" "+k]+=1
						else:
							trigramsd_temp[i+" "+j+" "+k]=1

				for elements in wordsl:
					element=stem(elements)
					if element in wordsd_temp:
						wordsd_temp[element]+=1
					else:
						wordsd_temp[element]=1
				f.close()

				# collect additional features like email_ids and urls
				f=open(fo,"rU")
				count_mail.append(0)
				count_url.append(0)
				emails=[]
				urls=[]
				for line in f:
					if not ( re.search(r'forwarded by',line.lower()) or re.search(r'original message',line.lower()) ):
						emails=[]
						urls=[]
						emails = emails + re.findall(r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+',line)
						urls = urls + re.findall(r'www.',line)
						for email in emails:
							count_mail[counter]+=1
						for url in urls:
							count_url[counter]+=1
					else:
						break
				f.close()

				# collect features using synonyms and similarity in email content
				for word in wordsd:
					if word in wordsd_temp:
						if word in feature_names:
							temp_list.append(wordsd_temp[word]*response[0,feature_names.index(word)])
						else:
							temp_list.append(wordsd_temp[word])
					else:
						synonyms, flag = [], False
						for syn in wordnet.synsets(word):
							for l in syn.lemmas():
								synonyms.append(l.name())
						for synonym in synonyms:
							if synonym in wordsd_temp:
								temp_list.append(wordsd_temp[synonym])
								flag = True
								break
						if flag == False:
							syn1 = wordnet.synsets(word)
							for word2 in wordsd_temp:
								syn2 = wordnet.synsets(word2)
								for sense1, sense2 in product(syn1, syn2):
									sim = wordnet.wup_similarity(sense1, sense2)
									if sim and sim >= similarity_cutoff:
										temp_list.append(wordsd_temp[word2])
										flag = True
										break
									break # Use this break to check only first Synsets
								if flag == True:
									break
							if flag == False:
								temp_list.append(0)
				
				# collect features using synonyms and similarity in subject line
				for word in subd:
					if word in subd_temp:
						if word in feature_names:
							temp_list.append(subd_temp[word]*response[0,feature_names.index(word)]*subject_weight)
						else:
							temp_list.append(subd_temp[word]*subject_weight)
					else:
						synonyms, flag = [], False
						for syn in wordnet.synsets(word):
							for l in syn.lemmas():
								synonyms.append(l.name())
						for synonym in synonyms:
							if synonym in subd_temp:
								temp_list.append(subd_temp[synonym]*subject_weight)
								flag = True
								break
						if flag == False:
							syn1 = wordnet.synsets(word)
							for word2 in subd_temp:
								syn2 = wordnet.synsets(word2)
								for sense1, sense2 in product(syn1, syn2):
									sim = wordnet.wup_similarity(sense1, sense2)
									if sim and sim >= similarity_cutoff:
										temp_list.append(subd_temp[word2])
										flag = True
										break
									break # Use this break to check only first Synsets
								if flag == True:
									break
							if flag == False:
								temp_list.append(0)
				
				for digram in digramsd:
					if digram in digramsd_temp:
						temp_list.append(digramsd_temp[digram])
					else:
						temp_list.append(0)

				for trigram in trigramsd:
					if trigram in trigramsd_temp:
						temp_list.append(trigramsd_temp[trigram])
					else:
						temp_list.append(0)
				
				temp_list.append(count_url[counter])
				temp_list.append(count_mail[counter])
				temp_list.append(count_number[counter])
				temp_list.append(loop_var)

				counter += 1

				testSet.append(temp_list)
	return testSet, all_files

def main(dataset_name):
	'''Main function to start execution of extract.py'''
	global folder_names, subject_weight, cut_off, current_path, folder_path
	global subd, wordsd, digramsd, trigramsd, count_number, count_mail, count_url

	subject_weight = 3
	cut_off = 5

	current_path = os.path.dirname(os.path.abspath(__file__))
	folder_path = os.path.join(current_path, dataset_name)
	folder_names = next(os.walk(folder_path))[1]
	if 'results' in folder_names:
		folder_names.remove('results')

	print('Collecting Features...')
	subd, wordsd, digramsd, trigramsd, count_number, count_mail, count_url = collectFeatures()
	print('Features collected successfully.')

	print('Making Workfile...')
	makefiles('mergedworkfile.csv', 'wordfile.csv')
	print('Workfile complete.\nProgram run successful.')
					
if __name__ == '__main__':
	main("dataset")