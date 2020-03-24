A series of scripts i built that helped me get rid of old movies in my collection.

1. You start with sh `getLatestResults.sh` which will fetch a 
tree structure of a folder. It uses tree command with json 
output to store all files/folders in a json file.
2. Then you run `python extractPossibleMoviesFromTreeJsonOutput.py`
that help you filter out files are are 1. No videos (configured 
by a list of recognized video formats) 2. file size.
3. Then you run `python3 extractInfoAboutMoviesFromFullPath.py` 
that will go through all files filtered in step 2 and fetch
movie details from imdb.
   - GuessIt Library used for fetching movie name.
       - First i attempt to decipher a movie name from the filename. 
       - This is non trivial as the file name cannot be exact match 
       always.
       - We use GuessIt library to perform this task, which uses 
       decision trees and classifiers to magically find out 
       probable movie name.
       - This process does not reveal exact movie name, because of
       the nature of the problem, it all comes down to tweaking 
       the algorithm to maximise your data accuracy.
       - Sometimes there will be information missing in movie
       name, such as year, which will make it difficult to distinguish 
       between 2 movies of same name but from different year.
   - ImdbPy library used for fetch imdb results.
       - After finding most probable movie name, we search on imdb 
       with that name, fetching results.
       - we filter out results on a few parameters, such as
           - Year matching
           - Type of result - movie/tv series 
           - % title match (string matching)
       - We are left with a single, accurate search result, for 
       majority of cases.
       - Rest, we'll have to manually intervene for.
4. Then we run `python filterOutResults.py`. This script further
filter out results like - 
   - hasRating(movieResult) and 
   - isOlderThanFile(movieResult, entry) and 
   - doesNotContainTVinTitle
5. Then we run `python extractDeletableMovies.py` Which, 1. detect
movies that suck (<7 rating or <3 for comedies), moves them to 
a delete arrya, then provides an interactive menu, that gives 
us a choice to choose the correct result, in cases we were 
not able to identify exact match using steps above.
6. The result of step 5 is fed into `python deduplicateMovies.py` 
which allows us to detect duplicate movies and put them in a 
separate list. 
Duplicates are deduplicated on only one field, imdb id of the search
result. This script also provides a interactive menu of each duplicate,
allowing you to choose which files to keep. To make it easier,
It automatically attempts to choose largest file from the list so
you don't have to do it manually.

The result is a json segregating movies into 4 categories, 
- delete
- keep
- undecided
- duplicate

Can easily use above result to do all necessary operations.
       
Special thanks to 
- [GuessIt](https://guessit.readthedocs.io/en/latest/) For the amazing work it does
- [ImdbPy](https://imdbpy.github.io/) For a simple, easy-to-use library around IMDb 
       

```
Sample command that gives json output of folder:

tree -J -a -f -s --du

Sample output:
[{"type":"directory","name": ".","contents":[
    {"type":"file","name":"./README.md","size":458},
    {"type":"file","name":"./basic_menu_example.py","size":469},
    {"type":"directory","name":"./bms-bot","size":3501,"contents":[
      {"type":"file","name":"./bms-bot/test.py","size":3405}
    ]},
    {"type":"directory","name":"./curses_modules","size":21245,"contents":[
      {"type":"file","name":"./curses_modules/basic_menu.py","size":8127},
      {"type":"file","name":"./curses_modules/basic_menu_driver.py","size":1170},
      {"type":"file","name":"./curses_modules/filtering_menu.py","size":9963},
      {"type":"file","name":"./curses_modules/filtering_menu_driver.py","size":1793}
    ]},
    {"type":"file","name":"./filtered_menu_example.py","size":542},
    {"type":"directory","name":"./tree-output-parser","size":160,"contents":[
      {"type":"file","name":"./tree-output-parser/README.md","size":64}
    ]}
  ]},
  {"type":"report","size":26695,"directories":3,"files":9}
]
```