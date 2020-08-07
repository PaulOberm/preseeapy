class GenderCorpusMixin():
    def set_gender(self, name: str):
        """Set Corpus' instance gender by its name and check beforehand

        Args:
            name (str): Name of the gender the corpus should be filtered on
        """
        gender_list = self._feature_dict['Gender']
        if name in gender_list:
            self._gender = name
        elif name == "all":
            self._gender = "all"
        else:
            Warning('Gender not in accordance with corpus')
            self._gender = ""

    def __str__(self):
        return "gender_{}".format(self._gender)
