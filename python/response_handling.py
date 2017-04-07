import collections


def output(version, limit, itemID, userID, mostPopularItems, user_user_result, item_item_result):
# choose a function to be called by the version number given

        if version == 1:
            return version1(limit, mostPopularItems)
        elif version == 2:
            return version2(limit, user_user_result, mostPopularItems)
        elif version == 3:
            return version3(limit, user_user_result, mostPopularItems)
        elif version == 4:
            return version4(limit, item_item_result)
        elif version == 5:
            return version5(limit, itemID, userID, mostPopularItems, user_user_result, item_item_result)
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

def version2(limit, user_user_result, mostPopularItems):
# start with most_popular and append user_user_results dependent on the specified num_of_user_user

        # specify how many items of user_user results should be appended
        num_of_user_user = 1
        # set up resp structure
        resp = {}
        resp['recs']={}
        resp['recs']['ints']={}
        resp['recs']['ints']['3']=[]

        # get non_zero entries of user_user results
        non_zero_entries_user = [i for i in user_user_result if i != 0]

        # get the first elements of most_popular
        most_popular_restricted = []
        for i in range(limit):
            try:
                most_popular_restricted.append(mostPopularItems[i])
            except:
                most_popular_restricted.append(0)

        #TODO in the following subtraction useful information might get lost...we should either only subtract those
        #TODO items that have been already put into the recommendation list or specifically search for users that
        #TODO have read different articles than the first few in mostPopularItems
        # subtract the most_popular results from user_user results to avoid recommending the same item twice
        user_user_diff = list(set(non_zero_entries_user) - set(most_popular_restricted))

        # counter needed to handle different indices for mostPopularItems and user_user_diff
        counter = 0
        for i in range(limit):
            # first append the most_popular items but leave space for user_user results based on num_of_user_user
            if i - (limit-num_of_user_user) <= 0:
                try:
                    resp['recs']['ints']['3'].append(int(mostPopularItems[i]))
                except:
                    resp['recs']['ints']['3'].append(0)
            else:
                try:
                    resp['recs']['ints']['3'].append(int(user_user_diff[counter]))
                    counter = counter + 1
                except:
                    # if user_user_diff is already empty although more of it should be appended, try taking another
                    # item from most_popular
                    try:
                        resp['recs']['ints']['3'].append(int(mostPopularItems[i]))
                    except:
                        resp['recs']['ints']['3'].append(0)

        return resp

def version3(limit, user_user_result, mostPopularItems):
# fill the resp with as many results we have from user_user and then fill to the limit with most_popular

        # set up resp structure
        resp = {}
        resp['recs']={}
        resp['recs']['ints']={}
        resp['recs']['ints']['3']=[]

        # get non_zero entries from user_user_results
        non_zero_entries_user = [i for i in user_user_result if i != 0]
        # get number of non-zero entries to see how many from user_user_results we can put in resp
        num_non_zero_entries = len(non_zero_entries_user)

        # to avoid recommending the same article twice subtract user_user from most_popular since we add user_user_
        # results first
        most_popular_diff = list(set(mostPopularItems) - set(user_user_result))

        # counter needed to handle different indices in most_popular and user_user
        counter = 0
        for i in range(limit):
            # append non-zero user_user results
            if i < num_non_zero_entries:
                resp['recs']['ints']['3'].append(int(user_user_result[i]))
            else:
                # if user_user_results already empty add most_popular
                try:
                    resp['recs']['ints']['3'].append(int(most_popular_diff[counter]))
                    counter = counter + 1
                except:
                    resp['recs']['ints']['3'].append(0)

        return resp

def version4(limit, item_item_result):
# only item_item_collaborative filtering

    # set up resp structure
    resp = {}
    resp['recs'] = {}
    resp['recs']['ints'] = {}
    resp['recs']['ints']['3'] = []

    # fill complete resp with item_item_results
    for i in range(limit):
        try:
            resp['recs']['ints']['3'].append(int(item_item_result[i]))
        except:
            resp['recs']['ints']['3'].append(0)

    return resp

def version5(limit, itemID, userID, mostPopularItems, user_user_result, item_item_result):
# merging

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


