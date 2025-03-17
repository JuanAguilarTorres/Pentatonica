import config.constants as constant

# ---------------------------
# Matrix Management
# ---------------------------
class MatrixManager:
    def __init__(self):
        self.matrices = [[[False for _ in range(constant.grid_cols)] for _ in range(constant.grid_rows)]]
        self.current_matrix_index = 0
        
    def add_matrix(self):
        self.matrices.append([[False for _ in range(constant.grid_cols)] for _ in range(constant.grid_rows)])
        return len(self.matrices) - 1
    
    def can_delete_last_matrix(self):
        if len(self.matrices) <= 1:
            return False
        
        last_matrix = self.matrices[-1]
        return all(not cell for row in last_matrix for cell in row)
    
    def delete_last_matrix(self):
        if self.can_delete_last_matrix():
            self.matrices.pop()
            if self.current_matrix_index >= len(self.matrices):
                self.current_matrix_index = len(self.matrices) - 1
            return True
        return False
    
    def get_current_matrix(self):
        return self.matrices[self.current_matrix_index]
    
    def switch_to_matrix(self, index):
        if 0 <= index < len(self.matrices):
            self.current_matrix_index = index
            return True
        return False