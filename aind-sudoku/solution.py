assignments = []
row="ABCDEFGHI"
column="123456789"
digit=column

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B] 

boxes=cross(row,column)
unitlist=[cross(row,c) for c in column] + [cross(r,column) for r in row] 
unitlist = unitlist + [cross(r,c) for r in ["ABC","DEF","GHI"] for c in ["123","456","789"]]
#Diagonal
unitlist=unitlist + [[r+c for r,c in zip(row,column)]]+ [[r+c for r,c in zip(row,column[::-1])]]

box_unit=dict((b,[u for u in unitlist if b in u]) for b in boxes)
box_peer=dict((b,set(sum(box_unit[b],[])) - set([b])) for b in boxes)



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    #display(values)
    for u in unitlist:
        lst_len2=[b for b in u if len(values[b])==2]
        lst_twins=[(a,b) for a in lst_len2 for b in lst_len2 if ((a!=b) and (values[a]==values[b]))]
        for a,b in lst_twins:
            for c in u:
                if c!=a and c!=b:
                    for char in values[b]:
                        #print(c + " " + values[c])
                        assign_value(values,c,values[c].replace(char,""))
    print("\n")
    #display(values)
    return values
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    r=[]
    for a in A:
        for b in B:
            r.append(a+b)
    return r

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    r={}
    for n in range(len(grid)):
        if grid[n]==".":
            assign_value(r,boxes[n],"123456789")
        else:
            assign_value(r,boxes[n],grid[n])
    return r 

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    for r in row:
        s=""
        for c in column:
            s= s +  str(values[r+c]).ljust(10)
            if c in "36":
                s=s + "|"
        print(s)	 
        if r in "CF":
             print("-" *10 * 9)
def eliminate(values):
    for b in boxes:
        if len(values[b])==1:
            for p in box_peer[b]:
                assign_value(values,p,values[p].replace(values[b],""))
        if len(values[b])==0:
            return False
    return values

def only_choice(values):
    for u in unitlist:
        for  d in digit:
            lst=[b for b in u if d in values[b]]
            if len(lst)==1:
                assign_value(values,lst[0],d)
    return values

def reduce_puzzle(values):
    value=eliminate(values)
    if value is False:
        return False
    value=only_choice(value)
    if solved(value):
        return value
    return search(value)  

def solved(values):
    if all(len(values[b])==1 for b in boxes):
        return True
    return False;

 
def solve(grid_init):
    return reduce_puzzle(grid_values(grid_init))
    


def search(values):
    n,s=min((len(values[s]),s) for s in boxes if (len(values[s])>1))
    for v in values[s]:
        values_search=values.copy()
        assign_value(values_search,s,v)
        values_search=reduce_puzzle(values_search)
        if values_search is not False:
            return values_search
    return False

if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    print("Inicial")
    display(grid_values(diag_sudoku_grid))
    
    solution=solve(diag_sudoku_grid)
    print("\n\nSolucion")
    if solution is False:
        print("Not solution")
    else:
        display(solution)

    #try:
    #    from visualize import visualize_assignments
    #    visualize_assignments(assignments)
    #except:
    #    print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
