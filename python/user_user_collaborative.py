def filtering(user_item_publisher, userID):
    # user_item_publisher: user_item dictionary for current publisher
    # userID: requesting userID that shall get a recommendation


    similarity_list = {}
    # iterate through all users for that publisher
    for key in user_item_publisher.keys():

        # skip for loop if key user is equal to the requesting user or if key is zero
        if (key == userID) or (key == 0):
            similarity_list[key] = 0
            continue

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


    if max(similarity_list, key=similarity_list.get) == 0:
        return [0]
    else:
        # sort users by similarity
        most_similar_users = sorted(similarity_list, key=similarity_list.get, reverse=True)
        # get the item_list of the most similar user
        most_similar_item_list = user_item_publisher[most_similar_users[0]]
        # now if item list of the most similar user has no new articles check the next similar user in the sorted list
        # (but only if similarity is not zero)
        counter = 0
        while (not(set(most_similar_item_list) - set(user_item_publisher[userID]))) \
                and (counter < len(most_similar_users)) \
                and similarity_list[most_similar_users[counter]] > 0:
            counter = counter + 1
            most_similar_item_list = user_item_publisher[most_similar_users[counter]]

        # subtract lists to only obtain the items the requesting user has not read yet
        not_read_list = set(most_similar_item_list) - set(user_item_publisher[userID])

    # return 6 items from this function --> zero if not_read_list out of bounds
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