import requests
import logging
from datetime import datetime
from globals_vars import url

last_max_range_id = None
last_max_range_value = None

def GetFirstRowId(current_id):
    """Get the first ROW_ID and NumberOfPages from the REST API."""
    api_url = url + f"Location/{current_id}"

    try:
        response = requests.get(api_url, verify=False)
        response.raise_for_status()
        data = response.json()
        row_id_val = data.get("rowId")
        number_of_pages = data.get("numberOfPages")
        return row_id_val, number_of_pages
    
    except Exception as e:
        logging.error(f"Error fetching ROW_ID and NumberOfPages from API: {e}")
        return None, None

def GetMaxRange(current_id):
    """Get the MAX_RANGE from the REST API, cache by id."""
    global last_max_range_id, last_max_range_value
    if last_max_range_id == current_id and last_max_range_value is not None:
        return last_max_range_value
    api_url = url + f"Location/{current_id}"

    try:
        response = requests.get(api_url, verify=False)
        response.raise_for_status()
        data = response.json()
        last_max_range_id = current_id
        last_max_range_value = data.get("area")
        return last_max_range_value
    
    except Exception as e:
        logging.error(f"Error fetching MAX_RANGE from API: {e}")
        return None

def PostEachPallet(row_id, sub_row_val, distance_val, angle_x_val, angle_y_val):
    """Send each pallet data as JSON via HTTP POST."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    api_url = url + "RowEachPallet"

    payload = {
        "rowId": row_id,
        "palletNo": sub_row_val,
        "distance": distance_val,
        "angleX": angle_x_val,
        "angleY": angle_y_val,
        "updateDate": current_date
    }

    try:
        response = requests.post(api_url, json=payload, verify=False)
        response.raise_for_status()
        print(response)
        logging.info(f"POST each_pallet for ROW_ID: {row_id}, SUB_ROW: {sub_row_val}.")

    except Exception as e:
        logging.error(f"Error POST each_pallet: {e}")

def PostRowPallet(row_id, sub_row_val, sub_pallet_val):
    """Send ROW_PALLET data as JSON via HTTP POST."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    api_url = url + "RowPallet"

    if sub_pallet_val < 0:
        sub_pallet_val = -1

    payload = {
        "rowId": row_id,
        "palletNo": sub_row_val,
        "eachPallet": sub_pallet_val,
        "updateDate": current_date
    }

    try:
        response = requests.post(api_url, json=payload, verify=False)
        response.raise_for_status()
        print(response)
        logging.info(f"POST ROW_PALLET for ROW_ID: {row_id}, SUB_ROW: {sub_row_val}.")

    except Exception as e:
        logging.error(f"Error POST ROW_PALLET: {e}")

def PostStock(row_id, pallets_total):
    """Send STOCK update as JSON via HTTP POST."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    api_url = url + "Stock"

    payload = {
        "rowId": row_id,
        "pallet": pallets_total,
        "updateDate": current_date
    }

    try:
        response = requests.post(api_url, json=payload, verify=False)
        response.raise_for_status()
        print(response)
        logging.info(f"POST STOCK update for ROW_ID: {row_id}.")
    
    except Exception as e:
        logging.error(f"Error POST STOCK update: {e}")

def DeleteDataInStock():
    """Send delete row command as JSON via HTTP POST."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    api_url = url +"Stock/Data/" + current_date
    try:
        response = requests.delete(api_url, verify=False)
        response.raise_for_status()
        logging.info(f"Delete Data for Stock.")
    except Exception as e:
        logging.error(f"Error delete Stock.: {e}")