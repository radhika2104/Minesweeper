import random
import math
import time
from player import Human,RandomComputer,GeniusComputer
class Minesweeper:
    def __init__(self):
        self.r = 0
        self.c = 0
        while True:
            self.level = input('Enter "e","m" or "h" to choose from levels - easy,medium,hard: ')
            if self.level == "e":
                self.r = 5
                self.c =6
                break
            elif self.level == 'm':
                self.r=10
                self.c=10
                break
            elif self.level == 'h':
                self.r=15
                self.c=15
                break
            else:
                print('Invalid input. Please try again', '\n')
        self.board = [[' ' for j in range(self.c)] for i in range(self.r)]
        self.current_status = None
        self.user_guide_board = None

    def print_actual_board(self):
        #helper function to see current state of actual board
        for row in self.board:
            print(row)

    def create_user_guide_board(self,first_move):
        first_move = int(first_move)
        self.user_guide_board = [[' ' for j in range(self.c)] for i in range(self.r)]
        current_col= ((first_move%self.c)-1) if first_move%self.c!=0 else (self.c-1)
        current_row = math.ceil((first_move/self.c)-1)
        if self.level=='e':
            unlock_cells = (self.r*self.c)//4 #cells to be unlocked in first move

        elif self.level=='m':
            unlock_cells = (self.r*self.c)//6

        elif self.level=='h':
            unlock_cells = (self.r*self.c)//12

        self.user_guide_board[current_row][current_col]=str(self.board[current_row][current_col])
        unlocked_cells = 1
        direction_vectors = [0,1,-1]
        while unlocked_cells<=unlock_cells: #and len(q)>0 :

            k_r=random.choice(direction_vectors)
            k_c=random.choice(direction_vectors)

            if 0<=current_row+k_r<=(self.r-1):
                current_row += k_r
            else:
                continue
            if 0<=current_col+k_c<(self.c-1):
                current_col += k_c
            else:
                continue
            if self.board[current_row][current_col]== 'M':
                continue
            if self.user_guide_board[current_row][current_col]== ' ':

                self.user_guide_board[current_row][current_col]=str(self.board[current_row][current_col])
                unlocked_cells +=1

    def make_vectors(self):
        vectors= [(-1,0),(0,-1),(1,0),(1,0),(0,1),(0,1)]
        #every next_breadth_vectors is basically a bigger spiral breadth than the current one to navigate
        #there will be maximum self.r or self.c spirals to navigate from
        for counter in range(1,(max(self.r,self.c)*2+1)):
            i=2
            part_list= [vectors[0]]+[vectors[0]]*2*counter +[vectors[1]]+[vectors[1]]*2*counter
            while i<=5:
                part_list.extend([vectors[i]]+[vectors[i]]*counter)
                i+=1
            vectors.extend(part_list)
        return vectors
    def random_valid_cell(self,row,col,eligible_dict,vector_array,vector_counter):
        #if game is won, there will be no eligible cell to unlock, so we set current_status to false and return current_status
        #otherwise we recursively check if cells are valid after adding direction vectors and return a valid row,col
        if len(eligible_dict)==0:
            self.current_status=False
            #print('printing output as current status: ',self.current_status)
            return self.current_status
        #we check if current_row or current_column is in range, else we increase the vector_counter to check next vector in spiral
        #if current_row,current_col is not in not_visited_or_mined, that means we cannot unlock it, so we increase the vector_counter to check next vector in spiral
        elif ((row,col) not in eligible_dict.values()) or row>=self.r or row<0 or col>=self.c or col<0:
            vector_counter=random.choice([0,1,2,5])
            #0,1,2,5 are indexes for unique possible vectors to choose from
            return self.valid_cell(row+vector_array[vector_counter][0],col+vector_array[vector_counter][1],eligible_dict,vector_array,vector_counter)
        #if current_row,current_col is valid and eligible to unlock we return the row and col
        else:
            self.current_status=True
            return (row,col)

    def valid_cell(self,row,col,eligible_dict,vector_array,vector_counter):
        #if game is won, there will be no eligible cell to unlock, so we set current_status to false and return current_status
        #otherwise we recursively check if cells are valid after adding direction vectors and return a valid row,col
        if len(eligible_dict)==0:
            self.current_status=False
            return self.current_status
        #we check if current_row or current_column is in range, else we increase the vector_counter to check next vector in spiral
        #if current_row,current_col is not in not_visited_or_mined, that means we cannot unlock it, so we increase the vector_counter to check next vector in spiral
        elif ((row,col) not in eligible_dict.values()) or row>=self.r or row<0 or col>=self.c or col<0:
            vector_counter+=1
            return self.valid_cell(row+vector_array[vector_counter][0],col+vector_array[vector_counter][1],eligible_dict,vector_array,vector_counter)
        #if current_row,current_col is valid and eligible to unlock we return the row and col
        else:
            self.current_status=True
            return (row,col)

    def update_user_guide_board(self,move,mines,game_iterations):
        move = int(move)
        #find the col and row of current move and unlock it
        current_col= ((move%self.c)-1) if move%self.c!=0 else (self.c-1)
        current_row = math.ceil((move/self.c)-1)
        self.user_guide_board[current_row][current_col]=str(self.board[current_row][current_col])
        unlocked_cells = 1
        #we know that available_moves are not visited yet by the user
        #create a not-visited dictionary of {available_moves:row,col}
        #only if a move(row,col) is in this dictionary, it will be eligible for unlock
        not_visited_or_mined=dict()
        available_moves=self.available_moves()
        for av_move in available_moves:
            av_col= ((av_move%self.c)-1) if av_move%self.c!=0 else (self.c-1)
            av_row = math.ceil((av_move/self.c)-1)
            not_visited_or_mined[av_move]=av_row,av_col
        #if length of eligible cells to be unlocked is 0, then user has won and we abort the game
        if len(not_visited_or_mined)==0:
            self.current_status=False
            return self.current_status
        #the range of cells to be unlocked will vary for different levels and they will be randomly selected within the range
        if self.level=='e':
            #cells to be unlocked in every move is going to be in range of 0 to a certain factor of number of cells depending upon level
            unlock_cells = random.choice(range(1,(self.r*self.c)//6)) #1 to 3 range for thirty cells
            random_breaker= (self.r*self.c)//10
        elif self.level=='m':
            unlock_cells = random.choice(range(1,(self.r*self.c)//10))
            random_breaker= (self.r*self.c)//15
        elif self.level=='h':
            unlock_cells = random.choice(range(1,(self.r*self.c)//16))
            random_breaker= (self.r*self.c)//20
        #incase of last moves, there might be a case when cells to be unlocked are greater than eligible cells, in that case we make then less than eligible cells or equal
        if unlock_cells>len(not_visited_or_mined):
            if len(not_visited_or_mined)>1:
                unlock_cells = len(not_visited_or_mined)-1
            else:
                unlock_cells=len(not_visited_or_mined)
        #complete vector list to navigate through entire board based on updated current row and col
        direction_vectors = self.make_vectors()

        #there is an extra condition to unlock cells,if there is a mine we cannot unlock it
        #we need to remove mines from not visited
        for mine in mines:
            if mine in not_visited_or_mined:
                del not_visited_or_mined[mine]

        while unlocked_cells<=unlock_cells:
            #helper function to give back valid or column
            #we randomly choose vectors during beginning of the game
            if game_iterations<random_breaker:
                return_status_or_tuple = self.random_valid_cell(current_row,current_col,not_visited_or_mined,direction_vectors,0)
            else:
                return_status_or_tuple = self.valid_cell(current_row,current_col,not_visited_or_mined,direction_vectors,0)

            if return_status_or_tuple==False:
                return self.current_status #we abort game if user has won, i.e. eligible list is 0
            else:
                current_row = return_status_or_tuple[0]
                current_col = return_status_or_tuple[1]
            #now if a current_row,current_col is in not_visited_or_mined, we can unlock it
                self.user_guide_board[current_row][current_col]=str(self.board[current_row][current_col])
                unlocked_cells +=1
            #once we unlock it , we remove it from not_visited_or_mined for next iteration of unlocking since it has been visited
                for key,value in dict(not_visited_or_mined).items():
                    if value==(current_row,current_col):
                        del not_visited_or_mined[key]
                #since we are updating list everytime, we also need to check if game is over, if list is 0-game is won
                if len(not_visited_or_mined)==0:
                    self.current_status=False
                    return self.current_status
                else:
                    self.current_status=True
        #we will reach here only if game continues, in that case we return game_status as true
        return self.current_status

    def print_user_board(self):
        print('\n','-----------------USER GAME BOARD-------------------','\n')
        for row in self.user_guide_board:
            print(' | ',end=' ')
            row_display = '   |  '.join(row)
            print(row_display,' |')
    #cannot make static because we will block the cells which need no input for visibility
    def board_index_reference(self):
        k=0
        print('\n','--------------MOVE REFERENCE BOARD----------------','\n')
        if self.user_guide_board==None:
            for row in self.board:
                    print(' | ',end='')
                    #row_list = []
                    row_list = [str(i+(self.c*k)) if row[i-1]==' ' or row[i-1]=='M' else str('#') for i in range(1,len(row)+1) ]
                    for cell in row_list:
                        if len(cell)==1:
                            print(' ',cell,end=' |')
                        elif len(cell)==2:
                            print('',cell,end=' |')
                        elif len(cell)==3:
                            print('',cell,end='|')
                    print()
                    k+=1
        else:
            moves =self.available_moves()
            i= 0
            for row in self.user_guide_board:
                print(' |',end='')
                for cell in row:
                    if cell!=' ':
                        print('  ','#',end='  |')
                    else:
                        if len(str(moves[i]))==1:
                            print('  ',str(moves[i]),end='  |')
                        elif len(str(moves[i]))==2:
                            print(' ',str(moves[i]),end='  |')
                        elif len(str(moves[i]))==3:
                            print(' ',str(moves[i]),end=' |')
                        i+=1
                print()

    def available_moves(self):
        moves = []
        k=0
        if self.user_guide_board==None:
            for row in self.board:
                moves += [(i+(self.c*k)) for i in range(1,len(row)+1) if row[i-1]== ' ' or row[i-1]=='M']
                k+=1
        else:
            for row in self.user_guide_board:
                moves += [(i+(self.c*k)) for i in range(1,len(row)+1) if str(row[i-1]) not in "123456780"]
                k+=1
        return moves

    def check_status(self):
        pass

    def create_mine_update_board(self,first_move):
        first_move = int(first_move)
        if self.level== 'e':
            n_mines = self.r*self.c//5
        elif self.level == 'm':
            n_mines = self.r*self.c//5
        elif self.level == 'h':
            n_mines = self.r*self.c//4 #can make divided by 5 if too tough
        current_col= ((first_move%self.c)-1) if first_move%self.c!=0 else (self.c-1)
        current_row = math.ceil((first_move/self.c)-1)
        self.board[current_row][current_col]='P'
        mine_list = random.sample(self.available_moves(),n_mines)

        for reference in mine_list:
            current_col= ((reference%self.c)-1) if reference%self.c!=0 else (self.c-1)
            current_row = math.ceil((reference/self.c)-1)

            self.board[current_row][current_col]='M'
        return mine_list

    def calculate_mines(self):
        #we will count adjacent mines for every cell and modify board
        for row_n in range(len(self.board)):
            for col_n in range(len(self.board[row_n])):
                mine_count =0
                adjacent_index = {} #map of every cell's ajacent row and column no. in form{cell_ref:[row_number,column_number]}
                if self.board[row_n][col_n] != 'M':
                    adjacent_index['top left']=[row_n-1,col_n-1]
                    adjacent_index['top']=[row_n-1,col_n]
                    adjacent_index['top right']=[row_n-1,col_n+1]
                    adjacent_index['left']=[row_n,col_n-1]
                    adjacent_index['right']=[row_n,col_n+1]
                    adjacent_index['bottom left']=[row_n+1,col_n-1]
                    adjacent_index['bottom']=[row_n+1,col_n]
                    adjacent_index['bottom right']=[row_n+1,col_n+1]

                    for row_r,col_r in adjacent_index.values():
                        if 0<=row_r<=(self.r-1) and 0<=col_r<=(self.c-1):
                    
                            if self.board[row_r][col_r] == 'M':
                                mine_count +=1
                    self.board[row_n][col_n] = mine_count
        return True

    def make_first_move(self,first_move):
        self.current_status = True
        player_ind_ref = int(first_move)-1
        #update game board with mines and first move
        mines= self.create_mine_update_board(first_move)
        #once the mines have been created and assigned on board, we need to -
        #calculate adjacent mines for each cell on board
        self.calculate_mines()
        #create user_guide and update_user_guide_board will be different because for each level no. of first clues are different from other clues
        self.create_user_guide_board(first_move)
        #printing the user_guide_board
        self.print_user_board()
        #create this board with references in backend
        #depending upon e,m,h: unlock and print first block size for first move
        #return first freeze block of the printed board for next move
        return mines

    def update_mines_user_board(self):
        for row_n in range(len(self.user_guide_board)):
            for col_n in range(len(self.user_guide_board[0])):
                if self.board[row_n][col_n]=='M':
                    self.user_guide_board[row_n][col_n]= 'M'

    def make_move(self,move,mines,game_iterations):
        current_col= ((move%self.c)-1) if move%self.c!=0 else (self.c-1)
        current_row = math.ceil((move/self.c)-1)
        #if user made a move on mine, game over and print mines
        if self.board[current_row][current_col]=='M':
            self.current_status = False
            print('\n','Oops...Mine discovered at current position.', '\n')
            #update mines in user_board to display it to user
            self.update_mines_user_board()
            print('printing all mines .....','\n')
        #else update the current position and unveil the user game board for next move
        else:
            self.current_status = self.update_user_guide_board(move,mines,game_iterations)
            if self.current_status==False:
                print('\n','Congratulations.You won!','\n')
                self.update_mines_user_board()
                print('printing all mines .....','\n')
        #printing the user_guide_board
        self.print_user_board()
        return self.current_status

def play(game,player):
    start_time = time.time()
    #printing cell references for first move
    game.board_index_reference()
    #getting first_move from player
    first_move_input= player.get_move(game)
    mines= game.make_first_move(first_move_input)
    game_iterations = 1
    #inorder to successfully unlock cells till end of game, so that we dont run between infinite loops
    #depending upon level of game, we make buckets of when to break the random pattern of unlocking cells
    #once random_breaker is breached, we will use simple breadth first search to unlock cells (randomly choosing cells at this point will go into infinite loop)

    while game.current_status:

        #printing index reference board to take user input while game continues
        game.board_index_reference()
        #we get move from user based on available moves
        user_move=player.get_move(game)
        #we make that move on board and if there is no mine at move made,we update user board and print it; else we stop the game since user looses
        time.sleep(0.6)
        valid = game.make_move(user_move,mines,game_iterations)
        if valid:
            game_iterations+=1
            #we check at every move if there are no more moves to be made and the user has won the game
        else:
            print('\n','Game Over!')
            elapsed_time = time.time()-start_time
            minus_time_sleep = 0.6*(game_iterations-1)
            print('\n','Time Taken {} seconds'.format(round(elapsed_time-minus_time_sleep)))
            break

if __name__== '__main__':
    p = Human()
    m = Minesweeper()
    play(m,p)
