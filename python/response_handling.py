import collections


def output(version, limit, itemID, userID, mostPopularItems, user_user_result, item_item_result):
# choose a function to be called by the version number given

        if version == 1:
            return version1(limit, mostPopularItems)
        elif version == 2:
            return version2(limit, itemID, userID, mostPopularItems, user_user_result, item_item_result)
        else:
            return {}

def version1(limit, mostPopularItems):
# only uses most_popular results

        # set up resp structure
        resp = {}
        resp['recs']={}
        resp['recs']['ints']={}
        resp['recs']['ints']['3']=[]

        # append most_popular items --> if empty append 0
        for i in range(limit):
            try:
                resp['recs']['ints']['3'].append(int(mostPopularItems[i]))
            except:
                resp['recs']['ints']['3'].append(0)

        return resp

def version2(limit, itemID, userID, mostPopularItems, user_user_result, item_item_result):
# merging all lists

    # set up resp structure
    resp = {}
    resp['recs'] = {}
    resp['recs']['ints'] = {}
    resp['recs']['ints']['3'] = []

    # if limit is 1 only recommend the most popular item
    if limit == 1:
        try:
            resp['recs']['ints']['3'].append(int(mostPopularItems[0]))
        except:
            resp['recs']['ints']['3'].append(0)


    else:
        # if itemID = 0 only recommend most popular items
        if itemID == 0:
            for i in range(limit):
                try:
                    resp['recs']['ints']['3'].append(int(mostPopularItems[i]))
                except:
                    resp['recs']['ints']['3'].append(0)

        elif userID == 0:

            if item_item_result:
                # if userID = 0 recommend mostly most-popular and leave one space for item-item
                for i in range(limit-1):
                    try:
                        resp['recs']['ints']['3'].append(int(mostPopularItems[i]))
                    except:
                        resp['recs']['ints']['3'].append(0)
                try:
                    resp['recs']['ints']['3'].append(int(item_item_result[0]))
                except:
                    resp['recs']['ints']['3'].append(0)

            else:
                for i in range(limit):
                    try:
                        resp['recs']['ints']['3'].append(int(mostPopularItems[i]))
                    except:
                        resp['recs']['ints']['3'].append(0)

        # we know everything
        else:

            all_results = mostPopularItems + user_user_result + item_item_result
            non_zero_entries = [i for i in all_results if i != 0]
            counterList = collections.Counter(non_zero_entries)
            sorted_list = counterList.most_common()

            for i in range(limit):
                try:
                    resp['recs']['ints']['3'].append(int(sorted_list[i][0]))
                except:
                    resp['recs']['ints']['3'].append(0)


    return resp


