from typing import Any, Dict
import requests

from news.models import TopItem, Comment, PollOption


API_URL = 'https://hacker-news.firebaseio.com/v0'
ITEM_ENDPOINT = '/item/'
LATEST_ITEMS_ENDPOINT = '/topstories'
COMMENT_FIELDS = [f.name for f in Comment._meta.get_fields()]
TOPITEM_FIELDS = [f.name for f in TopItem._meta.get_fields()]
POLLOPTION_FIELDS = [f.name for f in PollOption._meta.get_fields()]


def api_call():
    """Get news Items from the HackerNews public API."""
    # get list of ids of latest top items
    latest_items_url  = ''.join([API_URL, LATEST_ITEMS_ENDPOINT, '.json'])
    print("Accessing: %s" % latest_items_url)
    api_response = requests.get(latest_items_url)
    print("Response code: %s", api_response.status_code)
    if api_response.status_code != 200:
        return
    print("Data: %s" % api_response.json())
    latest_top_items_list = api_response.json()

    for top_item in latest_top_items_list[:100]:
        item_response = requests.get(''.join([API_URL, ITEM_ENDPOINT, str(top_item),'.json']))

        if item_response.status_code != 200:
            continue
        print("Data: %s" % item_response.json())
        top_item_obj = item_response.json()

        # change id from external api to ext_id
        top_item_obj["ext_id"] = top_item_obj.pop("id")
        top_item_obj = format_fields(top_item_obj)
        
        comment_list =  []
        if "kids" in top_item_obj:
            comment_list = top_item_obj["kids"]
        
        top_item_obj = {k:v for k, v in top_item_obj.items() if k in TOPITEM_FIELDS}
        try:
            top_item = TopItem.objects.create(**top_item_obj)
        except Exception as e:
            print(e)
            continue
        else:
            print("%s: %s saved" % (top_item.type, top_item.title))

        if top_item_obj["type"] == "poll" and len(top_item_obj["parts"]) > 0:
            for poll_id in top_item_obj["parts"]:
                pollopt = requests.get(''.join([API_URL, ITEM_ENDPOINT, str(poll_id), '.json']))
                
                if pollopt.status_code != 200:
                    continue

                pollopt_obj = pollopt.json()
                pollopt_obj["ext_id"] = pollopt_obj.pop("id")
                pollopt_obj = format_fields(pollopt_obj)
                pollopt_obj = {k:v for k, v in pollopt_obj.items() if k in POLLOPTION_FIELDS}
                try:
                    pollopt = PollOption.objects.create(**pollopt_obj)
                except Exception as e:
                    print(e)
                    continue 
                else:
                    print("[SAVED] %s: %s" % (pollopt.type, pollopt.text))


        # get direct comments on the news item only
        if len(comment_list) == 0:
            continue

        for comment_id in comment_list:
            comment_resp = requests.get(''.join([API_URL, ITEM_ENDPOINT, str(comment_id), '.json']))
            if comment_resp != 200:
                continue
            
            comment_obj = comment_resp.json()
            comment_obj["ext_id"] = comment_obj.pop("id")
            comment_obj = format_fields(comment_obj)
            comment_obj = {k:v for k, v in comment_obj.items() if k in COMMENT_FIELDS}
            try:
                comm = Comment.objects.create(**comment_obj)
            except Exception as e:
                print(e)
                continue
            else:
                print("[SAVED] %s: %s" % (comm.type, comm.text))
    print("Fetch Complete!")

def format_fields(item_dict: Dict[str, Any]):
    """convert certain fields in API response to appropriate data types."""
    from django.utils.timezone import make_aware
    from datetime import datetime
    item_dict["time"] = make_aware(datetime.fromtimestamp(item_dict["time"]))
    return item_dict