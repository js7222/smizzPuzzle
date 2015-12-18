
def permute_row(values, row_length):
    if not values:
        return []

    required_length = sum(values) + len(values) - 1
    if row_length < required_length :
        raise ValueError
    permutes = []
    if len(values) == 1:
        value = values[0]
        bit_field = set_n_bits(value)
        permutes = [bit_field << i for i in reversed(xrange(0,row_length-value+1))]
        return permutes

    space_for_head = values[0] + 1
    tail = values[1:]
    min_space_for_tail = sum(tail) + len(tail) - 1
    while (space_for_head + min_space_for_tail -1 < row_length):
        tail_perms = permute_row(tail, row_length - space_for_head)
        head_perm = set_n_bits(values[0]) << (row_length-space_for_head+1)
        permutes += [head_perm | tail_perm for tail_perm in tail_perms]
        space_for_head += 1
    return permutes


def filter_out_permute(permutes, permute_filter):
    return [permute for permute in permutes if (permute & permute_filter) == permute_filter]


def set_n_bits(n):
    bit_field = 0
    for i in xrange(0,n):
        bit_field |= (1<<i)
    return bit_field

def get_filtered_column(grid,index,row_length):
    bit_mask = 1 << (row_length-1-index)
    column_length = len(grid)
    iter_mask = 1 << (column_length-1)
    value = 0
    for filtered_row in grid:
        if filtered_row & bit_mask:
            value |= iter_mask
        iter_mask >>= 1
    return value

def set_filtered_column(grid,index,row_length,value):
    bit_mask = 1 << (row_length-1-index)
    column_length = len(grid)
    iter_mask = 1 << (column_length-1)
    for filtered_row in grid:
        if iter_mask & value:
            filtered_row |=bit_mask
        iter_mask >> 1
    return 

def permute_values(permuted_values, value_length, values):
    return [permute_row(row_value, value_length) for row_value in values]

def get_unique_permuted_values(values):
    return [i for i in xrange(0,len(values)) if len(values[i])==1]

class Grid(object):
    def __init__(self,row_values,column_values,filtered_grid):
        self.row_values = row_values
        self.column_values = column_values
        self.filtered_grid = filtered_grid
        self.row_length = len(column_values)
        self.column_length = len(row_values)
        self.permuted_columns = [None for i in xrange(self.row_length)]
        self.permuted_rows = [None for i in xrange(self.column_length)]

    def get_filter_row(self,index):
        return self.filtered_grid[index]

    def get_filter_column(self, index):
        return get_filtered_column(self.filtered_grid,index,self.row_length)

    def permute_row(self,index):
        permuted_row = permute_row(self.row_values[index], self.row_length)
        self.permuted_rows[index] = permuted_row
        return permuted_row

    def permute_column(self,index):
        permuted_column = permute_row(self.column_values[index], self.column_length)
        self.permuted_columns[index] = permuted_column
        return permuted_column
    
    def permute_rows(self):
        [self.permute_row(i) for i in xrange(0,len(self.row_values))]
        return self.permuted_rows

    def permute_columns(self):
        [self.permute_column(i) for i in xrange(0,len(self.column_values))]
        return self.permuted_columns

    def get_unique_rows(self):
        return get_unique_permuted_values(self.permuted_rows)

    def filter_rows(self):
        for i in xrange(len(self.permuted_rows)):
            filter = self.get_filter_row(i)
            filtered_row = filter_out_permute(self.permuted_rows[i],filter)
            self.permuted_rows[i] = filtered_row
        return self.permuted_rows
    
    def filter_columns(self):
        for i in xrange(len(self.permuted_columns)):
            filter = self.get_filter_column(i)
            filtered_row = filter_out_permute(self.permuted_columns[i],filter)
            self.permuted_columns[i] = filtered_row
        return self.permuted_columns

    def calculate(self):
        pass

    def set_filtered_row(self,value,index):
        self.filtered_grid[index]=value


    def set_filtered_column(self,value,index):
        set_filtered_column(self.filtered_grid,index,self.row_length)
        
        

