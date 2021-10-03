import re
from .subsection import Subsection


class Section:

    def __init__(self, json_dict):
        self.json_dict = json_dict
        self.id_str = self.json_dict.get("@id")
        self.versionDate = self.json_dict.get("versionDate")
        self.is_subheading = None
        self.num = None
        self.title = None
        self.subsections = []
        self.version = None
        self.urlID = None
        self.repealed_by = None 
        self.text = None
        self.parse_section_num()

        try:
            self.title = self.json_dict.get("languageVersion").get("title_fi")
        except:
            pass
        
        if self.json_dict.get("repealedBy") == None:
            self.repealed_by = False
        elif self.json_dict.get("repealedBy") != None:
            self.repealed_by = True
        else:
            raise Exception("Dfd")
        
        section_type = self.json_dict.get("@type")

        if section_type == "sfl:SubheadingVersion":
            is_subheading = True
        elif section_type == "sfl:SectionVersion":
            is_subheading = False
        else:
            raise Exception("Section type not found")

        if self.is_subheading == True:
            self.title = self.json_dict.get("languageVersion").get("hasFormat").get("content_fi")
        else:
            try:
                self.title = self.json_dict.get("languageVersion").get("title_fi")
            except:
                pass
        self.create_content()
        #----------------------------------------
    

        if self.id_str == "sfsd:2006/624/luku/25/pykala/1/ajantasa/20130101":
            #raise Exception(self.subsections)
            pass

    def create_content(self):

        subsection_iterable = self.json_dict.get("hasPart")
        if subsection_iterable != None:
            if isinstance(subsection_iterable, dict) == True : #and "momentti" in subsection_dict.get("@id")
                new_subsection = Subsection(subsection_iterable, repealed=self.repealed_by)
                self.subsections.append(new_subsection)

            elif isinstance(subsection_iterable, list) == True:
                for list_item in subsection_iterable:
                    assert(type(list_item)) == dict
                    new_subsection = Subsection(list_item)
                    self.subsections.append(new_subsection)
                    
            elif type(subsection_iterable) == str:
                pass

            else:
                #print(f"WHAT: {subsection_iterable}")
                #raise Exception(f"Unkown subsection type {subsections_dict}")
                raise Exception(type(subsection_iterable))

        elif subsection_iterable == None and self.json_dict.get("@type") == "sfl:SectionVersion":
            try:
                self.text = self.json_dict.get("languageVersion").get("hasFormat").get("content_fi")
            except:
                raise Exception(f"Error creating section content\nJSON: {self.json_dict}")

        elif subsection_iterable == None:
            assert(isinstance(self.json_dict, dict))
            assert self.json_dict.get("repealedBy")!=None, f"{self.json_dict}"
            assert(self.repealed_by != False)
            self.subsections.append(Subsection(self.json_dict, repealed=True))

        else:
            raise Exception(f"Error while testing if a subsection is repealed: {self.json_dict}")

    def parse_section_num(self):
        section_part = re.findall(r"pykala/+\d*./",self.id_str)
        if len(section_part) != 0:
            assert(len(section_part)) == 1
            section_part = section_part[0].replace("pykala","")
            num = section_part.replace("/","")
            self.num = num + " §"
    
    def get_text_content(self):
        txt = "\n"
        if self.num != None:
            txt += self.num 
        if self.title != None:
            txt += " " + self.title
        txt += "\n"
        for subsection in self.subsections:
            txt += "\n" + subsection.get_text_content()
    
        return txt