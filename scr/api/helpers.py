import math
import re
import globals_vars
import api_utils
import mqtt_handlers


def FormatPalletData(np):
    """Format pallet data for web interface."""
    return {"pallet_v": np}


def FormatPointData(dt):
    """Format point data for web interface."""
    return {'point': dt}


def FormatAllZero():
    """Format zero data for web interface."""
    return {'pallet_v': 0, 'point': 0}


def FormatPointZero():
    """Format zero point data for web interface."""
    return {'point': 0}


def FormatCurrentRow(row):
    """Format current row data for web interface."""
    return {'c_row_v': row}


def FormatRow(row):
    """Format row data for web interface."""
    return {'row_v': row}


def ExtractNumericValues(input_str):
    """Extract numeric values from the input string."""
    return re.findall(r'[-+]?\d*\.\d+|\d+', input_str)


def CollectSensorData(input_str):
    """Collect and append data from the input string to the respective lists."""
    data = ExtractNumericValues(input_str)
    globals_vars.angle_x.append(float(data[0]))
    globals_vars.angle_y.append(float(data[1]))
    globals_vars.distance.append(float(data[2]))


def ConvertAngle(input_angle):
    """Convert angle from degrees to radians."""
    return float(input_angle * (math.pi / 180))


def CalDistacetrue(distance_measure, angle_y_val):
    """Calculate the true distance using the distance and angle."""
    adj_distance = distance_measure * math.cos(ConvertAngle(angle_y_val))
    globals_vars.distance_true.append(adj_distance)


def CalculateAverageDistance():
    """Calculate the average true distance."""
    if globals_vars.distance_true:
        valid_distances = []
        for d in globals_vars.distance_true:
            close_values = [other for other in globals_vars.distance_true if abs(d - other) <= 0.6 and d != other]
            if len(close_values) > 0:
                valid_distances.append(d)
        if len(valid_distances) == 0:
            avg = -1
        else:
            avg = sum(valid_distances) / len(valid_distances)
        return avg
    return 0


def CalResultPallet(average_distance):
    """Calculate the number of pallets based on the average distance."""
    max_range = (api_utils.GetMaxRange(globals_vars.current_id) * 1.2) + 4.2
    pallet_calc = (max_range - average_distance) / 1.215
    if pallet_calc < 0.8:
        pallet = 1
    else:
        pallet = math.floor(pallet_calc)
    globals_vars.sub_pallet.append(pallet)
    return pallet


def SumPallet():
    """Sum the number of pallets in the sub_pallet list."""
    return sum(math.floor(p) for p in globals_vars.sub_pallet if p >= 0)


def ClearLists(*lists):
    """Clear all lists passed as arguments."""
    for l in lists:
        l.clear()


def HandleNextRowOrQR(row_id):
    """Handle logic when receiving NEXT_ROW or QR message."""
    pallets_total = SumPallet()
    print(f"Total pallets for {row_id} : {pallets_total}")
    mqtt_handlers.socketio.emit('send_row', FormatRow(row_id), namespace='/')
    mqtt_handlers.socketio.emit('send_pallet', FormatPalletData(pallets_total), namespace='/')
    mqtt_handlers.socketio.emit('set_point_zero', FormatPointZero(), namespace='/')
    FormatPalletData(pallets_total)
    api_utils.PostStock(row_id, pallets_total)
    ClearLists(globals_vars.sub_pallet)
    globals_vars.sub_row = 1
    globals_vars.current_id += 1
    return api_utils.GetFirstRowId(globals_vars.current_id)