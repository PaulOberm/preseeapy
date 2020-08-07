class AgeCorpusMixin():
    # def __init__(self):
    #     self._age = ""

    def set_age(self, name: str):
        """Set Corpus' instance age by its name and check beforehand

        Args:
            name (str): Name of the age the corpus should be filtered on
        """
        age_list = self._feature_dict['Age']
        if name in age_list:
            self._age = name
        elif name == "all":
            self._age = "all"
        else:
            Warning('Age definition not in accordance with corpus')
            self._age = ""

    def __str__(self):
        return "age_{}".format(self._age)
