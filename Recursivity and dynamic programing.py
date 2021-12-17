def longest_oscillation(array):
    '''
    This function takes an array of integers as input and returns the indexes of longest oscillation
    defined as the longest alternating sequence of numbers such that:

    L[aj] 6= L[aj+1]
    if L[aj] < L[aj+1], then L[aj+1] > L[aj+2]
    if L[aj] > L[aj+1], then L[aj+1] < L[aj+2]

    The function uses a DP approach with memoization in 2 lists of n length.

    Complexity: O(n) where n is the length of the input array
    Space complexity: O(n) where n is the size of the input list
    :param array: An array of integers
    :return: A tuple including the length of the longest oscillation and a list of integers representing the
    indexes of the elements included in the oscillation
    '''

    # If the list is empty return
    if len(array) == 0:
        return (0, [])

    # 2 lists for keeping track of the index that oscillate positively or oscillate negatively
    memo_positive = [0]
    memo_negative = [0]
    for x in range(1, len(array)):
        # if the current element is greater than the one before it it is oscillating positively
        # meaning the element before must be oscillating negatively.
        if array[x] > array[x-1]:
            memo_positive = memo_negative + [x]

        # if the current element is less than the one before it it is oscillating negatively
        # meaning the element before must be oscillating positively.
        elif array[x] < array[x-1]:
            memo_negative = memo_positive + [x]

    # return the list with the greatest oscillation
    if len(memo_negative) >= len(memo_positive):
        return len(memo_negative), memo_negative
    else:
        return len(memo_positive), memo_positive



def longest_walk(M):
    '''
    This function takes an N*M matrix as input and returns the longest increasing path in
    that matrix using a DP approach based on the DFS algorithm
    Complexity: O(N*M) where N and M are the dimensions of the input matrix.
    Space complexity: O(M*N) where N and M are the dimensions of the input matrix.
    :param M: An N*M matrix represented as a list of lists
    :return: a tuple containing the length of the longest path and the indexes corresponding to the moves
    '''
    # if the matrix is empty return
    if len(M) == 0:
        return (0, [])

    # Get the dimensions of the input matrix
    m, n = len(M), len(M[0])

    # Use an n*m matrix to keep track of all increasing paths
    memo = [[0]*m for _ in range(n)]

    # generate a list of length MN containing the maximum increasing path to the corresponding index
    Result = [longest_walk_aux(x, y, M, memo) for x in range(m) for y in range(n)]

    # an list to hold the solution
    solution = []
    maxVal = max(Result)

    # Get the index of the maximum path value
    index = Result.index(maxVal)
    # get the matrix coordinates of that element
    x, y = coordinates(index, n)
    # append the first coordinate to the solution
    solution.append((x, y))
    # this while loop will run at maximum N*M times where the longest path includes all elements
    while len(solution) < maxVal:
        # all possible moves from a position in a 2d matrix
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]
        # filter the valid moves from the current position
        validMoves = [move for move in moves if 0 <= move[0] < m and 0 <= move[1] < n]

        # iterate through the valid moves checking if the element at that position is 1 less than the current value\
        # if it is append it to the solution and break
        for move in validMoves:
            if Result[n*move[0] + move[1]] == Result[n*x + y] - 1:
                solution.append(move)
                x, y = move[0], move[1]
                break

    # reverse the solution to display it in ascending order
    solution.reverse()
    # return
    return maxVal, solution



def coordinates(index, n):
    '''
    This function takes a one dimensional list index and the number of columns in a matrix and returns
    the row and column of that element.
    :param index: The 1D index of the element
    :param n: the number of columns in the matrix
    :return: the row and column corresponding to the element
    '''
    return ((index // n), (index % n))


def longest_walk_aux(x, y, M, memo):
    '''
    This function recursively calls itself with all valid moves from the current position searching
    for the longest increasing path. It takes a memoized 2d array to return all results previously found
    declared in the caller function.
    :param x: The row in the matrix
    :param y: The column in the matrix
    :param M: The matrix represented as a 2d list
    :param memo: The memoization structure represented as a 2d list
    :return: The value of the longest path ending at position x, y
    '''

    # if the value has not been previously found and stored in memo
    if memo[y][x] == 0:
        # generate a list of all possible moves
        moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]
        # current value in matrix M
        currentVal = M[x][y]
        # list dimensions
        m, n = len(M), len(M[0])
        # filter all valid moves
        validMoves = [move for move in moves if 0 <= move[0] < m and 0 <= move[1] < n and currentVal > M[move[0]][move[1]]]
        # recursively call longest_walk_aux with all valid moves.
        arr = [longest_walk_aux(move[0], move[1], M, memo) for move in validMoves] + [0]
        # record the current return value in memo
        memo[y][x] = 1 + max(arr)
    return memo[y][x]




