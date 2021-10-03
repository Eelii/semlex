from elements import statute
Statute = statute.Statute

def testCreate():
    schema = "http://data.finlex.fi/schema/sfl/"
    #s = Statute(39, 1889)
    s = Statute(39, 1889) 
    s.printInfo()
    for chapter in s.chapters:
        for section in chapter.sections:
            print(section.get_text_content())
            #print(len(section.subsections))
testCreate()