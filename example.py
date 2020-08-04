from preseeapy.CorpusPreseea import PRESEEA

# Get a PRESEEA instance
corpus_preseea = PRESEEA(author='Obermayer Paul')

# Western andalusian wave model cities:
wave_model_city_list = ["Sevilla", "Córdoba", "Huelva", "Málaga", "Cádiz"]
wave_model_city_list = ["Madrid"]
phrase_list = ['ustedes ', 'vosotros ']

for city in wave_model_city_list:
    for phrase in phrase_list:
        corpus_preseea.create_report(city=city, phrase=phrase)
