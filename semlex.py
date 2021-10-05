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

    #print_statute(args.num, args.year)

