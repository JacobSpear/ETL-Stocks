def date_split(date_id):
    day = date_id % 100
    month = (date_id - day)//100 % 100
    year = (date_id-(100*month+day))//10000
    return (year,month,day)

def date_build(split_date):
    year = split_date[0]
    month = split_date[1]
    day = split_date[2]
    return 10000*year + 100*month + day

def leap_feb(year):
    if year%4==0:
        return 29
    else:
        return 28

def next_date(date_id):
    info = date_split(date_id)
    month_length = {
        1 : 31,
        2: leap_feb(info[0]),
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    if month_length[info[1]] == info[2] and info[1]==12:
        return date_build((info[0]+1,1,1))

    elif month_length[info[1]] == info[2]:
        return date_build((info[0],info[1]+1,1))

    else:
        return date_build((info[0],info[1],info[2]+1))

def date_id_sequence(date_list):
    date_dict = {}

    current = min(date_list)
    final = max(date_list)
    index = 0
    while current != next_date(final):
        date_dict[current] = index
        index += 1
        current = next_date(current)

    result = [date_dict[x] for x in date_list]

    return result

def to_string(date):
    split_date = date_split(date)
    
    split_date = [str(x) for x in split_date]
    
    for x in range(len(split_date)):
        if len(split_date[x])==1:
            split_date[x] = "0"+split_date[x]
    
    return split_date[0]+"-"+split_date[1]+"-"+split_date[2]
            
