def filtering(item_user_publisher, itemID):
# warning: I just swapped from user_item to item_user in the naming which could be confusing:
# item_user is a dictionary with items as keys and users that have read this item as entry

    similarity_list = {}
    # iterate through all items for that publisher
    for key in item_user_publisher.keys():

        # skip for loop if key item is equal to the requesting item or if key is zero
        if (key == itemID) or (key == 0):
            similarity_list[key] = 0
            continue

        else:

            requesting_item_users = item_user_publisher[itemID]
            # compared_item is that item the requesting item is currently been compared to
            compared_item_users = item_user_publisher[key]
            similarity_list.setdefault(key, 0)

            # count +1 if requesting item and compared item have been read by same user
            for i in requesting_item_users:
                if i in compared_item_users:
                    similarity_list[key] = similarity_list[key] + 1

    most_similar_items = sorted(similarity_list, key=similarity_list.get)

    # return 6 user from this function (limit is usually smaller or equal 6)
    item_item_result = []
    for i in range(6):
        try:
            item_item_result.append(list(most_similar_items)[i])
        except:
            item_item_result.append(0)
    try:
        return item_item_result
    except:
        return [0]