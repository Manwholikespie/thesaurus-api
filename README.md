# Thesaurus-API

Greetings, and welcome to the unofficial api for thesaurus.com. It is compatible with Python 2 and 3. While the code is quite readable, this documentation is your friend— as am I :) Let me know if there's anything you have trouble with, or if you have any ideas on how to make it better.

**Note**: If you have used this library before, be warned that some things have changed. Thesaurus.com updated their code— removing complexity filtering and changing how they classify "informal" words. On the bright side, there is now an `isVulgar` filter.  

## Introduction
With the thesaurus-api, you are able to grab synonyms and antonyms from thesaurus.com. Thanks to the way the website highlights synonym/antonym entries in different colors according to their relevance, I have also included functions to grab certain ranks of syn/ant entries according to the level of relevance you require.

Within the thesaurus class's primary class, `Word`, there are four functions:  
- `Word.synonyms()` : returns a filterable list of the word's synonyms.  
- `Word.antonyms()` : returns a filterable list of the word's antonyms.  
- `Word.origin()` : returns the origin of the word (according to Thesaurus.com).  
- `Word.examples()` : returns sentences showing how the word is used.  

More information is provided about these functions in the *Getting Started* section below.  

## License
Everything in here is licensed under the MIT license. Do with it what you want– make some money. Just know that if you use my code (or even star this repo), and I see that you work at the Betty Crocker Company (or some other equally prestigious venture)— I will most likely write on my resume that you use my code to great satisfaction.  

## Getting Started
You can install the module by doing:  
`$ pip install thesaurus` 

If for some reason the dependencies didn't install, you can install them by doing:  
`$ pip install requests`  
`$ pip install beautifulsoup4`  

In python, the syntax is fairly simple. You begin by importing and creating a `Word` class.  

```python
>>> from thesaurus import Word
>>> w = Word('box')
```
From here, if you wish to get the word's synonyms, you can use the `.synonyms()` function.  
*Note: All of the following information about this function also applies to its inverse, `.antonyms()`*

```python
>>> w.synonyms()
['carton', 'crate', 'pack', 'package', 'trunk', 'bin', 'case', 'casket', 'chest', 'coffer', 'portmanteau', 'receptacle']
```
This will get you the all of the synonyms under the word's first definition. To see how many definitions a word has, you can measure its length.  

```python
>>> len(w)
3
```
The index of its definitions begins at 0, so to get the synonyms for the second definition, you would use:

```python
>>> w.synonyms(1)
['wrap', 'pack', 'case', 'crate', 'confine', 'package', 'encase']
```
If you used a 0 instead of a 1, you would get the same data as in the first example. If you want to get a list of all the synonyms, but still separated by their definition, you would use 'all'.  

```python
>>> w.synonyms('all')
[['carton',
  'crate',
  'pack',
  'package',
  'trunk',
  'bin',
  'case',
  'casket',
  'chest',
  'coffer',
  'portmanteau',
  'receptacle'],
 ['wrap', 'pack', 'case', 'crate', 'confine', 'package', 'encase'],
 ['slug',
  'hit',
  'mix',
  'buffet',
  'scrap',
  'sock',
  'slap',
  'strike',
  'cuff',
  'clout',
  'wallop',
  'spar',
  'whack',
  'duke',
  'exchange blows']]
```

*Quick Note*: There are a lot of filtering options, and thus a long tutorial for how to use them. Here's a quick list of the available filters. More is explained below...

```python
relevance=[1,2,3]  
length=[1,2,3]  
partOfSpeech= [... see the table. POS_* ...]
form=['common','informal'] # or th.FORM_COMMON, th.FORM_INFORMAL
isVulgar=[True, False]
```

This is a lot of data, though, and we may not need all of it. Say you want to filter through the first definition for your word and find words that are of relevance 3.

```python
>>> w.synonyms(relevance=3)
['carton', 'crate', 'pack', 'package', 'trunk']
```
But maybe you want a bit more data, and you aren't being too strict on relevance, so you could settle for a few level 2's in there. The following will include both relevance 2 and 3. 

