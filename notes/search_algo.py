import os

from whoosh import index
from whoosh import qparser
from whoosh.analysis import StandardAnalyzer
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import *


def create_index():
    schema = Schema(href=ID(stored=True),
                    title=TEXT(field_boost=2.0, stored=True),
                    page_content=TEXT(stored=True))
    if not os.path.exists("index_dir"):
        os.mkdir("index_dir")
        ix = index.create_in("index_dir", schema)
    dirr = os.path.normpath('search/wiki_data')
    for subdir, dirs, files in os.walk(dirr):
        for file in files:
            if file.endswith(".txt"):
                f = open(os.path.join(subdir, file), 'r')
                # print ("https://en.wikibooks.org/wiki/Java_Programming/"+file[:-4].replace("-",".").replace("^","/"))
                link = "https://en.wikibooks.org/wiki/Java_Programming/" + file[:-4].replace("-", ".").replace("^", "/")
                mydata = f.read()
                ix = index.open_dir("index_dir")
                w = ix.writer()
                w.add_document(href=link, title=str(file[:-4].replace("-", ".").replace("^", ":")),
                               page_content=str(mydata))
                # print(mydata)
                f.close()
                w.commit()


def query(my_query):
    schema = Schema(href=ID(stored=True),
                    title=TEXT(field_boost=2.0, stored=True),
                    page_content=TEXT(analyzer=StemmingAnalyzer(), stored=True))

    ix = index.open_dir("index_dir")

    # qp = QueryParser("page_content", schema=ix.schema)
    mparser = qparser.MultifieldParser(["title", "page_content"], schema=schema, group=qparser.OrGroup)
    my_query_new = ""
    ff_q=[]
    final_my_query_new=""
    analyzer = StandardAnalyzer()
    for t in analyzer(my_query):
        # print(t.text)
        my_query_new += " " + str(t.text)
        ff_q.append(str(t.text))
    my_stop_words = ["when","http", "all", "but","how","so","which", "has","is","it","do","than","some","what","was","class","my","there","both"
                     "would","even"]
    for words in ff_q:
        if words not in my_stop_words:
            (words)
            final_my_query_new +=" "+str(words)
    q = mparser.parse(final_my_query_new)

    mparser.add_plugin(qparser.FuzzyTermPlugin())
    final_link = []
    final_highlights =[]
    with ix.searcher() as s:
        results = s.search(q, limit=10)
        results.fragmenter.surround = 50
        # print(results)
        for r in results:
            final_link.append(r['href'])
            final_highlights.append(str(r.highlights("page_content")))
    return final_link, final_highlights

#
# def search(request):
#     cur_dir = os.path.normpath('test_xlsx_file_here')
#
#     for sub_dir, dirs, files in os.walk(cur_dir):
#         for file in files:
#             if file.endswith(".xlsx") and not file.startswith("~"):
#                 name = os.path.join(sub_dir, file)
#                 wb = load_workbook(str(name))
#                 ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
#     type = []
#     text_code = []
#     for i in range(2, ws.max_row + 1):
#         temp = ""
#         if ws.cell(row=i, column=2).value != None:
#             temp = temp + str(ws.cell(row=i, column=2).value)
#         if ws.cell(row=i, column=3).value != None:
#             temp = temp + str(ws.cell(row=i, column=3).value)
#         type.append(str(ws.cell(row=i, column=1).value))
#         text_code.append(temp)
#     #create_index()
#     final_l1, final_h1 = query(text_code[0])
#     final_l2, final_h2 = query(text_code[1])
#     final_l3, final_h3 = query(text_code[2])
#     final_l4, final_h4 = query(text_code[3])
#     final_l5, final_h5 = query(text_code[4])
#     final_l6, final_h6 = query(text_code[5])
#     final_l7, final_h7 = query(text_code[6])
#     final_l8, final_h8 = query(text_code[7])
#     final_l9, final_h9 = query(text_code[8])
#     final_l10, final_h10 = query(text_code[9])
#
#
#     context = {
#         'type': type,
#         'text_code': text_code,
#         'final_link1': final_l1,
#         'final_link2': final_l2,
#         'final_link3': final_l3,
#         'final_link4': final_l4,
#         'final_link5': final_l5,
#         'final_link6': final_l6,
#         'final_link7': final_l7,
#         'final_link8': final_l8,
#         'final_link9': final_l9,
#         'final_link10': final_l10,
#         'final_h1': final_h1,
#         'final_h2': final_h2,
#         'final_h3': final_h3,
#         'final_h4': final_h4,
#         'final_h5': final_h5,
#         'final_h6': final_h6,
#         'final_h7': final_h7,
#         'final_h8': final_h8,
#         'final_h9': final_h9,
#         'final_h10': final_h10,
#
#     }
#     return render(request, 'index.html', context)