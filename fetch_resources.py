def fetch_resources(request):
    #@author: eyuep.alikilic - artefact Germany
    #@info: LW-Preload-List-Fetcher 21.06.2019
    from flask import escape
    import requests
    import re
    import json
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and 'domain' in request_json:
        mainURL = request_json['domain']
    elif request_args and 'domain' in request_args:
        mainURL = request_args['domain']
    else:
        return json.dumps("No domain found")
    r = requests.get(mainURL)
    fullsource = r.text
    caturl = re.findall('id="nav-level0-copy"><ul[^>]*>.*?href="(.*?)"',fullsource) 
    r = requests.get(caturl[0])
    cat_fullsource = r.text
    produrl = re.findall('class=\"products-grid\">.*?<a href=\"(.*?)\"',cat_fullsource) 
    r = requests.get(produrl[0])
    prod_fullsource = r.text
    ruleCSS ='href=\"('+mainURL+'\/media\/css_secure\/.*?css.*?)\"'
    ruleJS = 'src=\"('+mainURL+'\/media\/js\/.*?.js.*?)\"'
    catCSS = re.findall(ruleCSS,cat_fullsource) 
    catJS = re.findall(ruleJS,cat_fullsource) 
    catRes=catJS
    catRes.extend(catCSS)
    prodCSS = re.findall(ruleCSS,prod_fullsource) 
    prodJS = re.findall(ruleJS,prod_fullsource) 
    prodRes=prodJS
    prodRes.extend(prodCSS)
    homeCSS = re.findall(ruleCSS,fullsource)
    homeJS = re.findall(ruleJS,fullsource)
    homeRes = homeJS
    homeRes.extend(homeCSS)
    res = catRes
    res.extend(prodRes)
    res.extend(homeRes)
    res = list(set(res))
    base= re.findall('https:\/\/www.*..\.(.*)',mainURL)
    upload_blob("quicklink-resource-lists",json.dumps(res),"ql-res-list-"+base[0]+".json")

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(source_file_name,content_type='application/json')
    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
