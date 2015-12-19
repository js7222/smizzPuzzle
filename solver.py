
import functools

class GridComputeError(StandardError):
    pass

class NoSuchAxisError(StandardError):
    pass

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

def set_filtered_column(row_length,value,index,grid):
    formatter = "#0{}b".format(row_length + 2)
    bit_mask = 1 << (row_length-1-index)
    column_length = len(grid)
    iter_mask = 1 << (column_length-1)
    for i in xrange(0, len(grid)):
        filtered_row = grid[i]
        if iter_mask & value:
            filtered_row |= bit_mask
        grid[i] = filtered_row
        iter_mask >>= 1
    return 

def permute_values(permuted_values, value_length, values):
    return [permute_row(row_value, value_length) for row_value in values]

def get_unique_permuted_values(values):
    return [i for i in xrange(0,len(values)) if len(values[i])==1]

def get_axis_value(value, length):
    mask_bit = 1 << (length-1)
    separated_values = []
    last_bit_set=False
    formatter = "#0{}b".format(length + 2)
    while mask_bit:
        if mask_bit & value:
            if not last_bit_set:
                separated_values += [1]
            else:
                separated_values[-1]+=1
            last_bit_set=True
                
        else:
            last_bit_set=False
        mask_bit >>=1
    return separated_values
            
ROW=0
COLUMN=1

class Grid(object):
    def __init__(self,row_values,column_values,filtered_grid):
        self.row_values = row_values
        self.column_values = column_values
        self.filtered_grid = filtered_grid
        self.row_length = len(column_values)
        self.column_length = len(row_values)
        self.permuted_columns = [[]for i in xrange(self.row_length)]
        self.permuted_rows = [[] for i in xrange(self.column_length)]
        self.formatter = "#0{}b".format(self.row_length + 2)

    def get_filter_row(self,index,grid=None):
        grid = grid if grid else self.filtered_grid
        return grid[index]

    def print_value(self, value):
        print format(value, self.formatter)
        
    def get_filter_column(self, index,grid=None):
        grid = grid if grid else self.filtered_grid        
        return get_filtered_column(grid,index,self.row_length)

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

    def get_unique_axis(self,axis):
        if axis == ROW:
            return get_unique_permuted_values(self.permuted_rows)
        elif axis == COLUMN:
            return get_unique_permuted_values(self.permuted_columns)
        raise NoSuchAxisError
        
    def filter_rows(self, row_indices):
        for i in row_indices:
            filter = self.get_filter_row(i)
            filtered_row = filter_out_permute(self.permuted_rows[i],filter)
            self.permuted_rows[i] = filtered_row
        return self.permuted_rows
    
    def filter_columns(self, column_indices):
        for i in column_indices:
            filter = self.get_filter_column(i)
            filtered_row = filter_out_permute(self.permuted_columns[i],filter)
            self.permuted_columns[i] = filtered_row
        return self.permuted_columns

    def calculate(self):
        before_unique_columns = self.get_unique_axis(COLUMN)
        before_unique_rows = self.get_unique_axis(ROW)
        self.permute_rows()
        self.permute_columns()
        invalidated_rows = xrange(0,self.column_length)
        self.filter_unique_rows(invalidated_rows, before_unique_rows, before_unique_columns)
        self.print_filtered_grid()
        permuted_values = [([(permuted_row, False) for permuted_row in  self.permuted_rows[i]], i, ROW) for i in xrange(0,len(self.permuted_rows)) if len(self.permuted_rows[i]) != 1]
        permuted_values += [([(permuted_column, False) for permuted_column in self.permuted_columns[i]], i, COLUMN) for i in xrange(0,len(self.permuted_columns)) if len(self.permuted_columns[i]) != 1]
        permuted_values.sort(key=lambda arg: len(arg[0]))
        for permuted_value in permuted_values:
            print "no of permuted values {0} i {1} axis {2}".format(len(permuted_value[0]),permuted_value[1],permuted_value[2])
        self.print_filtered_grid()
        for permuted_pair,index,axis in permuted_values:
            for permuted_value,checked in permuted_pair:
                if not checked:
                    permuted_pair = True
                    filtered_grid = self.filtered_grid[:]
                    if axis == ROW:
                        self.set_filtered_row(permuted_value,index,filtered_grid)
                    elif axis == COLUMN:
                        self.set_filtered_column(permuted_value,index,filtered_grid)
                    try:
                        pass
