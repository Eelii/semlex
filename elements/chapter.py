import re
from .section import Section

class Chapter:

    def __init__(self, json_dict):
        assert type(json_dict) == dict
        assert json_dict.get("@type") == "sfl:ChapterVersion"
        self.json_dict = json_dict
        self.id_str = None
        self.title = None
        self.num = None
        self.versionDate = None
        self.sections = []

        try:
            self.title = self.json_dict.get("languageVersion").get("title_fi")
        except:
            pass

        self.versionDate = self.json_dict.get("versionDate")
        self.id_str = json_dict.get("@id")
        parsed = re.findall(r"luku/\d\d*[a-z]*", self.id_str)
        assert len(parsed) <= 3
        parsedAndSplit = parsed[0].split("/")
        self.num = parsedAndSplit[1]
    
    def create_sections(self):
        sections_lst = self.json_dict.get("hasPart")

        for section_dict in sections_lst:
            if type(section_dict) == dict and section_dict.get("@type") == "sfl:SectionVersion":
                newSection = Section(section_dict)
                self.sections.append(newSection)

    def get_sections_count(self):
        count = 0
        for section in self.sections:
            if section.is_subheading != True:
                count += 1
        return count