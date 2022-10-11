
### accumulative summation

class Solver():

    def __init__(self, arr = None):
        assert arr is not None

        self.arr = arr
        self.arr_sum = sum(arr)
        self.arr_len = len(arr)
        self.idx1 = 0
        self.idx2 = len(arr)-1
        self.solutions_found = 0

    def solve(self):
        self.sum_left = self.arr[self.idx1]
        self.sum_right = self.arr[self.idx2]

        # Check if sum is not divisible by 3
        if self.arr_sum % 3 != 0:
            return self.solutions_found

        while self.idx1 < self.idx2: #O(N)
            
            # If left sum is smaller than right sum
            if self.sum_left > self.sum_right:
                self.idx2 -= 1
                self.sum_right += self.arr[self.idx2]
            # If right sum is smaller than left sum
            elif self.sum_right > self.sum_left:
                self.idx1 += 1
                self.sum_left += self.arr[self.idx1]
            # If both sums are equal
            elif self.sum_right == self.sum_left:
                sum_third = self.arr_sum - self.sum_left - self.sum_right
                #check if the third sum is also equal
                if sum_third == self.sum_left:
                    self.solutions_found += 1
                # break equilibrium to avoid infinite regress
                self.idx1 += 1
                self.sum_left += self.arr[self.idx1]
            else:
                # This error should not be trigerred under normal use cases
                raise ValueError("Witchcraft")

        return self.solutions_found



    
    

    
#Total: Time O(2N) ----> O(N)
#       Space O(1)
### Evolutionary search is not ideal here, but cool to try nevertheless.
if __name__ == "__main__":
    problem_1 = Solver(arr= [ 2, 2 ,0, 4, 0, 4])
    result = problem_1.solve()
    print(result)
        