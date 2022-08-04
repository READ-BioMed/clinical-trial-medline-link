import gzip
import sys
import xmltodict
import json
import jsonpickle

with gzip.open(sys.argv[1], 'r') as f:
    xml_dict = xmltodict.parse(f.read())

pubmed_articles = xml_dict['PubmedArticleSet']['PubmedArticle']

ids={}

for pa in pubmed_articles:
    pmid = pa['MedlineCitation']['PMID']['#text']

    article = pa['MedlineCitation']['Article']

    nctids = []


    if 'DataBankList' in article:
        journal = article["Journal"]["Title"]
        year = pa["PubmedData"]["History"]["PubMedPubDate"][-1]["Year"]

        for k,v in article['DataBankList'].items():
            if k=='DataBank':
                if type(v) == list:
                    for vv in v:
                        for k1,v1 in vv['AccessionNumberList'].items():
                            if v1 == None:
                                continue

                            if type(v1) == str:
                                if v1.lower().startswith('nct'):
                                    nctids.append(v1)
                            else:
                                for v11 in v1:
                                    #print("l:",v11)
                                    if type(v11)==str and v11.lower().startswith('nct'):
                                        nctids.append(v11)
                else:
                    for k1,v1 in v['AccessionNumberList'].items():
                        if v1 == None:
                            continue

                        #print(v1, type(v1))
                        if type(v1) == str:
                            if v1.lower().startswith('nct'):
                                nctids.append(v1)
                        else:
                            
                            for v11 in v1:
                                #print("nl:",v11)
                                if type(v11)==str and v11.lower().startswith('nct'):
                                    nctids.append(v11)
    if len(nctids) > 0:
        ids[pmid]= { "nctids": nctids }

        ids[pmid]["journal"] = journal
        ids[pmid]["year"] = year

        if 'MeshHeadingList' in pa['MedlineCitation']:
            ids[pmid]["MeSH"] =  pa['MedlineCitation']['MeshHeadingList']
        if 'PublicationTypeList' in article:
            ids[pmid]["PT"] = article["PublicationTypeList"]


with  open('./'+sys.argv[1]+'.json', 'w') as f:
    json.dump(jsonpickle.encode(ids), f)
