import xml.etree.ElementTree as ET
import os
import random
import re


class Statute:

    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(path)
        self.tree_root = self.tree.getroot()
        self.has_parts = self.check_for_parts()
        self.has_chapters = self.check_for_chapters()
        self.name = self.get_name()
        self.number = self.get_number()
        self.year = self.get_year()
        self.part_elements = self.get_elements("part")
        self.chapter_elements = self.get_elements("chapter")
        self.section_elements = self.get_section_elements()
        
    
    def get_xml_tags(self, unique=False):
        tags = []

        for element in self.tree_root.iter():
            tag = element.tag
            tag = self.trim_tag(tag)
            tags.append(tag)

        if unique == True:
            tags = set(tags)
        return tags

    def check_for_parts(self):
        for element in self.tree_root.iter():
            if self.trim_tag(element.tag) == get_tags().get("part"):
                return True
        return False
    
    def check_for_chapters(self):
        for element in self.tree_root.iter():
            if self.trim_tag(element.tag) == get_tags().get("chapter"):
                return True
        return False

    def trim_tag(self, tag):
        tag = tag.split("}")
        if len(tag) > 1:
            tag = tag[1]
            return tag
        else:
            return False

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

    def get_section_elements(self):
        section_elements = []
        section_tag = get_tags().get("section")
        for element in self.tree_root.iter():
            if section_tag == self.trim_tag(element.tag) and ET.iselement(element) == True:
                section_elements.append(element)
            elif ET.iselement(element) == False:
                raise Exception(f"{self.get_section_elements}")
        return section_elements 
    
    def get_elements(self, name):
        elements = []
        for element in self.tree_root.iter():
            if self.trim_tag(element.tag) == get_tags().get(name):
                elements.append(element)
        return elements

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
        "subsection_text":"saa:MomenttiKooste",
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



stat = create_random_statute()
i = 0
while (stat.has_parts == False):
    i += 1
    stat = create_random_statute()
    print(i)

print(f"PARTS: {stat.has_parts}")
print(stat.has_chapters)
print(stat.name)
print(stat.number)
print(stat.year)
print(stat.part_elements)


"""for section_elem in stat.section_elements:
    for i in section_elem.iter():
        print(i)"""
"""
for i in stat.tree_root.iter():
    print(i)"""