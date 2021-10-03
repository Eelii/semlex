from .subparagraph import Subparagraph

class Paragraph:

    def __init__(self, json_dict):
        assert type(json_dict) == dict
        self.json_dict = json_dict
        self.subparagraphs = []
        self.paragraphID = None
        self.paragraphType = None
        self.isMemberOf = None
        self.version = None
        self.text = None
        self.id_str = self.json_dict.get("@id")
        self.versionDate = self.json_dict.get("versionDate")

        if self.json_dict.get("@type") == "sfl:PreambleVersion":
            self.is_preamble = True
            self.is_final_paragraph = False
        elif self.json_dict.get("@type") == "sfl:FinalParagraphVersion":
            self.is_final_paragraph = True
            self.is_preamble = False
        else:
            assert self.json_dict.get("@type") == "sfl:ParagraphVersion", f"Json type {self.json_dict.get('@type')} not recognized."
            self.is_preamble = False
            self.is_final_paragraph = False

        # TODO self.version
        if self.json_dict.get("hasPart"):
            subparagraph_iterable = self.json_dict.get("hasPart")

            if isinstance(subparagraph_iterable, list):
                for list_item in subparagraph_iterable:
                    assert(isinstance(list_item, dict) == True)
                    new_subparagraph = Subparagraph(list_item)
                    self.subparagraphs.append(new_subparagraph)

            elif isinstance(subparagraph_iterable, dict):
                new_subparagraph = Subparagraph(subparagraph_iterable)
                self.subparagraphs.append(new_subparagraph)

            else:
                raise Exception("Unknown type of subparagraph_iterable")

        elif self.json_dict.get("languageVersion") != None:
            self.text = self.json_dict.get("languageVersion").get("hasFormat").get("content_fi")

        if self.text == None and len(self.subparagraphs) == 0:

            raise Exception(f"No text or subparagraphs in paragraph: {self.id_str}")
        
        if self.text == "":
            raise Exception(self.json_dict)

        self.fix_subparagraphs()
    
    #624/2006 25:1 missing 2nd subsection
    #---------------------------------------------------
    def fix_subparagraphs(self):
        if len(self.subparagraphs) >= 2:
            index = 1
            while index < len(self.subparagraphs):
                subpar1 = self.subparagraphs[index-1]
                subpar2 = self.subparagraphs[index]
                if subpar1.text == subpar2.text:
                    self.subparagraphs.pop(index)
                index += 1 
    #---------------------------------------------------
    def get_text_content(self):
        txt = ""
        if len(self.subparagraphs) > 0:
            for subparagraph in self.subparagraphs:
                txt += subparagraph.get_text_content() + "\n"
        elif self.text != None:
            txt += self.text 
        else:
            txt = "NO CONTENT"

        return txt