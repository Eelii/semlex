class Subparagraph:
    
    # TODO RL 51:3 - wrong order!
    def __init__(self, json_dict):
        self.json_dict = json_dict
        self.versionDate = json_dict.get("versionDate")
        self.text = self.json_dict.get("languageVersion").get("hasFormat").get("content_fi")


    def get_text_content(self):
        return self.text