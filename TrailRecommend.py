trail_info_unsorted=[]
state_parks = {'a':'Keystone','b':'Kooser','c':'Laurel Hill','d':'Linn Run','e':'Ohiopyle'}
difficulties = {'a':'easiest','b':'more difficult','c':'most difficult'}



#Read data from text file and put into a list of lists
with open ("traildata.txt","r") as traildata:
  line = traildata.readline()
  while line != "":
    info = line.split("\t")
    #remove \n from data, change trail distance to a number
    info[5] = info[5][:-1]
    info[2] = float(info[2])
    trail_info_unsorted.append(info)
    line = traildata.readline()

#Sort by trail length since this assignment is about sorting
def sort2(left,right):
    result = []
    while left and right:
        if left[0][2]<right[0][2]:
            result.append(left[0])
            left.pop(0)
        else:
            result.append(right[0])
            right.pop(0)
    if left:
        result += left
    if right:
        result += right
    return result

def sort1(list1):
    if len(list1)<=1:
        return list1
    mid_index = len(list1)//2
    left_split = list1[:mid_index]
    right_split = list1[mid_index:]

    left_sorted = sort1(left_split)
    right_sorted = sort1(right_split)

    return sort2(left_sorted,right_sorted)


trail_info = sort1(trail_info_unsorted)






#ask for filter
def filter_main():
    print("Choose one or more categories to filter by:")
    print("\ta   by State Park")
    print("\tb   by trail length")
    print("\tc   by trail difficulty\n")
    filter_str = input("Choose 1 or more categories by typing in the letter(s) and then Enter: ")
    #put in list, get rid of repeats
    filter_list = list(filter_str)
    filter_set = set(filter_list)
    filter_list = list(filter_set)[::-1]

    return filter_list

#If we haven't started the interest list, add the filtered indexes
def add_to_list(inside_index,filter_set,interest_list):
    for index in range(len(trail_info)):
        if trail_info[index][inside_index] in filter_set:
            interest_list.append(index)
    return interest_list


#If interest list is already started, take out indexes that don't fit next filter
def subtract_from_list(inside_index,filter_set,interest_list):
    for index in reversed(interest_list):  
      if trail_info[index][inside_index] not in filter_set:
        interest_list.remove(index)
    return interest_list

#If user wants to filter by state park, this chooses park(s) and corrects interest list
def filter_park(interest_list):
    print("\n")
    print("Possible State Parks:")
    for key,park in state_parks.items():
        print("\t",key,"   ",park)
    park_list = input("Choose 1 or more State Parks by typing in the corresponding letter(s): ")
    park_set = set()
    for letter in park_list:
        if letter in state_parks:
            park_set.add(state_parks[letter])
    if not interest_list:
        add_to_list(1,park_set,interest_list)
    else:
        subtract_from_list(1,park_set,interest_list)
    
    return interest_list

#If user wants to filter by difficulty level, this chooseslevels(s) and corrects interest list  
def filter_difficulty(interest_list):
    print("\n")
    print("Possible Difficulty Levels:")
    for key,level in difficulties.items():
        print("\t",key,"   ",level)
    difficulty_list = input("Choose 1 or more difficulty levels by typing in the corresponding letter(s): ")
    difficulty_set = set()
    for letter in difficulty_list:
        if letter in difficulties:
            difficulty_set.add(difficulties[letter])
    if not interest_list:
        add_to_list(3,difficulty_set,interest_list)
    else:
        subtract_from_list(3,difficulty_set,interest_list)
    
    return interest_list

#If user wants to filter by trail length, this chooses max or min length
def ask_length(maxmin):
    if maxmin == 1:
        adj = "longest"
    else:
        adj = "shortest"
    length = input(f"\nHow many miles is the {adj} trail you would be interested in?")
    try: 
        return float(length)
    except:
        return None


#If user wants to filter by trail length, this finds all trails between max and min and corrects interest list
def filter_length(interest_list):
    max_length = None
    min_length = None
    while max_length == None:
        max_length = ask_length(1)
    while min_length == None:
        min_length = ask_length(0)
    if min_length > trail_info[-1][2] or max_length < trail_info[0][2]:
        interest_list = []
        return interest_list
    min_index = length_index(min_length)
    if min_index != 0 and trail_info[min_index][2]==min_length:
        while min_index > 0 and trail_info[min_index-1][2]==min_length:
            min_index -=1
    max_index = length_index(max_length)
    if trail_info[max_index][2]>max_length:
        max_index -= 1
    else:
        while max_index < len(trail_info)-1 and trail_info[max_index+1][2]==max_length:
            max_index +=1
    
    if len(interest_list) == 0:
        for index in range(min_index,max_index+1):
            interest_list.append(index)
    else:
        for index in reversed(interest_list):
            if index < min_index or index > max_index:
                interest_list.remove(index)
    
    return interest_list


##If user wants to filter by trail length, this finds index of max and min trails
def length_index(length,start_index = 0, end_index = None):
    if end_index == None:
        end_index = len(trail_info)-1
    mid_index = start_index + (end_index - start_index)//2
    if trail_info[mid_index][2] == length:
        return mid_index
    if start_index >= end_index:
        return mid_index
    if length > trail_info[mid_index][2]:
        start_index = mid_index + 1
    else:
        end_index = mid_index
    mid_index = length_index(length,start_index,end_index)
    return mid_index
    

#Prints results
def print_list(interest_list):
    if len(interest_list)==0:
        print("\n\nThere are no trails that meet your requirements.")
    else:
        if len(interest_list)==1:
            trails = "trail"
            fit = "fits"
            verb = "is"
            s = ""
        else:
            trails = "trails"
            fit = "fit"
            verb = "are"
            s = "s"
        print(f"\n\nThere {verb} {len(interest_list)} {trails} that {fit} your requirement{s}:\n")
        
        for index in interest_list:
          distance1 = str(trail_info[index][2])
          print(f"{trail_info[index][0]} Trail at {trail_info[index][1]} is {distance1} mile long and is rated as {trail_info[index][3]}.       Look for {trail_info[index][5]}. ")
      









all_finished = False
while not all_finished:
    print('\n\n/\  _FIND A LOCAL TRAIL_  /\______ ')
    print('  \/                      \/\n\n')
    print("We'll list all local trails that fit your requirements.\n")
    finished = False
    length_choice = False
    interest_list = []
    filter_list = filter_main()
    while filter_list and not finished:
        if filter_list[0]=='a':
            interest_list = filter_park(interest_list)
            if len(interest_list)==0:
                finished = True
        elif filter_list[0]=='b':
            length_choice = True
        elif filter_list[0]=='c':
            interest_list = filter_difficulty(interest_list)
            if len(interest_list)==0:
                finished = True
        filter_list = filter_list[1:]
            
    if length_choice:
        interest_list = filter_length(interest_list)

    print_list(interest_list)
    print("\n\n")
    ask = ""
    while ask!="y" and ask!="n":
        ask = input("Would you like to search again?  y or n:")
    if ask == "n":
        all_finished = True

print("\n\nGood bye!")


#trail_info is a list of lists, each element of first list contains 
# trail name, park name, trail length, difficulty, trail type, markers
#state_parks is dictionary mapping letter to Sate Park
#difficulties is dictionary mapping letter to difficulty level
#filter_list is list of letters of categories user wants to search by
#all_finished True when program done
#finished = True when search done
#length_choise is True if user filters by length