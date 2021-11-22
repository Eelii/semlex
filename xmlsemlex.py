import xml.etree.ElementTree as ET
import os
import random
import re

class StatuteElement:

    def __init__(self):
        pass 
    
    def get_elements(self, name):
        elements = []
        for element in self.tree_root.iter():
            if self.trim_tag(element.tag) == get_tags().get(name):
                elements.append(element)
        return elements

    def trim_tag(self, tag):
        tag = tag.split("}")
        if len(tag) > 1:
            tag = tag[1]
            return tag
        else:
            return False

    def get_xml_tags(self, unique=False):
        tags = []

        for element in self.tree_root.iter():
            tag = element.tag
            tag = self.trim_tag(tag)
            tags.append(tag)

        if unique == True:
            tags = set(tags)
        return tags


class Statute(StatuteElement):

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.tree = ET.parse(path)
        self.tree_root = self.tree.getroot()
        self.name = self.get_name()
        self.number = self.get_number()
        self.year = self.get_year()
        self.part_elements = self.get_elements("part")
        self.chapter_elements = self.get_elements("chapter")
        self.section_elements = self.get_elements("section")

        self.parts = []
        
        if len(self.part_elements) > 0:
            for part_elem in part_elements:
                self.parts.append(Part(part_elem))
        
        self.chapters = []

        if len(self.chapter_elements) > 0:
            for chapter_elem in self.chapter_elements:
                self.chapters.append(Chapter(chapter_elem))

        self.sections = []
        
        if len(self.part_elements) == 0 and len(self.chapter_elements) == 0:
            for section_elem in self.section_elements:
                self.sections.append(Section(section_elem))

    def get_name(self):
        name = ""
        document_type = ""
        for element in self.tree_root.iter():
            if self.trim_tag(element.tag) == get_tags().get("statute_name"):
                name = element.text
            if self.trim_tag(element.tag) == get_tags().get("statute"):
                for key, item in element.attrib.items():
                    if "saadostyyppiNimi" in key:
                        document_type = item
        return f"{document_type} {name}"

    def get_number(self):
        number_elem = self.get_elements("document_number")
        assert(len(number_elem) == 1)
        number = number_elem[0].text
        return number
            
    def get_year(self):
        year_elem = self.get_elements("document_year")
        assert(len(year_elem) == 1)
        year = year_elem[0].text
        return year

    def get_text_content(self):
        
        text_content = ""
        if len(self.parts) > 0:
            for part in self.parts:
                text_content += part.get_text_content()
        else:
            for section in self.sections:
                if section.get_text_content() != None:
                    text_content += section.get_text_content()
        return text_content
    
    def print_info(self):

        print(f"Number: {self.number}")
        print(f"Year: {self.year}")
        print(f"Name: {self.name}")

class Part(StatuteElement):

    def __init__(self, part_tree):
        super().__init__()
        self.tree_root = part_tree
        self.chapter_elements = self.get_elements("chapter")
        
        self.chapters = []
        if len(self.chapter_elements) > 0:
            for chapter_elem in self.chapter_elements:
                self.chapters.append(Chapter(chapter_elem))

    def get_text_content(self):
        for chapter in self.chapters:
            print("TODO")

class Chapter(StatuteElement):

    def __init__(self, chapter_tree):
        super().__init__()
        self.tree_root = chapter_tree
        self.section_elements = self.get_elements("section")

        self.sections = []
        if len(self.section_elements) > 0:
            for section_elem in self.section_elements:
                self.sections.append(Section(section_elem))

class Section(StatuteElement):

    def __init__(self, section_tree):
        super().__init__()
        self.tree_root = section_tree
        self.subsection_elements = []
        self.subsection_elements += self.get_elements("subsection_text_only")
        self.subsection_elements += self.get_elements("subsection_with_paragraphs")

        self.subsections = []
        if len(self.subsection_elements) > 0:
            for subsection_elem in self.subsection_elements:
                self.subsections.append(Subsection(subsection_elem))

    def get_text_content(self):
        for subsection in self.subsections:
            return subsection.get_text_content()



class Subsection(StatuteElement):

    def __init__(self, subsection_element):
        super().__init__()
        self.elem = subsection_element
        self.tree_root = subsection_element
        self.text = "SUBSECTION: NO CONTENT"
        self.paragraphs = []

        if self.elem.text != None and len(self.elem.text) > 0:
            self.text = self.elem.text
            
        else:
            para_elems = self.get_elements("paragraphs")
            assert len(para_elems > 0)
            for para_elem in para_elems:
                new_paragraph = Paragraph(para_elem)
                self.paragraphs.append(new_paragraph)

    def get_text_content(self):

        if len(self.text) > 0:
            return "\n\n" + self.text
        else:
            assert len(self.paragraphs) > 0
            for paragraph in self.paragraphs:
                paragraph.get_text_content

class Paragraph(StatuteElement):

    def __init__(self, paragraph_element):
        super().__init__()
        self.paragraph_element = paragraph_element
        self.tree_root = paragraph_element
        self.text = "PARAGRAPH: NO CONTENT"
        
        if self.trim_tag(self.paragraph_element.tag) == get_tags().get("paragraph_preamble_text"):
            self.is_preamble = True
            self.text = self.paragraph_element.text
        else:
            assert self.trim_tag(self.paragraph_element.tag) == get_tags().get("paragraph_text"), f"{self.paragraph_element.tag} not recognized"
            self.is_preamble = False
            self.text = self.paragraph_element.text

    def get_text_content():
        if len(self.text) > 0:
            return "\n\n" + self.text
        else:
            return ""

def create_random_statute():
    new_statute = Statute(get_random_xml_path())
    return new_statute

def get_random_xml_path():
    filePaths = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if ("pyxml.py" in name):
                continue
            else:
                filePaths.append(os.path.join(root, name))
    randomFile = filePaths[random.randint(0, len(filePaths)-1)]
    return randomFile

def print_things():
    stat = create_random_statute()
    print(stat.get_text_content())
    stat.print_info()


def get_tags(with_namespaces=False):

    tags_with_namespaces = {
        "document_type":"met1:AsiakirjatyyppiNimi",
        "document_number":"asi1:AsiakirjaNroTeksti",
        "document_year":"asi1:ValtiopaivavuosiTeksti",
        "document_reference":"sis1:ViiteTeksti",
        "statute":"saa:Saados",
        "statute_name":"met1:NimekeTeksti",
        "part":"saa:Osa",
        "part_id_text":"saa:OsaTunnusKooste",
        "chapter":"saa:Luku",
        "chapter_id_text":"saa:LukuTunnusKooste",
        "section":"saa:Pykala",
        "section_id_text":"saa:PykalaTunnusKooste",
        "section_heading":"saa:SaadosOtsikkoKooste",
        "section_subheading":"saa:SaadosValiotsikkoKooste",
        "subsection_text_only":"saa:MomenttiKooste",
        "subsection_with_paragraphs":"saa:KohdatMomentti",
        "paragraphs":"saa:KohdatMomentti",
        "paragraph_text":"saa:MomenttiKohtaKooste",
        "paragraph_preamble_text":"saa:MomenttiJohdantoKooste"
    }


    if with_namespaces == True:
        return tags_with_namespaces
    else:
        tags = {}
        for key, item in tags_with_namespaces.items():
            tags[key] = item.split(":")[1]
        return tags


print_things()





"""for section_elem in stat.section_elements:
    for i in section_elem.iter():
        print(i)"""
"""
for i in stat.tree_root.iter():
    print(i)"""