#                        grid = Grid(self.row_values, self.column_values,filtered_grid)
#                        grid.calculate()
                    except GridComputeError:
                        "print try again"
                        
        
            
        
    def filter_unique_rows(self, invalidated_rows, before_unique_rows, before_unique_columns):
        permuted_rows_before = self.permuted_rows[:]
        self.filter_rows(invalidated_rows)
        unique_rows = self.get_unique_axis(ROW)
        before_filtered_grid = self.filtered_grid[:]
        for i in xrange(0,len(self.permuted_rows)):
            permute_row = self.permuted_rows[i]
            agg = ~0
            for value in permute_row:
                agg &= value
            new_value = self.get_filter_row(i) | agg
            self.set_filtered_row(new_value,i)

        get_filter_row = functools.partial(Grid.get_filter_row, self)
        invalidated_columns = self.get_invalidated_axes(xrange(0,self.row_length), before_filtered_grid, self.row_length, get_filter_row)
        if not invalidated_columns:
            return
        before_unique_rows = self.get_unique_axis(ROW)
        self.filter_unique_columns(invalidated_columns, before_unique_columns, before_unique_rows)
        for unique_column in self.get_unique_axis(COLUMN):
            if get_axis_value(self.get_filter_column(unique_column), self.column_length) != self.column_values[unique_column]:
                raise GridComputeError                
            
            

    def filter_unique_columns(self, invalidated_columns, before_unique_columns, before_unique_rows):
        self.filter_columns(invalidated_columns)
        unique_columns = self.get_unique_axis(COLUMN)
        before_filtered_grid = self.filtered_grid[:]
        for i in xrange(0,len(self.permuted_columns)):
            permute_column = self.permuted_columns[i]
            agg = ~0
            for value in permute_column:
                agg &= value
            new_value = self.get_filter_column(i) | agg
            self.set_filtered_column(new_value,i)

        get_filter_column = functools.partial(Grid.get_filter_column, self)
        invalidated_rows = self.get_invalidated_axes(xrange(0,self.column_length), before_filtered_grid, self.column_length, get_filter_column)
        if not invalidated_rows:
            return
        before_unique_columns = self.get_unique_axis(COLUMN)
        self.filter_unique_rows(invalidated_rows, before_unique_rows, before_unique_columns)
        for unique_row in self.get_unique_axis(ROW):
            if get_axis_value(self.get_filter_row(unique_row), self.row_length) != self.row_values[unique_row]:
                raise GridComputeError                
        
    def get_invalidated_axes(self, flipped_alt_axes, before_filtered_grid, alt_axis_length,get_filter_alt_axis):
        invalidated_axes = set()
        for flipped_alt_axis in flipped_alt_axes:
            before_alt_axis = get_filter_alt_axis(flipped_alt_axis,before_filtered_grid)
            after_alt_axis = get_filter_alt_axis(flipped_alt_axis,self.filtered_grid)
            if before_alt_axis & after_alt_axis != before_alt_axis:
                raise GridComputeError

            invalidated_bits = (~before_alt_axis & after_alt_axis)
            bit_mask = 1 << (alt_axis_length-1)
            index = 0
            while bit_mask:
                if bit_mask & invalidated_bits:
                    invalidated_axes.add(index)
                index += 1
                bit_mask >>= 1
        return invalidated_axes
    
    def print_filtered_grid(self):
        print "\n"
        for row in self.filtered_grid:
            print format(row, self.formatter)
    def set_filtered_row(self,value,index,grid=None):
        grid = grid if grid else self.filtered_grid
        grid[index]=value

    def set_filtered_column(self,value,index,grid=None):
        grid = grid if grid else self.filtered_grid
        set_filtered_column(self.row_length,value,index,grid)
