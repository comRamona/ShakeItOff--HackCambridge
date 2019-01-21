import requests
import csv
import urllib
import json
import os
from io import BytesIO
import requests
import json

def send_request(image_url):
# Set image_url to the URL of an ima.ge that you want to analyze
    subscription_key = os.environ['OCR_KEY']
    assert subscription_key
    vision_base_url = "https://uksouth.api.cognitive.microsoft.com/vision/v1.0/"
    ocr_url = vision_base_url + "ocr"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params  = {'language': 'unk', 'detectOrientation': 'true'}
    data    = {'url': image_url}
    response = requests.post(ocr_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    analysis = response.json()

    return analysis


def parse_result(analysis):
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            item = ""
            for word_info in word_metadata["words"]:
                item = item + word_info['text']
                item = item + " "
            word_infos.append(item)
    return word_infos


def clean_info(word_infos):

    stuff = [[x] for x in word_infos]



    data =  {

            "Inputs": {

                    "input1":
                    {
                        "ColumnNames": ["Col1"],
                        "Values": stuff
                    },        },
                "GlobalParameters": {
    }
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/387a031cf5974c38b75d4c1d23282804/services/a27a1c5b1a574aa1b96c97630f79f133/execute?api-version=2.0&details=true'
    api_key = os.environ["AZURE_API_KEY_CLEAN"]
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    try:
        #response = urllib2.urlopen(req)

        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        req = urllib.request.Request(url, body, headers) 
        response = urllib.request.urlopen(req)

        result = response.read()
        return result
    except Exception as error:
        print("The request failed with status code: ")
        return error

def classify_food(clean_data):

    decoded_clean_data = clean_data
    stuff = [[x] for x in itemize_list(decoded_clean_data)]

    # print(stuff)
    #stuff = [[x] for x in clean_data]

    data =  {

            "Inputs": {

                    "input1":
                    {
                        "ColumnNames": ["Col1"],
                        "Values": stuff
                    },        },
                "GlobalParameters": {
    }
    }

    body = str.encode(json.dumps(data))
    print(data)

    url = 'https://ussouthcentral.services.azureml.net/workspaces/387a031cf5974c38b75d4c1d23282804/services/3ca32335c31b4bfb9d2f06421cfa9bc1/execute?api-version=2.0&details=true'
    api_key =  os.environ["AZURE_API_KEY_CLASSIFY"]
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    try:
        # response = urllib2.urlopen(req)
        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        req = urllib.request.Request(url, body, headers) 
        print(req.data)
        response = urllib.request.urlopen(req)

        result = response.read()
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: ")
        print(error.read())
        return error

def match_classification(clean_data, classification):
    clean_data_items = itemize_list(clean_data)
    classification_items = itemize_list(classification)

    pairs = tuple(zip(clean_data_items, classification_items))

    foods = []
    for pair in pairs:
        if pair[1] == '1':
            foods.append(pair[0])
    return foods

def itemize_list(item_list):
    #print(item_list)
    calories = {}
    x=json.loads(item_list.decode('utf-8'))
    results = x['Results']
    values = results['output1']['value']['Values']
    allv=[]
    for v in values:
      allv.append(v[0])
    return allv

def compute_calories(items):
    total = 0
    final_res=[]
    for item in items:
        ll = str(item).lower()
        if "total" in ll or "ttl" in ll or "tota" in ll or "subtotal" in ll:
            break
        calories, name = get_calories_per_item(item)
        print(calories,name)
        #print(calories)
        if calories != -1:
           total += calories
           final_res.append((name,calories))
    return {
        'total': int(total),
        'items': final_res,
    }

def get_calories_per_item(item_name="waffle"):
    if item_name in ["welcome","thank you","balance"]:
        return -1, item_name
    if len(item_name) <=4:
        return -1,item_name
   
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients' # Set destination URL here
    url2 = 'https://trackapi.nutritionix.com//v2/search/instant'
    header_fields = {'Content-Type':'application/json', 'x-app-id': os.environ["NUTRITIONX_ID"], 
                     'x-app-key':os.environ["NUTRITIONIX_KEY"]}
    
    post_fields = {
     "query": item_name,
     "timezone": "US/Eastern"
    }

    headers = {}
    r = requests.post(url, data=json.dumps(post_fields), headers=header_fields)

    food = r.json()
    #return food
    food_info = food.get('foods',0)
    if food_info != 0:
        try:
            return food_info[0]['nf_calories'], item_name
        except Exception as e:
            print(e)
            return -1, item_name
    else:
        return -1,item_name


def main():
    image_url = "https://res.cloudinary.com/di1eacmti/image/upload/v1547978783/sg1wsizd72p2llcqj0pw.jpg"
    analysis = send_request(image_url)
    items = clean_info(parse_result(analysis))
    results = classify_food(items)
    foods = match_classification(items, results)
    print(compute_calories(foods[:4]))

if __name__ == '__main__':
   main()
