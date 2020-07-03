from CorpusPreseea import PRESEEA

# Get a PRESEEA instance
corpus_preseea = PRESEEA()

# Define search issue with filters and phrase
corpus_preseea.set_filter(city="Pereira", gender="male",
                          age="young", education="low")
corpus_preseea.set_search_phrase('le ')

# Get data via scrapy framework as API
test_list = corpus_preseea.retrieve_phrase_data()

# Write data with stats into .csv file
corpus_preseea.write_csv(data=test_list, file_name="example.csv")
