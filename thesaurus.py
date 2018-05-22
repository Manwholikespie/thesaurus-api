import requests
from bs4 import BeautifulSoup
from pprint import pprint

"""
I will do my best to come back and add better comments/docstrings to this file
as quick as I can, but for now I think the README should suffice for your
documentation. If I'm being really lazy about it though, just make an issue or
email me and tell me I'm a bitch.
"""

def formatWordUrl(inputWord):
    url = 'http://www.thesaurus.com/browse/'
    url = url + inputWord.strip().lower().replace(' ', '%20')
    return url

def btw(inputString, lh, rh):
    # extract a string between two other strings.
    return inputString.split(lh, 1)[1].split(rh, 1)[0]

def getFilter(keyName, filters):
    return filters['filters'][keyName] if keyName in filters['filters'] else None

def fetchWordData(inputWord):
    url = formatWordUrl(inputWord)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # part of speech and meaning
    posTags = soup.select(".e126ceh80")
    pos = [[z.text for z in x.select('em')][0] for x in posTags]
    meaning = [[z.text for z in x.select('strong')][0] for x in posTags]

    definitionCount = len(posTags)
    defns = []

    for defnNum in range(0, definitionCount):
        wordPath = '.css-1s00u8u'
        data = soup.select(wordPath)

        curr_def = {
            'partOfSpeech': pos[defnNum],
            'meaning': meaning[defnNum],
            'syn': [],
            'ant': []
        }

        if defnNum == 0:
          for x in data: 
              # tuple key is (word, relevance, length, complexity, form)
              entry = ()

              category = x.select('.e1s2bo4t1')
              if len(category) != 0:   # i.e. is it a syn with a hyperlink (most of them)

                entry += (str(category[0].text),)

                cat = category[0].get('class')
                relevance = 0
                c = 'ant'
                if ('css-1hn7aky' in cat or 'css-1usnxsl' in cat):
                  relevance = 3
                  if ('css-1hn7aky' in cat):
                    c = 'syn'
                elif ('css-ebz9vl' in cat or 'css-1sg8uz8' in cat):
                  relevance = 2
                  if ('css-ebz9vl' in cat):
                    c = 'syn'
                elif ('css-vdoou0' in cat or 'css-t2pzdt' in cat):
                  relevance = 1
                  if ('css-vdoou0' in cat):
                    c = 'syn'

                entry += (relevance, len(str(category[0].text)))

                entry += (None,None)

                curr_def[c].append(entry)
        defns.append(curr_def)

    # add origin and examples to the last element so we can .pop() it out later
    clean = lambda x: x.strip().replace('\u201d', '"').replace('\u201c', '"')
    origin = [clean(x.text) for x in soup.select("div#word-origin div p")]

    defns.append({
    'examples': [clean(x.text) for x in soup.select("div#example-sentences div p")],

    # TODO: fix this, as there is a '...' that appears. Use span.oneClick-link
    'origin': origin[0] if len(origin) > 0 else ''
    })

    return defns

class Word:
    def __init__(self, inputWord):
        # in case you want to visit it later
        self.url = formatWordUrl(inputWord)
        self.data = fetchWordData(inputWord)  # fetch the data from thesaurus.com
        self.extra = self.data.pop()

    def __len__(self):
        # returns the number of definitions the word has
        return len(self.data)

    ### FUNCTIONS TO HELP ORGANIZE DATA WITHIN THE CLASS ###
    def filter(self, defnNum='all', **filters):
        """filter out our self.data to reflect only what we need/want in
        different functions
        """
        if len(self) == 0:
            return []

        # here are the available filters that we will pull out of the args.
        relevance = getFilter('relevance', filters)
        partOfSpeech = getFilter('partOfSpeech', filters)
        length = getFilter('length', filters)
        complexity = getFilter('complexity', filters)
        form = getFilter('form', filters)

        # just in-case there is some sort of user error in entering word form.
        if form: # make sure it's not NoneType first.
            if 'informal' in form.lower():
                form = 'informal-word'
            elif 'common' in form.lower():
                form = 'common-word'

        # we are going to assume they want to filter all of the definitions.
        # if not, we will need to only filter over that ONE definition number.
        if defnNum == 'all':
            startRange, endRange = 0, len(self.data)
        else:
            startRange, endRange = defnNum, defnNum+1

        fdata = []  # the data we are going to return

        options = [relevance, length, complexity, form]
        temp_options = list(options)
        made_changes = False
        for x in range(0, len(options)):
            # turn all of our inputs into list forms of said input.
            if type(options[x]) != list:
                options[x] = [options[x]]
                made_changes = True

        if not made_changes:
            options = temp_options # change it back to the fast and easy one.
            optIdx = [i for i, x in enumerate(options) if x is not None]

            # returns the relevant data (aka not the word) for tuple entries
            f = lambda x: [x[1:][z] for z in optIdx] == [options[z] for z in optIdx]

            for x in range(0, len(self.data)):
                # remember: tuple key is (word, relevance, length, complexity,
                # form)
                if (partOfSpeech == None) or (self.data[x]['partOfSpeech'] == partOfSpeech):
                    fdata.append({
                        'syn': [y for y in self.data[x]['syn'] if f(y)],
                        'ant': [y for y in self.data[x]['ant'] if f(y)]
                    })
                else:
                    continue

            return fdata

        # we're SOL. Time to do it the hard'n slow way.
        optIdx = [i for i, x in enumerate(options) if x != [None]]
        options = [options[z] for z in optIdx]

        # tuple key is (word, relevance, length, complexity, form)
        for x in range(startRange, endRange):
            # iterate through definitions
            if (partOfSpeech != None) and (self.data[x]['partOfSpeech'] not in partOfSpeech):
                fdata.append({})
                continue

            c_entry = {'syn': [], 'ant': []}

            for entry_type in ['syn', 'ant']:
                c_def = self.data[x]

                for y in range(0, len(c_def[entry_type])):
                    # iterate through synonym entries
                    word = [c_def[entry_type][y][1:][yy] for yy in optIdx]
                    z, zz = 0, len(word)
                    looksGood = True

                    while (looksGood == True) and (z < zz):
                        opt = word[z]
                        looksGood = True if opt in options[z] else False
                        z += 1

                    if looksGood == True:
                        c_entry[entry_type].append(c_def[entry_type][y])

            fdata.append(c_entry)

        return fdata


    ### FUNCTIONS TO RETURN DATA YOU WANT ###
    """
    Each of the following functions allow you to filter the output
    accordingly: relevance, partOfSpeech, length, complexity, form.
    """
    def synonyms(self,defnNum=0,allowEmpty=True,**filters):
        data = [x['syn'] if 'syn' in x else [] for x in self.filter(defnNum=defnNum, filters=filters)]

        # the word does not exist. return empty.
        if not data:
            return []
        
        data = [[y[0] for y in x] for x in data]

        if defnNum != 'all':
            return data[0]
        else:
            if allowEmpty == True:
                return data
            else:
                return [x for x in data if len(x) is not 0]

    def antonyms(self,defnNum=0,allowEmpty=True,**filters):
        data = [x['ant'] if 'ant' in x else [] for x in self.filter(defnNum=defnNum, filters=filters)]

        # word does not exist. return empty.
        if not data:
            return []
        
        data = [[y[0] for y in x] for x in data]

        if defnNum != 'all':
            return data[0]
        else:
            if allowEmpty == True:
                return data
            else:
                return [x for x in data if len(x) is not 0]

    def origin(self):
        return self.extra['origin']

    def examples(self):
        return self.extra['examples']


if __name__ == '__main__':
	word = Word('happy')
