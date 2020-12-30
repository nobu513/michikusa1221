from django.shortcuts import render, get_object_or_404, redirect
from .models import DocDData
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F
import re

def return_description(document, searchwords):
    
    description = ""
    rows = document.split("\n")
    
    # searchword_list = kkma.nouns(searchwords)
    searchword_list = searchwords.replace("　", " ").split(" ")[:-1]
    
    center_index = 0
    
    # まず、中心となる１文を見つけるためのデータを作る

    for index, row in enumerate(rows):
        
        # 完全一致の場合
        if searchwords in row:
            
            center_index = index
            
            #最初の文の場合 後の２文を取ってくる
            if center_index == 0:
                description += rows[0] + rows[1] + rows[2]

            #最後の文の場合　前の２文を取ってくる
            elif center_index == len(rows):
                description += rows[-3] + rows[-2] + row[-1]
    
            #真ん中の文の場合 前後の文を取ってくる
            else:
                description += rows[center_index-1] + rows[center_index] + rows[center_index+1]
            print('0')
            return description.replace(searchwords, "<b>{}</b>".format(searchwords))
        

        else:
            for word in searchword_list:
                if word in row:
                    center_index = index 
                    #最初の文の場合 後の２文を取ってくる
                    if center_index == 0:
                        row_1 = rows[0]
                        row_2 = rows[1]
                        row_3 = rows[2]
                        for word in searchword_list:
                            if word in row_1:
                                row_1 = row_1.replace(word, "<b>{}</b>".format(word))
                            if word in row_2:
                                row_2 = row_2.replace(word, "<b>{}</b>".format(word))
                            if word in row_3:
                                row_3 = row_3.replace(word, "<b>{}</b>".format(word))
                        description += row_1 + row_2 + row_3
                        
                        
                      
                    #最後の文の場合　前の２文を取ってくる
                    elif center_index == len(rows):
                        row_1 = rows[-3]
                        row_2 = rows[-2]
                        row_3 = rows[-1]
                        for word in searchword_list:
                            if word in row_1:
                                row_1 = row_1.replace(word, "<b>{}</b>".format(word))
                            if word in row_2:
                                row_2 = row_2.replace(word, "<b>{}</b>".format(word))
                            if word in row_3:
                                row_3 = row_3.replace(word, "<b>{}</b>".format(word))
                        description += row_1 + row_2 + row_3
                        
                     
                    #真ん中の文の場合 前後の文を取ってくる
                    else:
                        row_1 = rows[center_index-1]
                        row_2 = rows[center_index]
                        row_3 = rows[center_index+1]
                        for word in searchword_list:
                            if word in row_1:
                                row_1 = row_1.replace(word, "<b>{}</b>".format(word))
                            if word in row_2:
                                row_2 = row_2.replace(word, "<b>{}</b>".format(word))
                            if word in row_3:
                                row_3 = row_3.replace(word, "<b>{}</b>".format(word))
                        description += row_1 + row_2 + row_3
                        
                    return description
    
    return rows[0]


# Create your views here.
def homefunc(request):
    return render(request, 'home.html', {})

def rankfunc(request):
    if request.method == "POST":
        if 'searchWords' in request.POST:
            searchWords = request.POST['searchWords']
            
            if len(searchWords) >= 30:
                error_msg = "너무 깁니다."
                return render(request, "home.html", {"error_msg": error_msg})
            elif not searchWords:
                error_msg = "입력하세요."
                return render(request, "home.html", {"error_msg": error_msg})
            else:
                query = SearchQuery(searchWords)
                rank = SearchRank(F('search_vector'), query)
                
                results = DocDData.objects.annotate(rank=rank).filter(search_vector=query).order_by('-rank')[:25].values_list('title', 'doc', 'book_id', 'pk')
                
                error = ""
                if not results:
                    error = "No results found."
                
                book_ids = []
                titles = []
                docs = []
                pks = []

                for i, result in enumerate(results):
                    if i == 25:
                        break
                    book_ids.append(result[2])
                    titles.append(result[0])
                    docs.append(result[1])
                    pks.append(result[3])
            
                # descriptionの部分
                descriptions = []
            
                for doc in docs:
                    
                    descriptions.append(return_description(doc, searchWords))
                    

                objs = zip(titles, pks, book_ids, descriptions)
                
                return render(request, "list.html", {'objs':objs, 'searchWords':searchWords, "error": error})
    return redirect('home')

        

