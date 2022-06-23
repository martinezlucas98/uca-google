# Latest improvements
- New Language Support: English.

- Improve Spanish Detection.
- Improve performance in some modules like lemmatization, stemming, tokenizer and lang_detect. Loading heavy objects into memory only once when starting the service and not every time these modules are used.
- Two new Api Routes:<br>
<span style="margin-left: 10px">
    <b>/autocomplete</b>:  returns the same autocomplete options that google scholar returns.
</span><br>
<span style="margin-left: 10px">
    <b>/lemmastemm</b>:  A 'lighter' and faster version of <b>/expand_query</b>, which returns only the language, lammatization and stemming.
</span>

<br>

# Issues
- The New Lang_detect2 module is more precise when detecting the Spanish language but it increases the response time quite a bit

- Most of the modules that have  <b>/expand_query</b> and <b>/lemmastemm</b> in common have a pretty good performance (between 1 to 5 ms), while the <b>lemmatization</b> module takes between 40ms to 200ms, so it would be nice to improve the lemmatization time.

- The <b>classification</b> module Sometimes does not return the desired value, since the data set is minimal, that is, it contains very few words, more words need to be added in order to give greater results.
Example for the argument "schedules" the classification "bus" is returned which may make sense but if we ask for "class schedules" it returns "dress clothes"

# Ideas for future development
- Work with the index service to get autocomplete answers based on the UC Google environment.
- Save autocomplete history.
- Build Machine Learning models to classify the query.

