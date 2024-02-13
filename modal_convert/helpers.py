from datetime import timedelta

def check_list_of_dict_by_date(list_data, date, key):
        data = []
        for val in list_data:
            if(date == val[key].date()):
                data.append(val)
        return data

def merge_list_filter_by_date(list1, list2, start_date, end_date):
        result = []
        delta = timedelta(days=1)
        while start_date <= end_date:
            data = check_list_of_dict_by_date(list1, start_date, 'start')
            if not data:
                data = check_list_of_dict_by_date(list2, start_date, 'start')
            if data:
                result += data
            start_date += delta
        return result