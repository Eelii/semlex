from .paragraph import Paragraph

class Subsection:

    def __init__(self, json, repealed=False):
        self.text = None
        self.paragraphs = []
        self.subsectionID = None
        self.version = None
        self.isMemberOf = None
        self.json = json
        self.id_str = self.json.get("@id")
        self.versionDate = self.json.get("versionDate")
        # TODO self.version = 

        if repealed == False:
            assert json.get("@type") == "sfl:SubsectionVersion"
            if self.json.get("hasPart") != None:
                paragraphs_list = self.json.get("hasPart")
                for paragraphJson in paragraphs_list:
                    if type(paragraphJson) == dict:
                        newParagraph = Paragraph(paragraphJson)
                        self.paragraphs.append(newParagraph)

            elif self.json.get("languageVersion") != None:
                self.text = json.get("languageVersion").get("hasFormat").get("content_fi")

            else:
                raise Exception("Error while creating a subsection")
        
        elif repealed == True:
            self.text = "KUMOTTU"
        
        else:
            raise Exception(repealed)
        
    def get_text_content(self):
        txt = ""
        if len(self.paragraphs) > 0:
            for paragraph in self.paragraphs:
                txt = txt + paragraph.get_text_content() + "\n"
        else:
            txt = f"{self.text}\n"
        return txt