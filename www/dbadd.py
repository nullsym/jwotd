#!/usr/bin/env python

from sachiye import db
from sachiye.models import Wotd
import argparse



parser = argparse.ArgumentParser(description='Add a WOTD to the database')
parser.add_argument("-w", "--wotd")
parser.add_argument("-r", "--romaji")
parser.add_argument("-d", "--definition")
args = parser.parse_args()

# print("Wotd: " + str(args.wotd))
# print("Romaji: " + str(args.romaji))
# print("Def: " + str(args.definition))

tmp = Wotd(wotd=args.wotd, romaji=args.romaji, defn=args.definition)
db.session.add(tmp)
db.session.commit()