# Feature-Based Alignment Analyses with LingPy and CLTS 
# Modified from script by Johann-Mattis List
# From https://gist.github.com/LinguList/7fac44813572f65259c872ef89fa64ad
# see https://calc.hypotheses.org/1962

from pyclts import CLTS
from itertools import combinations
import csv,re


# CLTS has a method for converting between IPA and ASJP, 
#  but there were some errors and it needed customising anyway
#  so we've manually coded the translation here:
IPA_to_ASJP = {
 "v": "v",
 "d": "d",
 "r": "r",
 "u": "u",
 "ʃ": "S",
 "o": "o",
 "s": "s",
 "ø": "e",
 "f": "f",
 "e": "e",
 "k": "k",
 "a": "E",
 "æ": "E",
 "ɛ": "E",
 "ʊ": "u",
 "z": "z",
 "ɣ": "x",
 "w": "w",
 "o": "o",
 "e": "e",
 "E": "e",
 "y": "i",
 "m": "m",
 "ŋ": "N",
 "ɛ": "E",
 "i": "i",
 "ɪ": "i",
 "n": "n",
 "ə": "3",
 "l": "l",
 "ɔ": "o",
 "h": "h",
 "t": "t",
 "a": "a",
 "j": "y",
 "u": "u",
 "ʧ": "C",
 "ç": "x", # Not ideal, but closest type
 "b": "b",
 "g": "g",
 "ð": "8",
 "θ": "8",
 "ʒ": "Z",
 "x": "x",
 # Custom translations
 "Þ": "8",
 "W": "w",
 "V": "3",
 "U": "u",
 "E": "e",
 "H": "Z",
 "Θ": "8",
 "F": ["f","v"],
 "əe": ["3","e"],
 "au": ["E","u"],
 "ou": ["o","u"],
 "eai": ["e","E","i"], 
 "eu": ["e","u"], 
 "ei": ["e","i"],
 "ai": ["E","i"],
 "ɛu": ["E","u"],
 "ɛʊ": ["E","u"],
 "aʊ": ["E","u"],
 "ɔʊ": ["o","u"],
 "aɪ": ["E","i"],
 "eɪ": ["e","i"],
 "eʊ": ["e","u"],
 "øʊ": ["e","u"],
 "ɛɪ": ["E","i"]}

clts = CLTS('../data/clts')
bipa = clts.transcriptionsystem('bipa')
asjp = clts.transcriptionsystem('asjpcode')

def getFeatures(segment):

	if segment == "F":
		features = bipa("f")[0]
		features.phonation = 'unspecified'
		return(features)
		
	if segment == "V":
		features = bipa("ə")[0]
		features.height = 'unspecified'
		features.centrality = 'unspecified'
		features.duration = 'unspecified'
		features.roundedness = 'unspecified'
		return(features)
		
	if segment == "E" or segment == "E:":
		features = bipa("e")[0]
		features.duration = "unspecified"
		return(features)
		
	if segment == "Þ" or segment == "Θ":
		features = bipa("θ")[0]
		features.phonation = 'unspecified'
		return(features)
		
	if segment == "W":
		features = bipa("w")[0]
		features.manner = 'unspecified'
		return(features)
		
	if segment == "U":
		features = bipa("u")[0]
		return(features)
		
	if segment == "H":
		features = bipa("ʒ")[0]
		return(features)
		
		
	if segment == "eai":
		segment = "ai"
	if segment == "aue":
		features = bipa("au")[0]
	if segment == "xxx":
		features = bipa("x")[0]
	if segment == "yai":
		features = bipa("ai")[0]
	if segment == "mm":
		features = bipa("m")[0] # geminates are treated properly elsewhere

	features = bipa(segment)[0]

	if features.type is None:
		features.type = "diphthong"
	
	if features.type == "vowel" and features.featuredict["duration"] is None:
		features.duration = "short"
		
	if features.type == "consonant" and features.featuredict["airstream"] is None:
		features.airstream = "normal"
	

	return(features)


def score_dipthongs_v_vowels(dip,vowel,features):
	dipParts = [x for x in re.split("(.\\:?)",dip) if x!=""]
	sx = 0
	for part in dipParts:
		sx += score_sounds(part,vowel,features)
	return(sx/len(dipParts))
	
def score_dipthongs_v_dipthongs(dip1,dip2,features):
	
	dip1Parts = [x for x in re.split("(.\\:?)",dip1) if x!=""]
	dip2Parts = [x for x in re.split("(.\\:?)",dip2) if x!=""]
	sx = 0
	for i in [0,1]:
		sx += score_sounds(dip1Parts[i],dip2Parts[i],features)
	return(sx/len(dip1Parts))
	
