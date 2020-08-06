class EducationCorpusMixin():
    def set_education(self, name: str):
        """Set Corpus' instance education by its name and check beforehand

        Args:
            name (str): Name of the education the corpus should be filtered on
        """
        education_list = self._feature_dict['Education']
        if name in education_list:
            self._education = name
        elif name == "all":
            self._education = "all"
        else:
            Warning('Education definition not in accordance with corpus')
            self._education = ""

    def __str__(self):
        return "education:{}".format(self._education)