```python
>>> w.synonyms(relevance=[2,3])
['carton', 'crate', 'pack', 'package', 'trunk', 'bin', 'case', 'casket', 'chest', 'coffer', 'portmanteau', 'receptacle']
```

This API allows for quite a bit of fun filtering options. If we wanted to look through all of the definitions of the word 'old', and find words which are lengthy and have good relevance:

```python
>>> Word('old').synonyms('all', relevance=[2,3], length=3)
[[], ['old-fashioned', 'traditional', 'antediluvian'], ['established']]
```

You can also search strictly for results that are `'common'` or `'informal'`. If you have used this library previously, please know that `'common'` now **does** mean *not informal*. Thus, if you want all the words, don't specify a form filter. If you want only informal words, specify `form='informal'`. If you don't want any informal words, specify `form='common'`.  

**Note**: I have recently implemented global constants that you can import and use instead of these strings. For the form filter, they are:

```python
FORM_INFORMAL = 'informal'
FORM_COMMON   = 'common'
```

```python
>>> import thesaurus as th
>>> th.Word('old').synonyms('all', form='informal') # or form=th.FORM_INFORMAL
[['hoary', 'wasted'], ['hackneyed'], []]
>>> th.Word('old').synonyms(1, form='common') # or form=th.FORM_COMMON
['antique', 'age-old', 'venerable', 'crumbling', 'old-fashioned', 'primitive', 'former', 'traditional', 'old-time', 'outmoded', 'original', 'antediluvian', 'relic', 'bygone', 'past', 'aboriginal', 'remote', 'antiquated', 'archaic', 'dated', 'decayed', 'done', 'early', 'erstwhile', 'immemorial', 'late', 'moth-eaten', 'once', 'onetime', 'out-of-date', 'passé', 'primeval', 'primordial', 'pristine', 'rusty', 'sometime', 'stale', 'superannuated', 'unfashionable', 'unoriginal', 'worn-out', 'olden', 'quondam', 'cast-off', 'demode', 'of old', 'of yore', 'oldfangled', 'time-worn']
```

Finally, you can filter by a definition's part-of-speech. Please note that these values are directly inline with the constants thesaurus.com has chosen. To prevent you from making mistakes, I have also expressed these as global constants— in their abbreviated and full forms:


| Constant  | String Value |
| ------------- | ------------- |
| POS\_ADJECTIVE, POS\_ADJ  | 'adj'  |
| POS\_ADVERB, POS\_ADV  | 'adv' |
| POS\_CONTRADICTION, POS\_CONT | 'contradiction' |
| POS\_CONJUNCTION, POS\_CONJ | 'conj' |
| POS\_DETERMINER, POS\_DET | 'determiner' |
| POS\_INTERJECTION, POS\_INTERJ | 'interj' |
| POS\_NOUN | 'noun' |
| POS\_PREFIX | 'prefix' |
| POS\_PREPOSITION, POS\_PREP | 'prep' |
| POS\_PRONOUN, POS\_PRON | 'pron' |
| POS\_VERB | 'verb' |
| POS\_ABBREVIATION, POS\_ABB | 'abb' |
| POS\_PHRASE | 'phrase' |
| POS\_ARTICLE | 'article' |

When using the `partOfSpeech` filter, it is important to use `'all'`, otherwise you will get nothing in the case that a definition's first definition is not your same partOfSpeech.

```python
>>> import thesaurus as th
>>> th.Word('box').synonyms('all', partOfSpeech='noun') # or th.POS_NOUN
[['carton',
  'crate',
  'pack',
  'package',
  'trunk',
  'bin',
  'case',
  'casket',
  'chest',
  'coffer',
  'portmanteau',
  'receptacle'],
 [],
 []]
>>> th.Word('box').synonyms('all', partOfSpeech='verb') # or th.POS_VERB
[[],
 ['wrap', 'pack', 'case', 'crate', 'confine', 'package', 'encase'],
 ['slug',
  'hit',
  'mix',
  'buffet',
  'scrap',
  'sock',
  'slap',
  'strike',
  'cuff',
  'clout',
  'wallop',
  'spar',
  'whack',
  'duke',
  'exchange blows']]
```
If you do not want to keep the empty definition results in there, you can use `allowEmpty=False` when making your search:  

