class Pronoun():

    def __init__(self):
        self._pronoun = {
                "1ps_sg": ['yo'],
                "2ps_sg": ['tú'],
                "3ps_sg": ['él', 'ella', 'usted'],
                "1ps_pl": ['nosotros', 'nosotras'],
                "2ps_pl": ['vosotros', 'vosotras'],
                "3ps_pl": ['ellos', 'ellas', 'ustedes'],
            }

    def get_pronoun_key(self, phrase: str) -> str:
        """Get respondign key for a pronoun if phrase is a pronoun

        Args:
            phrase (str): Pronoun

        Returns:
            str: Pronoun key
        """
        key_list = list(self._pronoun.keys())

        pronoun_key = None
        for key in key_list:
            for element in self._pronoun[key]:
                if element in phrase and len(phrase) <= len(element)+2:
                    pronoun_key = key
                    break
            if pronoun_key is not None:
                break

        return pronoun_key
