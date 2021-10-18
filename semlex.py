import os
import xml.etree.ElementTree as ET
from random import randrange
from elements import statute
Statute = statute.Statute



def get_statute_string(num=756, year=2011):
    schema = "http://data.finlex.fi/schema/sfl/"
    #s = Statute(39, 1889)
    s = Statute(num, year) 
    printed = ""
    if s != False:
        for chapter in s.chapters:
            for section in chapter.sections:
                printed += section.get_text_content()

        if printed == "":
            return False
        else:
            return printed
    else:
        return False

def list_all_file_paths():
    file_paths = []
    files_to_ignore = [] 
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name in files_to_ignore:
                continue
            else:
                file_paths.append(os.path.join(root, name))
    return file_paths

def list_all_dir_paths():
    dirPaths = []
    dirs_to_ignore = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            if name in dirs_to_ignore:
                continue
            else:
                dirPaths.append(os.path.join(root, name))
    return dirPaths

def get_xml_folder_names():
    cwd = os.getcwd()
    dir_names = []
    xml_folders_path = os.path.join(cwd,"xml")
    for dirname, dirnames, filenames in os.walk(xml_folders_path):
        for subdirname in dirnames:
            dir_names.append(subdirname)
    return dir_names

def get_xml_folder_paths():
    stat_years = get_xml_folder_names()
    assert len(stat_years) > 0 
    folder_paths = [] 
    xml_folders_path = os.path.join(os.getcwd(), "xml")
    stat_year_folder_paths = []

    for folder_name in stat_years:
        path = os.path.join(xml_folders_path, folder_name)
        stat_year_folder_paths.append(path)
    return stat_year_folder_paths

def get_xml_file_paths():
    file_paths = []
    xml_folder_paths = get_xml_folder_paths()

    for xml_folder_path in xml_folder_paths:
        for dirname, dirnames, filenames in os.walk(xml_folder_path):
            for filename in filenames:
                if filename != None:
                    file_path = os.path.join(xml_folder_path, filename)
                    file_paths.append(file_path)
    return file_paths

def get_ElementTree(xml_path):
    tree = ET.parse(xml_path)
    return tree


"""
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", help="Säädösnumeron vuosi-osa", metavar="year", type=int)
    parser.add_argument("--num", help="Säädösnumero numero-osa", metavar="num", type=int)
    args = parser.parse_args()

    if args.num != None and args.year != None:
        stat_str = get_statute_string(num=args.num, year=args.year)
        if stat_str == False:
             print(f"Säädösnumerolla {args.num}/{args.year} ei löytynyt säädöstä.")
        else:
            print(stat_str)

    elif args.num != None and args.year == None:
        stat_str = False
        print(f"Etsitään satunnaista säädöstä {args.num}/X ...")
        while stat_str == False:
            random_year = randrange(1889,2021,1)
            stat_str = get_statute_string(num=args.num, year=random_year)
        print(stat_str)

    elif args.num == None and args.year != None:
        stat_str = False
        print(f"Etsitään satunnaista säädöstä X/{args.year} ...")
        while stat_str == False:
            random_num = randrange(0,3000,1)
            stat_str = get_statute_string(num=random_num, year=args.year)
        print(stat_str)
    
    elif args.num == None and args.year == None:
        stat_str = False
        print("Etsitään satunnaista säädöstä...")
        while stat_str == False:
            random_year = randrange(1889,2021,1)
            random_num = randrange(0,3000,1)
            stat_str = get_statute_string(num=random_num, year=random_year)
    print(stat_str)
"""
file_paths = get_xml_file_paths()
file_path = file_paths[100]
tree = get_ElementTree(file_path)
root = tree.getroot()

print(root)