import json
import requests
from .section import Section
from .part import Part
from .chapter import Chapter 
from .enacting_clause import Enacting_clause

class Statute:
    json_str = None
    url = None
    statuteID = None
    title = None
    has_parts = None 
    parts = []
    has_chapters = None
    chapters = []
    enacting_clause = None
    sections = None
    numOfSections = None
    documentDate = None
    documentType = None
    version = None 
    versionDate = None

    def __init__(self, num, year, xml=False):

        if xml == True:
            pass
        else:
            self.url = createUrl(num, year)
            self.json_str = getJsonStr(self.url)
            if self.json_str != False:
                self.get_body()

            if self.has_parts:
                self.create_parts()

            if self.has_chapters:
                self.create_chapters()
                for chapter in self.chapters:
                    chapter.create_sections()
            else:
                self.create_sections()

        """self.statuteID = getStatuteID(self.json_str)
        self.numOfSections = getStatuteNumOfSections(self.json)
        self.documentDate = getStatuteDocumentDate(self.json)
        self.documentType = getStatuteDocumentType(self.json)
        #self.version = self.getVersion()
        self.title = getStatuteTitle(self.json)"""

    def get_body(self):
        json_dic = json.loads(self.json_str)
        first_layer = json_dic.get("temporalVersion").get("hasPart")
        sfl_types = get_sfl_types()
        layer_types = []

        if first_layer != None:
            for part in first_layer:
                part_type = part.get("@type") 
                if part_type in sfl_types:
                    part_type = sfl_types[part_type]
                layer_types.append(part_type)

        if "Encating Clause" in layer_types:
            pass
            #self.enacting_clause = Enacting_clause()
        else:
            self.enacting_clause = False
        
        if "Part" in layer_types:
            self.has_parts = True
        else:
            self.has_parts = False

        if "Chapter" in layer_types:
            self.has_chapters = True
        else:
            self.has_chapters = False

    def create_parts(self):
        json_dict = json.loads(self.json_str)

        if self.enacting_clause == None:
            parts_layer = json_dict.get("temporalVersion").get("hasPart")

        elif self.enacting_clause != None:
            parts_layer = json_dict.get("temporalVersion").get("hasPart")[1:]

        for part in parts_layer:

                if part.get("@type") == "sfl:ChapterVersion":
                    pass #TODO 588/2013
                
                else:
                    assert part.get("@type") == "sfl:PartVersion"    
                    new_part = Part(part)
                    self.parts.append(new_part)

        a_part = json_dict.get("temporalVersion").get("hasPart")[1]
        possible_chapter = a_part.get("hasPart")[1]

        if possible_chapter.get("@type") == "sfl:ChapterVersion":
            self.has_chapters = True
        else:
            self.has_chapters = False

    def create_chapters(self):

        assert(self.has_chapters ==  True)
        json_dict = json.loads(self.json_str)
        chapters_layers = []

        if self.enacting_clause == None:
            layer = json_dict.get("temporalVersion").get("hasPart")

        elif self.enacting_clause != None:
            layer = json_dict.get("temporalVersion").get("hasPart")[1:]

        if self.has_parts == True:
            for part_layer in layer:
                for chapter_layer in part_layer.get("hasPart"):
                    if type(chapter_layer) == str:
                        pass
                    else:
                        assert chapter_layer.get("@type") == "sfl:ChapterVersion"
                        chapters_layers.append(chapter_layer)

        elif self.has_parts == False:
            if isinstance(layer, dict):
                for chapter_layer in layer.get("hasPart"):
                        if type(chapter_layer) == str:
                            pass
                        else:
                            assert chapter_layer.get("@type") == "sfl:ChapterVersion"
                            chapters_layers.append(chapter_layer)

            elif isinstance(layer, list):
                for chapter_layer in layer:
                        if type(chapter_layer) == str:
                            pass
                        elif chapter_layer.get("@type") == ("sfl:SectionVersion"):
                            pass #TODO 228/1929
                        else:
                            assert chapter_layer.get("@type") == "sfl:ChapterVersion"
                            chapters_layers.append(chapter_layer)

        else:
            raise Exception("Statute.has_parts == None")

        
        for chapter_json in chapters_layers:
            new_chapter = Chapter(chapter_json)
            self.chapters.append(new_chapter)

    def create_sections(self):
        pass

    def create_encating_clause(self, enactingJson):
        version = self.get_version(enactingJson.get("version"))
        versionDate = enactingJson.get("versionDate")
        text = enactingJson.get("languageVersion").get("hasFormat").get("content_fi")
        self.enacting_clause = Enacting_clause(version, versionDate, text)
    
    def get_version(self, json):   
        #TODO
        #assert (self.json.get("temporalVersion").get("@type") == "sfl:StatuteVersion")
        sfl = self.json.get("temporalVersion").get("hasPart").get("versionDate")
        if sfl == "sfl:Original":
            return "original"
        elif sfl == "sfl:Consolidated":
            return "consolidated"
        else:
            return "unknown"

        """if sections[0]:
            return sections
        else:
            for s in sections:
                print(s)"""

    def printInfo(self):
        print(self.title)
        print("--------------------------------------")
        print(f"Säädöksen nimi: {str(self.title)}")
        print(f"Säädöksen tunnus: {str(self.statuteID)}")
        print(f"Säädöksen tyyppi: {str(self.documentType)}")
        print(f"Säädösdokumentin päiväys: {str(self.documentDate)}")
        print(f"Lukuja: {str(len(self.chapters))}")
        if (self.has_chapters == False):
            print(f"Pykälien määrä: {str(self.numOfSections)}")
        #elif (self.has_chapters(True)): #TODO

    def printAll(self):
        self.printInfo()
        print("\n\n")

        if self.has_chapters == True:
            for chapter in self.chapters:
                for section in chapter.sections:
                    print(section.title+"\n")
                    for subsection in section.subsections:
                        print(subsection.text)
                        for paragraph in subsection.paragraphs:
                            print(paragraph.text)
        else:
            for section in self.sections:
                    print(section.title+"\n")
                    for subsection in section.subsections:
                        print(subsection.text)
                        for paragraph in subsection.paragraphs:
                            print(paragraph.text)


#----------------------------------------------------------------------------------#

def createUrl(idnum, year):
    url = 'http://data.finlex.fi/eli/sd/{0}/{1}?pretty&tree'.format(str(year),str(idnum))
    return url

def getJsonStr(url):
    payload = {"Accept":"application/ld+json"}
    r = requests.get(url, allow_redirects=True, headers = payload)
    if (r.status_code == 200):
        if (len(r.text) > 950):
            return r.text
        else:
            return False
    else:
        return False

def getJsonDic(jsonStr):
    jsonDic = json.loads(jsonStr)
    return jsonDic

def get_sfl_types():
    sfls = {
        "sfl:StatuteVersion":"Statute",
        "sfl:PartVersion":"Part",
        "sfl:ChapterVersion":"Chapter",
        "sfl:EnactingClauseVersion":"Enacting Clause",
        "sfl:SubheadingVersion":"Subheading",
        "sfl:SectionVersion":"Section",
        "sfl:SubsectionVersion":"Subsection",
        "sfl:ParagraphVersion":"Paragraph",
        "sfl:SubparagraphVersion":"Subparagraph",
        "sfl:AttachmentVersion":"Attachment"}
        #xsd:date?
    return sfls