def score_sounds(
		a, 
		b, 
		features, 
		classes=None
		):
	"""
	Score sounds with Hamming distance from feature system.
	"""
	
	featureScoreBetweenConsonantsAndVowels = 0

	# Define base score for the classes
	#  here, we weight all tokens equally
	classes = classes or {
		"consonant": 1, 
		"vowel": 1, 
		"diphthong": 1,
		"tone": 1
		}
	
	# convert sounds to transcription system
	sA = getFeatures(a)
	sB = getFeatures(b)
	
	# Handle diphtongs
	if sA.type == "diphthong" and sB.type == "vowel":
		return(score_dipthongs_v_vowels(a,b,features))
	elif sA.type == "vowel" and sB.type == "diphthong":
		return(score_dipthongs_v_vowels(b,a,features))
	elif sA.type == "diphthong" and sB.type == "diphthong":
		return(score_dipthongs_v_dipthongs(a,b,features))

	# return low value if classes don't match
	if sA.type != sB.type:
		return(featureScoreBetweenConsonantsAndVowels)

	# base score is the number of features
	#  (dipthongs are already dealt with above)
	sim = len(features[sA.type]) #(4 in this implementation)

	# normalization factor
	normalize = classes[sA.type] / sim

	# return in case of identity (if normalisation factor is 1, then this will return similarity of 1)
	if a == b:
		return sim * normalize
	
	# reduce similarity in case of mismatch
	for feature in list(set(features[sA.type] + features[sB.type])):
		sAFeat = sA.featuredict[feature]
		sBFeat = sB.featuredict[feature]
		# If the two features are different (and neither are unspecified) ...
		if (sAFeat != sBFeat) and (sAFeat!="unspecified") and (sBFeat!="unspecified"):
		# reduce the similarity
			sim -= 1
	return sim * normalize


def get_feature_scorer(
		tokens, 
		classes=None, 
		features=None
		):
	"""
	Retrieve a scoring dictionary for alignment algorithms.
	"""

	# define the features
	features = {
		"consonant": list(
			bipa['t'].featuredict),
		"vowel": list(
			bipa['a'].featuredict),
		"tone": list(
			bipa['⁵⁵'].featuredict)
		}
	# define base score for the classes
	classes = {
		"consonant": 1, 
		"vowel": 1, 
		"tone": 1
		}
	
	scorer = {}
	for a, b in combinations(tokens, r=2):
		scorer[a, b] = scorer[b, a] = score_sounds(a, b,features)
		scorer[a, a] = score_sounds(a, a,features)
		scorer[b, b] = score_sounds(b, b,features)

	return scorer


def get_historical_scorer(allTokens):
	# Make a scorer based on Jager (2015)
	
#	manualTranslation = {"e":"e","ɔ": "o","ɛ": "E","ø": "e","u": "u","o":"o","i":"i","ə":"3","a":"E","ɣ":"x","ð":"8"}
	# convert all of the tokens to ASJP codes
	asjpSegments = []
	for seg in allTokens:
		seg2 = seg.replace(":","")
		asjpSegments.append(IPA_to_ASJP[seg2])

	mat = []
	# Sound pairs with a positive PMI score provide evidence for relatedness
	# (idetical sounds have high PMI)
	# The scorer needs to reflect similarity, so no need to flip
	#  But we do scale
	with open('../data/JaegerDistances_pnas.1500331112.sd04.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			mat.append(row)
	pmiMin = 100
	pmiMax = -100
	headers = [x for x in mat[0] if x!=""]
	dists = {}
	for i in range(len(mat)-2):
		segi = headers[i]
		for j in range(len(mat[i])-1):
			segj  = headers[j]
			pmi = float(mat[i+1][j+1])
			if pmi < pmiMin:
				pmiMin = pmi
			if pmi > pmiMax:
				pmiMax = pmi
			dists[segi,segj] = pmi
			
	for k in dists:
		dists[k] = ((dists[k]-pmiMin)/ (pmiMax-pmiMin))
	
	historicalScorer = {}
	for i in range(len(asjpSegments)):
		ipa1 = allTokens[i]
		asjp1 = asjpSegments[i]
		for j in range(len(asjpSegments)):
			ipa2 = allTokens[j]
			asjp2 = asjpSegments[j]
			if len(asjp1)==1 and len(asjp2)==1:
				historicalScorer[ipa1,ipa2] = dists[asjp1,asjp2]
			else:
				scores = []
				for s1 in asjp1:
					for s2 in asjp2:
						scores.append(dists[s2,s2])
				score = sum(scores)/len(scores)
				historicalScorer[ipa1,ipa2] = score
						
	return(historicalScorer)

if False:	
	cons = ['p', 't', 'b', 'd', 'pʰ', 'tʰ']
	vows = ['a', 'e', 'i', 'o', 'u']
	scorer = get_scorer(cons+vows)

if False:
	from tabulate import tabulate
	matrix = [[1 for x in cons] for y in cons]
	for (i, a), (j, b) in combinations(enumerate(cons), r=2):
		matrix[i][j] = matrix[j][i] = round(scorer[a, b], 2)
	for i, (c, r) in enumerate(zip(cons, matrix)):
		matrix[i] = [c]+r
	print(tabulate(matrix, headers=cons, tablefmt='pipe'))

	matrix = [[1 for x in vows] for y in vows]
	for (i, a), (j, b) in combinations(enumerate(vows), r=2):
		matrix[i][j] = matrix[j][i] = round(scorer[a, b], 2)
	for i, (c, r) in enumerate(zip(vows, matrix)):
		matrix[i] = [c]+r
	print(tabulate(matrix, headers=vows, tablefmt='pipe'))