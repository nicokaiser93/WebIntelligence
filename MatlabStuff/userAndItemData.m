% open the text file and save each line separately in 'wholeLines'
fid = fopen('nr100000lines.log');
wholeLines = textscan(fid,'%s','delimiter','\n');
fclose(fid);

% iterate through all lines 
recCounter = 1;
for k = 1:numel(wholeLines{1})
    % check if line belongs to recommendation_request
    if strcmp('recommendation_',wholeLines{1}{k}(1:15))
        % get string without the title in the beginning
        thisLine = wholeLines{1}{k}(25:end);
        % attributes are always divided by a comma, so split the thisLine
        % into its attributes (little mistake if text has comma)
        lineSplitByContent = textscan(thisLine,'%s','delimiter',',');
        % write all attributes of one line in a cell in
        % recommendation_request 
        recommendation_request{recCounter} = lineSplitByContent{1};
        recCounter = recCounter + 1;
    end
end

%% what user and item IDs do we have

% iterate through all recommendation_requests
for k = 1:numel(recommendation_request)
    % iterate through all attributes of one recommendation_request
    for l = 1:numel(recommendation_request{k})
        % if attribute has at least 4 digits
        if numel(recommendation_request{k}{l}) > 3
            % if the attribute belongs to userID (code is 57)
            if strcmp(recommendation_request{k}{l}(1:4), '"57"')
                % get the userID as number
                thisUserID = str2double(recommendation_request{k}{l}(6:end));
                % save all userIDs in an array
                userIDs(k) = thisUserID;
            end
            % look also for itemID in this row (code 25)
            if strcmp(recommendation_request{k}{l}(1:4), '"25"')
                % get itemID as number
                thisItemID = str2double(recommendation_request{k}{l}(6:end));
                % save all itemIDs in an array
                itemIDs_1(k) = thisItemID;
            end
        end
    end
end

% remove all entries that occur multiple times and sort them 
userIDs = unique(userIDs);
% save to array itemIDs_1 because we are yet missing the items that are
% mentioned in the lines with 'item_update'
itemIDs_1 = unique(itemIDs_1);
% put all userIDs in a struct called 'user'
user = struct('id',userIDs);



%% what articles did a user read

% put all itemIDs a user has read into a cell in user.articlesRead
user.articlesRead = cell(1,numel(user.id));

% iterate through all recommendation_requests
for k = 1:numel(recommendation_request)
    % iterate through all attributes in a recommendation_request
    for l = 1:numel(recommendation_request{k})
        % if attribute has at least 4 digits
        if numel(recommendation_request{k}{l}) > 3
            % if attribute has code 25 it is for the itemID
            if strcmp(recommendation_request{k}{l}(1:4), '"25"')
                % temporarily save the itemID that is in this
                % recommendation_request
                itemID = str2double(recommendation_request{k}{l}(6:end));
            end
            % search for the user in this specific recommendation_request
            if strcmp(recommendation_request{k}{l}(1:4), '"57"')
                % get userID as number
                userID = str2double(recommendation_request{k}{l}(6:end));
                % search this userID in the user struct and save its index
                userIndex = find(user.id == userID);
                % append the itemID of this recommendation_request to 
                % user.articlesRead with the found ID
                user.articlesRead{userIndex} = [user.articlesRead{userIndex}, itemID];
            end
        end    
    end
end

% the first entry here contains all users that were not recognized in the
% recommendation_request...therefore they were given the number 0 and they
% are very many. Since they are untraceable, remove those entries.
user.articlesRead{1} = 0;

%% now for the items

% iterate through all lines and find those that start with
% 'item_update'(same procedure as for users before)
itemCounter = 1;
for k = 1:numel(wholeLines{1})
    % if line starts with'item_'
    if strcmp('item_',wholeLines{1}{k}(1:5))
        % get line without title
        thisLine = wholeLines{1}{k}(14:end);
        % attributes are always divided by a comma, so split the thisLine
        % into its attributes (little mistake if text has comma)
        lineSplitByContent = textscan(thisLine,'%s','delimiter',',');
        % write all attributes of one line in a cell in
        % item_update_content 
        item_update_content{itemCounter} = lineSplitByContent{1};
        itemCounter = itemCounter + 1;
    end
end
%% what user ids do we have in the item_update lines

% iterate through all item_updates
for k = 1:numel(item_update_content)
    % iterate through all attributes of an item_update
    for l = 1:numel(item_update_content{k})
        % if it has at least 4 digits
        if numel(item_update_content{k}{l}) > 3
            % check if attribute is "id"
            if strcmp(item_update_content{k}{l}(1:4), '"id"')
                % temporarily save this itemID
                thisID = str2double(item_update_content{k}{l}(6:end));
                % save thisID to an array of IDs
                itemIDs_2(k) = thisID;
            end
        end
    end
end
% remove double entries and sort them
itemIDs_2 = unique(itemIDs_2);

% put together all itemIDs
allItemIDs = [itemIDs_1 , itemIDs_2];
% write all itemIDs in a item struct
item.id = allItemIDs;

%% see by whom a specific item has been read

% make a struct that contains a cell array of userIDs that have read this
% article
item.readBy = cell(1,numel(item.id));

% iterate through all items
for item_idx = 1:numel(item.readBy)
    % iterate through all users (except thefirst, because that are the not
    % recognized users)
    for user_idx = 2:numel(user.id)
        % see if the current itemID appears in the list of articles the
        % current user has read
        if sum(user.articlesRead{user_idx} == item.id(item_idx)) > 0
            % if yes save the userID that has read this article to the
            % 'readBy' struct of the current item
            item.readBy{item_idx} = [item.readBy{item_idx}, user.id(user_idx)];
        end
    end
end


%% general information

% iterate through all items
for k = 1: numel(item.readBy)
    % see how many users have read this article
    numOfReaders(k) = numel(item.readBy{k});
end
% save the number to the item struct
item.numOfReaders = numOfReaders;
% see by how many users an article has been read in average
mean(numOfReaders);

% iterate through all users
for k = 1:numel(user.articlesRead)
    % see how many articles a user has read
    numOfArticlesRead(k) = numel(user.articlesRead{k});
end
% save number to user struct
user.numOfArticlesRead = numOfArticlesRead;
% see how many articles a user has read in average
mean(numOfArticlesRead);