```python
>>> import thesaurus as th
>>> th.Word('box').synonyms('all', partOfSpeech=th.POS_NOUN, allowEmpty=False)
[['carton',
  'crate',
  'pack',
  'package',
  'trunk',
  'bin',
  'case',
  'casket',
  'chest',
  'coffer',
  'portmanteau',
  'receptacle']]
```

Introduced after the Spring Synonym Schism of 2018, thesaurus.com added the `isVulgar` option to filter out vulgar options.

```python
>>> Word('gay').synonyms('all', isVulgar=True)
[['homophile', 'lesbian', 'queer', 'Sapphic', 'homoerotic'], [], []]
```

To recap, the available filtering options and their parameters are:  

```python
relevance=[1,2,3]  
length=[1,2,3]  
partOfSpeech= [... see the table. POS_* ...]
form=['common','informal'] # or th.FORM_COMMON, th.FORM_INFORMAL
isVulgar=[True, False]
```

If you want to filter the data in your own way, you can access the raw word data (it's in tuple form... you can see they key in the thesaurus.py) by calling `.data` on the Word instance.

As for the other functions,

```python
>>> w = Word('kettle')
>>> w.origin()
'Old English cetil (Mercian), from Latin catillus "deep pan or dish for cooking," diminutive of catinus "bowl, dish, pot." A general Germanic borrowing (cf. Old Saxon ketel, Old Frisian zetel, Middle Dutch ketel, Old High German kezzil, German Kessel). Spelling with a -k- (c.1300) probably is from influence of Old Norse cognate ketill. The smaller sense of "tea-kettle" is attested by 1769.'
>>> w.examples()
['Then strain the liquor through a sieve, and put it into a kettle or stew-pan.',
 'Skim them well, and keep the kettle covered when you are not skimming.'
 'Cover the jar, and set it up to the neck in a kettle of boiling water.',
 'Cover the bottom of a large boiler or kettle with saw-dust or straw.',
 'If the pot wants replenishing, do it with boiling water from a kettle.',
 'There was a kettle on the hob, as there had been night and day for fifteen years.',
 "If I'd got a few handy, I should have the kettle boiling all the sooner.",
 'After they had had their smoke, passing the pipes from mouth to mouth, I brought forth our kettle.',
 'The rising tide was almost on us when they returned with a kettle full of hot tea.',
 'Stanton took charge of the kettle and dished out the rations that night.']
```

## Coming Soon
~~Make a findWord(inputWord) function that will return both synonyms and antonyms of individual ranks into a dictionary.~~

~~A Function that allows you to search for the synonyms/antonyms of a different definition of the word you are searching for (right now those are hidden in different tabs, but I should be able to fix that by changing the beautifulsoup selector to div#synonyms-[1,2,3, etc.].~~

~~Make a class that allows us to call anything we want from it more easily. I want to just specify a word class with the only input being the word, and then call word.synonyms, word.origin, etc.~~

~~Come up with a more organized way of naming the functions so that I don't confuse people.~~

Add nltk pos mappings.

Add automated tests and badges to show supported versions of Python, and detect any errors.

## Special Thanks
To [James](https://github.com/jaykm/) for the idea to just use rstrip() instead of something much more complicated to single-out an entry's relevanceLevel.

To [Kyle](https://github.com/AFishNamedFish) for his interest in this project. You rock, Kyle.

To [Stefano](https://github.com/stefano-bragaglia) for suggesting that I add filtering to function output.

To [Suhas](https://github.com/syelluru) for correcting my errors.

To [Bradley](https://github.com/bradleyfowler123) for his help in designing the `isVulgar` UX. He and his synonym-loving grandmother shall receive an authentic Manwholikespie personal poem one of these days.  
