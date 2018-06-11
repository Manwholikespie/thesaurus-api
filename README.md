# Thesaurus-API
**WARNING**: ~~thesaurus.com recently updated their css to randomize the classes and ids of everything as to prevent scraping. I'll get you guys a fix once I'm done with finals.~~ Edit: Alright I fixed it, but I still need to update the README. The code is now very well documented, so you *might* be able to figure out what to do between these two documents... but either way I'll probably update the README tomorrow so hang tight. Good night, my dear child. May we both dream of progress.

----

Greetings, and welcome to the unofficial api for thesaurus.com. It is compatible with Python 2 and 3. A few of these functions were originally written for an [acronym creator](https://github.com/Manwholikespie/backronym), however I figured other people might want to pull data from thesaurus.com.

## Introduction
With the thesaurus-api, you are able to grab synonyms and antonyms from thesaurus.com. Thanks to the way the website highlights synonym/antonym entries in different colors according to their relevance, I have also included functions to grab certain ranks of syn/ant entries according to the level of relevance you require.

Within the thesaurus class's primary class, `Word`, there are four functions:  
- `Word.synonyms()` : returns a filterable list of the word's synonyms.  
- `Word.antonyms()` : returns a filterable list of the word's antonyms.  
- `Word.origin()` : returns the origin of the word (according to Thesaurus.com).  
- `Word.examples()` : returns sentences showing how the word is used.  

More information is provided about these functions in the *Getting Started* section below.  

## License
Everything in here is licensed under the MIT license. Do with it what you want– make some money. Just don't get me involved.

## Getting Started
First, download the program.  
`git clone https://github.com/Manwholikespie/thesaurus-api`  

Then, install its dependencies.  
`pip install requests`  
`pip install beautifulsoup4`  

Next, navigate to its directory and launch python. 

```bash
$ cd thesaurus-api/
$ python
```

In python, the syntax is fairly simple. You begin by importing and creating a `Word` class.  

```python
>>> from thesaurus import Word
>>> myWord = Word('box')
```
From here, if you wish to get the word's synonyms, you can use the `.synonyms()` function.  
*Note: All of the following information about this function also applies to its inverse, `.antonyms()`*

```python
>>> myWord.synonyms()
[u'carton', u'crate', u'pack', u'trunk', u'package', u'case', u'bin', u'casket', u'chest', u'coffer', u'portmanteau', u'receptacle']
```
This will get you the all of the synonyms under the word's first definition. To see how many definitions a word has, you can measure its length.  

```python
>>> len(myWord)
3
```
The index of its definitions begins at 0, so to get the synonyms for the second definition, you would use:

```python
>>> myWord.synonyms(1)
[u'wrap', u'pack', u'case', u'crate', u'confine', u'package', u'encase']
```
If you used a 0 instead of a 1, you would get the same data as in the first example. If you want to get a list of all the synonyms, but still separated by their definition, you would use 'all'.  

```python
>>> myWord.synonyms('all')
[[u'carton',
  u'crate',
  u'pack',
  u'trunk',
  u'package',
  u'case',
  u'bin',
  u'casket',
  u'chest',
  u'coffer',
  u'portmanteau',
  u'receptacle'],
 [u'wrap', u'pack', u'case', u'crate', u'confine', u'package', u'encase'],
 [u'slug',
  u'hit',
  u'mix',
  u'buffet',
  u'scrap',
  u'sock',
  u'slap',
  u'strike',
  u'cuff',
  u'clout',
  u'wallop',
  u'spar',
  u'whack',
  u'duke',
  u'exchange blows']]
```
This is a lot of data, though, and we may not need all of it. Say you want to filter through the first definition for your word and find words that are of relevance 3.

```python
>>> myWord.synonyms(relevance=3)
[u'carton', u'crate', u'pack', u'trunk', u'package']
```
But maybe you want a bit more data, and you aren't being too strict on relevance, so you could settle for a few level 2's in there. The following will include both relevance 2 and 3. 

```python
>>> myWord.synonyms(relevance=[2,3])
[u'carton', u'crate', u'pack', u'trunk', u'package', u'case', u'bin', u'casket', u'chest', u'coffer', u'portmanteau', u'receptacle']
```

This API allows for quite a bit of fun filtering options. If we wanted to look through all of the definitions of the word 'old', and find words which are complex, lengthy, but still have good relevance:

```python
>>> Word('old').synonyms('all',relevance=[2,3], complexity=[2,3], length=3)
[[], [u'old-fashioned', u'antediluvian'], []]
```

You can also search strictly for results that are `'common'` or `'informal'`. Please note that common does not infer not informal. The majority of words are neither common nor informal.

```python
>>> Word('old').synonyms('all', form='informal')
[[u'hoary', u'wasted'], [u'hackneyed'], []]
>>> Word('old').synonyms(1,form='common')
[u'old-fashioned',
 u'former',
 u'traditional',
 u'original',
 u'past',
 u'remote',
 u'dated',
 u'done',
 u'early',
 u'late',
 u'once',
 u'sometime']
```

Finally, you can search by a definition's part-of-speech. The available options are:  
- `'noun'`  
- `'verb'`  
- `'adj'`  
- `'adv'`  
- `'as in'` (usually for prounouns or interjections)  
- `'prep'`  
- `'conjunction'`  

When using the `partOfSpeech` filter, it is important to use `'all'`, otherwise you will get nothing in the case that a definition's first definition is not your same partOfSpeech.

```python
>>> Word('box').synonyms('all', partOfSpeech='noun')
[[u'carton',
  u'crate',
  u'pack',
  u'trunk',
  u'package',
  u'case',
  u'bin',
  u'casket',
  u'chest',
  u'coffer',
  u'portmanteau',
  u'receptacle'],
 [],
 []]
>>> Word('box').synonyms('all', partOfSpeech='verb')
[[],
 [u'wrap', u'pack', u'case', u'crate', u'confine', u'package', u'encase'],
 [u'slug',
  u'hit',
  u'mix',
  u'buffet',
  u'scrap',
  u'sock',
  u'slap',
  u'strike',
  u'cuff',
  u'clout',
  u'wallop',
  u'spar',
  u'whack',
  u'duke',
  u'exchange blows']]
```
If you do not want to keep the empty definition results in there, you can use `allowEmpty=False` when making your search:  

```python
>>> Word('box').synonyms('all', partOfSpeech='noun', allowEmpty=False)
[[u'carton',
  u'crate',
  u'pack',
  u'trunk',
  u'package',
  u'case',
  u'bin',
  u'casket',
  u'chest',
  u'coffer',
  u'portmanteau',
  u'receptacle']]
```

To recap, the available filtering options and their parameters are:  

```python
relevance=[1,2,3]  
length=[1,2,3]  
complexity=[1,2,3]  
partOfSpeech=['verb','noun','adj','adv','as in','conjunction']  
form=['common','informal']  
```

If you want to filter the data in your own way, you can access the raw word data (it's in tuple form... you can see they key in the thesaurus.py) by calling `.data` on the Word instance.

As for the other functions,

```python
>>> myWord = Word('kettle')
>>> myWord.origin()
u'kettle O.E. cetil (Mercian), from L. catillus "deep pan or dish for cooking," dim. of catinus "bowl, dish, pot." A general Gmc. borrowing (cf. O.S. ketel, O.Fris. zetel, M.Du. ketel, O.H.G. kezzil, Ger. Kessel). Spelling with a -k- (c.1300) probably is from infl. of O.N. cognate ketill. The smaller sense of "tea-kettle" is 20c. Kettledrum is from 1542.'
>>> myWord.examples()
[u'Agnes was bending with red eyes over a kettle which was boiling on the fire.',
 u'She insisted on making tea, and was too quick with the kettle for Edward to help her.',
 u'The hot ascending current passes close by the metal sides of the kettle; while the cold descending current passes down the centre.',
 u'This is distilled water, and is purer than that in the kettle.',
 u'In the winter Snow-white lighted the fire, and put the kettle on, after scouring it, so that it resembled gold in brightness.',
 u'That remarkable change of attitude of his now included the kettle.',
 u"And as Dick gracefully reminds me, the pot can't call the kettle black.",
 u'Take them from the kettle, drain, and brown with butter, salt and pepper.',
 u'When Bill Haden returned from work he found the room done up, the table laid for tea, and the kettle on the fire.',
 u'But, to his surprise, no tanuki was there, nothing but the kettle he had found in the corner.']
```

## Coming Soon
~~Make a findWord(inputWord) function that will return both synonyms and antonyms of individual ranks into a dictionary.~~

~~A Function that allows you to search for the synonyms/antonyms of a different definition of the word you are searching for (right now those are hidden in different tabs, but I should be able to fix that by changing the beautifulsoup selector to div#synonyms-[1,2,3, etc.].~~

~~Make a class that allows us to call anything we want from it more easily. I want to just specify a word class with the only input being the word, and then call word.synonyms, word.origin, etc.~~

~~Come up with a more organized way of naming the functions so that I don't confuse people.~~

In addition to having a ['meaning'] part of each definition's dictionary when using findWordTotal, add a ['nltk meaning'] section so that it plays nicely with nltk's part-of-speech tagger.

Add automated tests and badges to show supported versions of Python, and detect any errors.

## Special Thanks
To [James](https://github.com/jaykm/) for the idea to just use rstrip() instead of something much more complicated to single-out an entry's relevanceLevel.

To [Kyle](https://github.com/AFishNamedFish) for his interest in this project. You rock, Kyle.

To [Stefano](https://github.com/stefano-bragaglia) for suggesting that I add filtering to function output.

To [Suhas](https://github.com/syelluru) for correcting my errors.
