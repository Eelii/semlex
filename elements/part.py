class Part:

    def __init__(self, json_dict):
        self.json_dict = json_dict
        self.version_type = self.json_dict.get("version")
        self.version_date = self.json_dict.get("versionDate")
        self.title = self.json_dict.get("languageVersion").get("title_fi")