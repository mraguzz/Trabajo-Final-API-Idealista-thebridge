
# LO CORREGI, PERO NO PUEDO TESTEARLO YA QUE SOLAMENTE PUEDO HACER UNA BÚSQUEDA AL MES.

# Import the necessary libraries
import base64
import requests as rq
import json
import pandas as pd

# Define a function in order to obtain our personalised token
def get_oauth_token():
    '''
    This function will return our personalised token
    '''
    with open("api_key.txt", "r") as f:
        api_key = f.read()
    with open("secret.txt", "r") as g:
        secret = g.read()
    message = api_key + ":" + secret   # Combine the API key and the secret to get our personalised message
    auth = "Basic " + base64.b64encode(message.encode("ascii")).decode("ascii")   # Encode the message
    headers_dic = {"Authorization" : auth,
                   "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8"}   # Define our headers
    params_dic = {"grant_type" : "client_credentials",   # Define the request params
                  "scope" : "read"}
    r = rq.post("https://api.idealista.com/oauth/token",   # Perform the request with the api url, headers and params
                      headers = headers_dic,
                      params = params_dic)
    token = json.loads(r.text)['access_token']   # Obtain the personalised token, as a json
    return token

# Define a function to obtain our search url for Sale or Rent for Madrid (with Default params)

def define_search_url(operation, country = 'es',language = 'es',max_items = '50',property_type = 'homes',order = 'priceDown',
                      center = '40.4167,-3.70325',distance = '60000',sort = 'desc',bankOffer = 'false',maxprice = '1000000'):
    '''
    This function will combine our params with the url, in order to create our own search url
    params: 
    
    operation = Kind of operation (sale, rent) 
    base_url = 'https://api.idealista.com/3.5/'     # Base search url
    country = Search country (es, it, pt)                          
    language = Search language (es, it, pt, en, ca) 
    max_items = Max items per call, the maximum set by Idealista is 50
    property_type = Type of property (homes, offices, premises, garages, bedrooms)
    order =  Order of the listings, consult documentation for all the available orders  ('priceDown', 'priceUp')
    center = '40.4167,-3.70325'     # Coordinates of the search center -> Default= MADRID CENTER
    distance = Max distance from the center
    sort = How to sort the found items
    bankOffer = If the owner is a bank ('true', 'false')
    maxprice = '1000000'     # Max price of the listings
    '''
    url = ('https://api.idealista.com/3.5/'  +      
           country +
           '/search?operation=' + operation +
           '&maxItems=' + max_items +
           '&order=' + order +
           '&center=' + center +
           '&distance=' + distance +
           '&propertyType=' + property_type +
           '&sort=' + sort + 
           '&numPage=%d' +
           '&maxPrice=' + maxprice +
           '&language=' + language)
    
    return url

def search_api(url):  
    '''
    This function will use the token and url created previously, and return our search results.
    '''
    token = get_oauth_token()   #  Get the personalised token

    headers = {'Content-Type': 'Content-Type: multipart/form-data;',   # Define the search headers 
               'Authorization' : 'Bearer ' + token}

    content = rq.post(url, headers = headers)   # Return the content from the request

    result = json.loads(content.text)   # Transform the result as a json file

    return result

# Since we need to give pagination to our search and this is our first search, we will set the pagination as 1
pagination = 1
first_search_url = url %(pagination)

# Proceed to do the search with the paginated url
results = search_api(first_search_url)

# First of all, we can extract 50 results/page, but there are more pages, so we have to define how many pages there are.
total_pages = results['totalPages']

def results_to_df(results):
    '''
    This function will save the json results as a dataframe and return the resulting dataframe
    '''
    df = pd.DataFrame.from_dict(results['elementList'])

    return df

def concat_df(df, df_tot):
    '''
    This function will take the main dataframe (df_tot), and concat it with the given individual dataframe, 
    returning the main dataframe 
    '''
    pd.concat([df_tot,df])
    
    return df_tot

# Proceed to save the obtained results as a dataframe
df = results_to_df(results)

df_tot = df.copy()

for i in range(1,total_pages):
    url = ('https://api.idealista.com/3.5/'+country+'/search?operation='+operation+#"&locale="+locale+
           '&maxItems='+max_items+
           '&order='+order+
           '&center='+center+
           '&distance='+distance+
           '&propertyType='+property_type+
           '&sort='+sort+ 
           '&numPage=%s'+
           '&language='+language) %(i)  
    results = search_api(url) 
    df = pd.DataFrame.from_dict(results['elementList'])
    df_tot = pd.concat([df_tot,df])

## EL ERROR ANTERIOR SE DEBE A QUE LA API ME PERMITE HACER SOLO 100 BÚSQUEDAS AL MES.
## SON 50 RESULTADOS POR PÁGINA Y REALICE 100 BÚSQUEDAS.

df_tot.shape

df_tot.to_csv('idealista16-2.csv') # GUARDO DATASET CON FECHA