def filtering(user_item_publisher, userID, itemID):
    # user_item_publisher: user_item dictionary for current publisher
    # userID: requesting userID that shall get a recommendation

    # NEW: userID == 0 is still compared to other based on the current article

    similarity_list = {}
    # iterate through all users for that publisher
    for key in user_item_publisher.keys():

        # skip for loop if key user is equal to the requesting user or if key is zero
        if (key == userID) or (key == 0):
            similarity_list[key] = 0
            continue

        # if userID=0 but we know the itemID of the article that is currently been read, we take only this as item-list
        elif userID == 0 and itemID != 0:

            requesting_user_item = itemID
            compared_user_items = user_item_publisher[key]

            #TODO does not make much sense but search for one user that has read the same article and more than one
            #TODO --> should use item/item filtering here

            if (requesting_user_item in compared_user_items) and (len(compared_user_items) > 1):
                most_similar_user = key
                break

        # optimal case - we know user and itemID:
        else:
            requesting_user_items = user_item_publisher[userID]

            # compared_user is the user the requesting user is currently been compared to
            compared_user_items = user_item_publisher[key]
            similarity_list.setdefault(key, 0)

            # count +1 if requesting user and compared user have read the same item
            for i in requesting_user_items:
                if i in compared_user_items:
                    similarity_list[key] = similarity_list[key] + 1


    if userID != 0:
        # find the most similar user by the max value in the similarity_list
        most_similar_user = max(similarity_list, key=similarity_list.get)
        # get the item_list of the most similar user
        most_similar_item_list = user_item_publisher[most_similar_user]
        # subtract lists to only obtain the items the requesting user has not read yet
        not_read_list = set(most_similar_item_list) - set(user_item_publisher[userID])
    else:
        # if userID == 0 take only the current item
        try:
            most_similar_item_list = user_item_publisher[most_similar_user]
        except:
            return [0]
        # put item in list with length 1 to be able to subtract the lists to get those items from the compared user that
        # are not the currently been read item
        itemID_asList = [itemID]
        not_read_list = set(most_similar_item_list) - set(itemID_asList)

    # return 5 items from this function --> zero if not_read_list out of bounds
    user_user_result = []
    for i in range(6):
        try:
            user_user_result.append(list(not_read_list)[i])
        except:
            user_user_result.append(0)
    try:
        return user_user_result
    except:
        return [0]