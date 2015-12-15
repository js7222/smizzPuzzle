
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



class Grid(object):
    def __init__(self,row_values,column_values,filtered_grid):
        self.row_values = row_values
        self.column_values = column_values
        self.filtered_grid = filtered_grid
        self.permuted_columns = []
        self.permuted_rows = []
        self.row_length = len(column_values)
        self.column_length = len(row_values)

    def get_filter_row(self,index):
        return self.filtered_grid[index]

    def permute_rows(self):
        self.permuted_rows = [permute_row(row_value, self.row_length) for row_value in self.row_values]
        return self.permuted_rows
    
    def filter_rows(self):
        for i in xrange(len(self.permuted_rows)):
            filter = self.get_filter_row(i)
            filtered_row = filter_out_permute(self.permuted_rows[i],filter)
            self.permuted_rows[i] = filtered_row
        return self.permuted_rows
        
