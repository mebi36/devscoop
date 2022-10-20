from typing import Any, Dict, List, Optional
import requests

from news.models import TopItem, Comment, PollOption


API_URL = 'https://hacker-news.firebaseio.com/v0'
ITEM_ENDPOINT = '/item/'
LATEST_ITEMS_ENDPOINT = '/topstories'
COMMENT_FIELDS = [f.name for f in Comment._meta.get_fields()]
TOPITEM_FIELDS = [f.name for f in TopItem._meta.get_fields()]
POLLOPTION_FIELDS = [f.name for f in PollOption._meta.get_fields()]


def get_item_list() -> Optional[List[int]]:
    """Get list of latest new items from the HN api."""
    latest_items_url = ''.join([API_URL, LATEST_ITEMS_ENDPOINT, '.json'])
    api_response = requests.get(latest_items_url)
    if api_response.status_code == 200:
        return api_response.json()
    raise RuntimeError("Error %s" % api_response.status_code)


def get_item(item_id: int) -> Optional[Dict[str, Any]]:
    """Get item from HN api based by id."""
    item_url = ''.join([API_URL, ITEM_ENDPOINT, str(item_id), '.json'])
    api_response = requests.get(item_url)

    if api_response.status_code == 200:
        return api_response.json()
    raise RuntimeError("Error %s" % api_response.status_code)


def api_call():
    """Get news Items from the HackerNews public API."""
    latest_top_items_list = get_item_list()

    for top_item_id in latest_top_items_list[2:4]:
        print(top_item_id)
        top_item_obj = get_item(top_item_id)

        top_item_obj = prepare_for_save(top_item_obj)
        
        comment_list =  []
        if "kids" in top_item_obj:
            comment_list = top_item_obj["kids"]
        print("comments: ", comment_list)
        
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
                pollopt_obj = prepare_for_save(pollopt_obj)
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
            
            comment_obj = prepare_for_save(comment_obj)
            comment_obj = {k:v for k, v in comment_obj.items() if k in COMMENT_FIELDS}
            try:
                comm = Comment(content_object=top_item, **comment_obj)
                comm.save()
            except Exception as e:
                print(e)
                continue
            else:
                print("[SAVED] %s: %s" % (comm.type, comm.text))
    print("Fetch Complete!")

def prepare_for_save(item_dict: Dict[str, Any]):
    """Prepare API response object for saving to devscoop db."""
    
    from django.utils.timezone import make_aware
    from datetime import datetime
    # specify that item is from HN
    item_dict["from_hn"] = True
    # id from HN api will be saved in ext_id field
    item_dict["ext_id"] = item_dict.pop("id")
    # convert UNIX time from api to datetime object
    item_dict["time"] = make_aware(datetime.fromtimestamp(item_dict["time"]))
    
    return item_dict