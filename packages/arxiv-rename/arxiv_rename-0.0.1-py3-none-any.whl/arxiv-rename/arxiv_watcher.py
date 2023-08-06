import re
import sys
import time
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
from arxiv_rename import arxivRename

CATEGORIES = [
    "acc-phys", "adap-org", "alg-geom", "ao-sci", "astro-ph", "atom-ph",
    "bayes-an", "chao-dyn", "chem-ph", "cmp-lg", "comp-gas", "cond-mat", "cs",
    "dg-ga", "funct-an", "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th",
    "math", "math-ph", "mtrl-th", "nlin", "nucl-ex", "nucl-th", "patt-sol",
    "physics", "plasm-ph", "q-alg", "q-bio", "quant-ph", "solv-int",
    "supr-con", "eess", "econ", "q-fin", "stat"
]

#  All subcategories with more than 2 capital letters (not SG, SI, SP, etc)
SUB_CATEGORIES = [
    'acc-ph', 'ao-ph', 'app-ph', 'atm-clus', 'atom-ph', 'bio-ph', 'chem-ph',
    'class-ph', 'comp-ph', 'data-an', 'dis-nn', 'ed-ph', 'flu-dyn', 'gen-ph',
    'geo-ph', 'hist-ph', 'ins-det', 'med-ph', 'mes-hall', 'mtrl-sci', 'optics',
    'other', 'plasm-ph', 'pop-ph', 'quant-gas', 'soc-ph', 'soft', 'space-ph',
    'stat-mech', 'str-el', 'supr-con'
]

# A common typo is to exclude the hyphen in the category.
categories = list(set(CATEGORIES + [cat.replace('-', '') for cat in
                                    CATEGORIES]))
subcategories = list(set(SUB_CATEGORIES + [cat.replace('-', '') for cat in
                                           SUB_CATEGORIES]))

RE_CATEGORIES = r'(?:{})(?:(?:[.][A-Z]{{2}})|(?:{}))?'.format(
    r'|'.join(categories), r'|'.join(subcategories)
)

RE_DATE = r'(?:(?:[0-2][0-9])|(?:9[1-9]))(?:0[1-9]|1[0-2])'
RE_VERSION = r'(?:[vV][1-9]\d*)?'

RE_NUM_NEW = RE_DATE + r'(?:[.]\d{4,5})' + RE_VERSION
RE_NUM_OLD = RE_DATE + r'(?:\d{3})' + RE_VERSION

# matches: 1612.00001 1203.0023v2
RE_ID_NEW = r'(?:{}).pdf$'.format(RE_NUM_NEW)

# matches: hep-th/11030234 cs/0112345v2 cs.AI/0112345v2
RE_ID_OLD = r'(?:{}/{}).pdf$'.format(RE_CATEGORIES, RE_NUM_OLD)


class MyHandler(RegexMatchingEventHandler):
    def on_moved(self, event):
        # print(event)
        arxivreg = re.compile(RE_ID_NEW + r'|' + RE_ID_OLD)
        if not (arxivreg.search(event.dest_path)):
            return
        arxivRename(event.dest_path)
        return

    def on_created(self, event):
        arxivreg = re.compile(RE_ID_NEW + r'|' + RE_ID_OLD)
        # print(event)
        if not (arxivreg.search(event.src_path)):
            return
        arxivRename(event.src_path)
        return


if __name__ == "__main__":
    # pattern = RE_ID_NEW + r'|' + RE_ID_OLD
    # # pattern = '.'

    # r = re.compile(pattern)
    # print(r.search("./1503.06237.pdf"))

    # print(RE_ID_NEW + r'|' + RE_ID_OLD)

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler(ignore_directories=True, case_sensitive=False)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