def detail_func(request, pk):
    


    # pk = request.POST['pk']
    obj = get_object_or_404(DocDData, pk=pk)
    # doc_info = DocDData.objects.get(pk=pk)
    doc = obj.doc
    docList = doc.split("\n")

    texts = ""
    for doc in docList:
        if len(doc) <= 33:
            
            if re.match(r'[0-9]{1,3}\s', doc):
                page = re.match(r'[0-9]{1,3}\s', doc).group()
                texts += doc.replace(page, "p{} \n\n".format(page))

            elif re.match(r'[0-9]{1,3}\t', doc):
                page = re.match(r'[0-9]{1,3}\t', doc).group()
                texts += doc.replace(page, "p{} \n\n".format(page))
            
            elif re.match(r'[0-9]{1,3}', doc):
                page = re.match(r'[0-9]{1,3}', doc).group()
                texts += doc.replace(page, "p{} \n\n".format(page))

            else:
                doc += "\n"
                texts += doc

        else:
            texts += doc
    title = obj.title
    book_id = obj.book_id
    next_pk = pk + 1
    if next_pk == 108779:
        next_pk = pk
    previous_pk = pk - 1
    if previous_pk == 10504:
        previous_pk = pk

    return render(request, "detail.html", {'book_id':book_id, 'title':title, 'texts':texts, 'pk':pk , 'next_pk':next_pk, 'previous_pk':previous_pk})

def gofunc(request):
    if request.method == "POST" and 'bookId' in request.POST:
        title = ""
        texts = ""
        pk = 5
        next_pk = 5
        previous_pk = 5
        
        if (request.POST['bookId'].isdigit()==False) or (request.POST["page"].isdigit()==False):
            error_msg2 = "error"
            return render(request, 'home.html', {"error_msg2":error_msg2})
        elif (not 1<=int(request.POST['bookId'])<=615) or (not 1<=int(request.POST['page'])<=615) :
            error_msg2 = "error"
            return render(request, 'home.html', {"error_msg2":error_msg2})
        else: 
            try:
                book_id = str(int(request.POST['bookId']))
                page = str(int(request.POST['page']))
                obj = DocDData.objects.filter(book_id__contains=book_id, pages__contains=page)
                
                doc = obj[0].doc
                title = obj[0].title
                pk = obj[0].pk
                next_pk = pk + 1
                if next_pk == 108779:
                    next_pk = pk
                previous_pk = pk - 1
                if previous_pk == 10504:
                    previous_pk = pk
                
                
                docList = doc.split("\n")
            
                for doc in docList:
                    if len(doc) <= 33:
                        
                        if re.match(r'[0-9]{1,3}\s', doc):
                            page = re.match(r'[0-9]{1,3}\s', doc).group()
                            texts += doc.replace(page, "p{} \n\n".format(page))

                        elif re.match(r'[0-9]{1,3}\t', doc):
                            page = re.match(r'[0-9]{1,3}\t', doc).group()
                            texts += doc.replace(page, "p{} \n\n".format(page))
                        
                        elif re.match(r'[0-9]{1,3}', doc):
                            page = re.match(r'[0-9]{1,3}', doc).group()
                            texts += doc.replace(page, "p{} \n\n".format(page))

                        else:
                            doc += "\n"
                            texts += doc

                    else:
                        texts += doc
                    
                return render(request, "detail.html", {'book_id':book_id, 'title':title, 'texts':texts, 'pk':pk , 'next_pk':next_pk, 'previous_pk':previous_pk})
            except:
                error_msg2 = "error"
                return render(request, 'home.html', {"error_msg":error_msg2})
                
        return redirect('home') 

    return redirect('home')

def kebaruja_ja(request):
    return render(request, "kebaruja_ja.html", {})

def kebaruja_ko(request):
    return render(request, "kebaruja_ko.html", {})

