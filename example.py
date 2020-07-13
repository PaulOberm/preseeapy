from preseeapy.CorpusPreseea import PRESEEA

# Get a PRESEEA instance
corpus_preseea = PRESEEA()

# Western andalusian wave model cities:
wave_model_city_list = ["Sevilla", "Córdoba", "Huelva", "Málaga", "Cádiz"]

for city in wave_model_city_list:
    # Define search issue with filters and phrase
    filter_name = corpus_preseea.set_filter(city=city,
                                            gender="all",  # "Hombre",
                                            age="all",  # "Grupo 1",
                                            education="all",  # "Bajo",
                                            phrase='vosotros ')

    # Get data via scrapy framework as API
    sample_list = corpus_preseea.retrieve_phrase_data()

    meta_data = corpus_preseea.analyse()

    # Write data with stats into .csv file
    corpus_preseea.write_csv(data=sample_list,
                             file_name="{}.csv".format(filter_name))

    print(filter_name)
