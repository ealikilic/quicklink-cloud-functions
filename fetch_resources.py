def fetch_resources(request):
    from flask import escape
    import requests
    import re
    import json
    #Domain should be passed in Args
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and 'domain' in request_json:
        mainURL = request_json['domain']
    elif request_args and 'domain' in request_args:
        mainURL = request_args['domain']
    else:
        return json.dumps("No domain found")
        
        
    #Fetching home page to find a category url
    r = requests.get(mainURL)
    fullsource = r.text
    #Fetching category url with a site specific regex. You should make adjustments here
    caturl = re.findall('id="nav-level0-copy"><ul[^>]*>.*?href="(.*?)"',fullsource) 
    r = requests.get(caturl[0])
    cat_fullsource = r.text
    #Fetching product url with a site specific regex. You should make adjustments here
    produrl = re.findall('class=\"products-grid\">.*?<a href=\"(.*?)\"',cat_fullsource) 
    r = requests.get(produrl[0])
    prod_fullsource = r.text
    
    #Fetching url list with a file specific regex. You should make adjustments here
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
    res = catRes
    res.extend(prodRes)
    res = list(set(res)) #removing duplicate resources
    return json.dumps(res)
