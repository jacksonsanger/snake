from __future__ import annotations
import dudraw
from dudraw import Color
import random

"""
    A program that uses dudraw to make the classic "snake" game
    Author: Jackson Sanger
    Date: 4-10-2023
    Course: COMP 1353
    Assignment: Project 1 - The Game of Snake
    Collaborators: none
    Internet Source: none
"""


#The Doubly Linked List class implementation:

# An individual node in a DoublyLinkedList.
# value: reference to the value stored in the node
# next: reference to the next node
# prev: reference to the previous node in the list
class Node:
    def __init__(self, v, p, n):
        self.value = v
        self.prev = p
        self.next = n
    
    def __str__(self):
       return str(self.value)

# A DoublyLinkedList data structure with sentinel nodes
# sentiel nodes header and trailer store None as values and are not part of the list
# The purpose of the sentiel nodes is to ensure all adds and removes are happening beteween two nodes
# (eliminates all special cases)
class DoublyLinkedList:
   
    def __init__(self):
        #initialize the header and trailer nodes. the trailer points to the header
        self.header = Node(None, None, None)
        self.trailer = Node(None, self.header, None)
        #make header point to trailer
        self.header.next = self.trailer
        self.size = 0
    
    #this method prints the doubly linked list for debugging purposes
    def __str__(self):
        #if list is empty:
        if self.header.next is self.trailer:
            return "[]"
        #create a result string
        result = '['
        #loop through the list, stopping at the last node
        temp = self.header.next
        while temp.next is not self.trailer:
            #add the value to the string
            result += str(temp.value) + " "
            temp = temp.next
        #return the result string plus the last value
        return result + str(temp) + "]"

    #method that returns whether or not the list is empty
    def is_empty(self):
        return self.size == 0
    
    #method that returns the size of the list
    def get_size(self):
        return self.size
    
    #method that returns the first value in the list
    def first(self):
        if self.size == 0:
            raise ValueError("List is empty")
        return self.header.next.value
    
    #method that returns the last value in the list
    def last(self):
        if self.size == 0:
            raise ValueError("List is empty")
        return self.trailer.prev.value

    #adds the value v between nodes n1 and n2
    def add_between(self, v, n1, n2):
        if n1 is None or n2 is None:
            raise ValueError("Invalid n1 or n2 - can't be None")
        if n1.next is not n2:
            raise ValueError("Second node must come after first node")
        
        #step 1: make a new node
        new_node = Node(v, n1, n2)
        
        #step 2: fix n1.next and n2.prev
        n1.next = new_node
        n2.prev = new_node

        #step 3: increment size
        self.size += 1

    def add_first(self, v):
        """
            parameters:
                v: type is the generic type E of the list
            return:
                None
            adds a the value v at the head of the list
        """
        self.add_between(v, self.header, self.header.next)

    def add_last(self, v):
        """
            parameters:
                v: type is the generic type E of the list
            return value:
                None
            adds a the value v at the tail of the list
        """
        self.add_between(v, self.trailer.prev, self.trailer)
    
    def remove_between(self, node1, node2):
        # check if either node1 or node2 is None. Raise a ValueError if so.
        if node1 is None or node2 is None:
            raise ValueError("Invalid node1 or node2")
        # Check that node1 and node 2 has exactly 1 node between them, 
        if node1.next.next is not node2:
            # raise a ValueError if not
            raise ValueError("There must be exactly 1 node between node1 and node2")
        
        # Everything is in order, so delete the node between node1 and node2, 
        # returning the value that was stored in it 
        value_to_return = node1.next.value
        node1.next = node2
        node2.prev = node1

        #decrement size
        self.size -= 1
        return value_to_return
    
    #method that utilizes the remove_between() method and removes/returns the first value
    def remove_first(self):
        return self.remove_between(self.header, self.header.next.next)
    
    #method that utilizes the remove_between() method and removes/returns the last value
    def remove_last(self):
        return self.remove_between(self.trailer.prev.prev, self.trailer)
    
    #method that searches for a specific value in the list and returns the index, (parameter v)
    #if not found, returns -1
    def search(self, v):
        #create temporary node to step through the list
        temp = self.header.next
        #make a variable to keep track of the current index
        index = 0
        #step through the entire list
        while temp is not self.trailer:
            #if we find the value, return the index
            if temp.value == v:
                return index
            #increment the index and step to the next node
            temp = temp.next
            index += 1
        #if we exit the loop, we didn't find the value. Return -1
        return -1
    
    #method that returns the value at the given index (param i) in the list
    def get(self, i):
        #add a check to make sure the index is valid
        if i < 0 or i >= self.size:
            raise IndexError("Invalid Index")
        #step through the loop with a temp node, and make a variable to keep track of the index
        temp = self.header.next
        index = 0
        #continue to step while the index is not the passed index from the parameter
        while index != i:
            temp = temp.next
            index += 1
        #if we exit the loop, we have found the right index. Return the value at the index
        return temp.value

#a SnakeSegment object that is to be stored in each node of the linked list
class SnakeSegment:
    #construct each segment to keep track of it's position, as well as a color value
    def __init__(self, x: float, y: float, color: Color = Color(0,255,0)):
        self.x_loc = x
        self.y_loc = y
        self.color = color
    #create a draw method so that the segment can show on the canvas
    def draw(self):
        #set the pen color to the color attribute, and draw a square at the current position
        dudraw.set_pen_color(self.color)
        dudraw.filled_square(self.x_loc, self.y_loc, 0.5)

#a Snake object that will be our snake on the screen
class Snake:
    def __init__(self):
        #make the body be a DoublyLinkedList object
        self.body = DoublyLinkedList()
        #initialize the snake to start with three segments in the right-lower corner of the screen
        self.body.add_first(SnakeSegment(12.5, 8.5))
        self.body.add_last(SnakeSegment(12.5, 7.5))
        self.body.add_last(SnakeSegment(12.5, 6.5))
        #initialize the direction to be up
        self.direction = 'up'
    
    #create a draw method which draws all the segments of the snake
    def draw(self):
        #create a temp node to step through the list. start at the first value
        temp = self.body.header.next
        #step all the way through the list
        while temp is not self.body.trailer:
            #if the current node is the first value:
            if temp is self.body.header.next:
                #call the SnakeSegment's draw method, then set the pen color to red for eyes and tongue
                temp.value.draw()
                dudraw.set_pen_color(dudraw.RED)
                #check which direction the snake is going:
                #for each case, draw the snake "face" in the right orientation so it looks natural when the snake turns
                if self.direction == 'up':
                    dudraw.filled_circle(temp.value.x_loc - 0.25, temp.value.y_loc + 0.15, 0.05)
                    dudraw.filled_circle(temp.value.x_loc + 0.25, temp.value.y_loc + 0.15, 0.05)
                    dudraw.filled_rectangle(temp.value.x_loc, temp.value.y_loc + 0.8, 0.1, 0.3)
                elif self.direction == 'down':
                    dudraw.filled_circle(temp.value.x_loc - 0.25, temp.value.y_loc - 0.15, 0.05)
                    dudraw.filled_circle(temp.value.x_loc + 0.25, temp.value.y_loc - 0.15, 0.05)
                    dudraw.filled_rectangle(temp.value.x_loc, temp.value.y_loc - 0.8, 0.1, 0.3)
                elif self.direction == 'left':
                    dudraw.filled_circle(temp.value.x_loc - 0.15, temp.value.y_loc -0.25, 0.05)
                    dudraw.filled_circle(temp.value.x_loc - 0.15, temp.value.y_loc + 0.25, 0.05)
                    dudraw.filled_rectangle(temp.value.x_loc - 0.8, temp.value.y_loc, 0.3, 0.1)
                elif self.direction == 'right':
                    dudraw.filled_circle(temp.value.x_loc + 0.15, temp.value.y_loc -0.25, 0.05)
                    dudraw.filled_circle(temp.value.x_loc + 0.15, temp.value.y_loc + 0.25, 0.05)
                    dudraw.filled_rectangle(temp.value.x_loc + 0.8, temp.value.y_loc, 0.3, 0.1)
            #otherwise, draw the segment normally
            else:
                temp.value.draw()
            #after the segment is drawn, move onto the next
            temp = temp.next
    #create a move method to advance the snake one "square"
    def move(self):
        if self.direction == 'up':
            #add a segment on top of the current first segment, then remove the last segment
            self.body.add_first(SnakeSegment(self.body.first().x_loc, self.body.first().y_loc + 1))
            self.body.remove_last()
        elif self.direction == 'left':
            #add a segment to the left of the current first segment, then remove the last segment
            self.body.add_first(SnakeSegment(self.body.first().x_loc - 1, self.body.first().y_loc))
            self.body.remove_last()
        elif self.direction == 'down':
            #add a segment below the current first segment, then remove the last segment
            self.body.add_first(SnakeSegment(self.body.first().x_loc, self.body.first().y_loc - 1))
            self.body.remove_last()
        elif self.direction == 'right':
            #add a segment to the right of the current first segment, then remove the last segment
            self.body.add_first(SnakeSegment(self.body.first().x_loc + 1, self.body.first().y_loc))
            self.body.remove_last()

    #a method that determines if the snake has encountered food
    def has_found_food(self, other: Food):
        #create variables for the first segments (x,y) and the foods (x,y)
        head_x = self.body.first().x_loc
        head_y = self.body.first().y_loc
        food_x = other.x_loc
        food_y = other.y_loc
        #if the two are equal, return true
        return head_x == food_x and head_y == food_y

    #a method that grows the snake by 1 segment
    def grow(self):
        #in order to add a new segment in the correct orientation, we need to look at the last two segments and determine the change in direction
        #this allows us to know which way the last two segments are moving
        #subtract the last segment's x value from the second to last's
        change_x = self.body.trailer.prev.prev.value.x_loc - self.body.last().x_loc
        #subtract the last segment's y value from the second to last's
        change_y = self.body.trailer.prev.prev.value.y_loc - self.body.last().y_loc
        #if the y change is positive, we know we need to add the segment below the last
        if change_y > 0:
            self.body.add_last(SnakeSegment(self.body.last().x_loc, self.body.last().y_loc - 1))
        #if the x change is negative, we know we need to add a segment to the right of the last
        elif change_x < 0:
            self.body.add_last(SnakeSegment(self.body.last().x_loc + 1, self.body.last().y_loc))
        #if the y change is negative, we know we need to add the segment on top of the last
        elif change_y < 0:
            self.body.add_last(SnakeSegment(self.body.last().x_loc, self.body.last().y_loc + 1))
        #if the x change is positive, we know we need to add the segment to the left of the last
        elif change_x > 0:
            self.body.add_last(SnakeSegment(self.body.last().x_loc - 1, self.body.last().y_loc))
    
    #a method that determines if the snake has crashed
    def has_crashed(self):
        #the following checks are for if the snake has crashed into the wall:
        #make sure to add an extra check to see which direction the snake is moving, otherwise the game would end prematurely if you're near a wall
        if self.body.first().x_loc - 0.5 < 0 and self.direction == 'left':
            return True
        elif self.body.first().x_loc + 0.5 > 20 and self.direction == 'right':
            return True
        elif self.body.first().y_loc - 0.5 < 0 and self.direction == 'down':
            return True
        elif self.body.first().y_loc + 0.5 > 20 and self.direction == 'up':
            return True
        
        #now check if it has crashed into itself
        #step through the entire list
        temp = self.body.header.next.next
        while temp is not self.body.trailer:
            #if the first node's (x,y) is the same as any other node's, we know the snake has crashed into itself
            if self.body.first().x_loc == temp.value.x_loc and self.body.first().y_loc == temp.value.y_loc:
                return True
            temp = temp.next
        #if we check everything, the snake has not crashed
        return False
        
#create a class for the food object
class Food:
    #construct it to keep track of it's (x,y) position
    def __init__(self, x: float, y: float):
        self.x_loc = x
        self.y_loc = y
    #a method that draws the food on the canvas
    def draw(self):
        #set the pen color to yellow and draw a square at the current position
        dudraw.set_pen_color(dudraw.RED)
        dudraw.filled_circle(self.x_loc, self.y_loc, 0.5)
    #create a generate method that will move the food to a random location
    def generate(self):
        #achieve this by just changing the position to a random location on the grid
        self.x_loc = random.randint(1, 20) - 0.5
        self.y_loc = random.randint(1, 20) - 0.5

#provided test code to test the DoublyLinkedList class
def dll_tester():
    # create a DoublyLinkedList
    test_list = DoublyLinkedList()
    
    #testing list creation
    assert test_list.get_size()==0,   'list should be empty to start!'
    
    #testing add_first
    test_list.add_first(1)
    assert test_list.first() == 1, 'add_first needs adjustment!'
    assert test_list.last() == 1, 'add_first needs adjustment!'
    assert test_list.get_size() == 1 ,    'add_first needs adjustment!'
    test_list.add_first(2)
    assert test_list.first() == 2, 'add_first needs adjustment!'
    assert test_list.last() == 1, 'add_first needs adjustment!'
    assert test_list.get_size() == 2, 'add_first needs adjustment!'
    
    #testing add_last
    test_list.add_last(3)
    assert test_list.first() == 2,'add_last needs adjustment!'
    assert test_list.last() == 3, 'add_last needs adjustment!'
    assert test_list.get_size() == 3, 'add_last needs adjustment!'

    #test remove_first
    assert test_list.remove_first() == 2, 'remove_first needs adjustment!'
    assert test_list.first() == 1, 'remove_first needs adjustment!'
    assert test_list.last() == 3, 'remove_first needs adjustment!'
    assert test_list.get_size() == 2, 'remove_first needs adjustment!'

    #test remove_last
    assert test_list.remove_last() == 3, 'remove_last needs adjustment!'
    assert test_list.first() == 1, 'remove_last needs adjustment!'
    assert test_list.last() == 1, 'remove_last needs adjustment!'
    assert test_list.get_size() == 1, 'remove_last needs adjustment!'

    while not test_list.is_empty():
        test_list.remove_first()

    assert test_list.get_size() == 0, 'list should be empty after removing all values'    

    for i in range(10):
        test_list.add_last(i+1)
    #test get method
    assert test_list.get(0) == 1, 'get(0) should return the element at first index'
    assert test_list.get(5) == 6, 'get(1) should return the element at index 1'
    assert test_list.get(9) == 10, 'get(9) should return the element at last index'

    print('All tests passed!')

#main animation loop
dudraw.set_canvas_size(600, 600)
#create a snake object and a food object
snake = Snake()
food = Food(5.5, 16.5)
limit = 1 #number of frames to allow to pass before snake moves
timer = 0  #a timer to keep track of number of frames that passed
key = '' #create an empty key variable for our animation loop condition
score = 0 #create a score variable to keep track of the user's score
game_over = False #create a game over variable, intitialized to False, so we know when the game is over
#set the x and y scale so our world is a 20x20 grid
dudraw.set_x_scale(0, 20)
dudraw.set_y_scale(0, 20)
#continue while q has not been pressed:
while key != 'q':
    timer += 1
    #process keyboard press here
    if dudraw.has_next_key_typed():
        #get the key
        key = dudraw.next_key_typed()
        #add an extra check that only allows the snake to be moved if the game is not over.
        #this prevents the user from being able to continue after crashing
        if not game_over:
            #process w by changing direction to up. Only process when the snake is moving left/right to prevent a game over when the user accidentally turns back on theirself
            if key == 'w' and (snake.direction == 'left' or snake.direction == 'right'):
                snake.direction = "up"
            #process a by changing direction to left. Only process when the snake is moving up/down to prevent a game over when the user accidentally turns back on theirself
            if key == 'a' and (snake.direction == 'up' or snake.direction == 'down'):
                snake.direction = "left"
            #process s by changing direction to down. Only process when the snake is moving left/right to prevent a game over when the user accidentally turns back on theirself
            if key == 's' and (snake.direction == 'left' or snake.direction == 'right'):
                snake.direction = "down"
            #process d by changing direction to right. Only process when the snake is moving up/down to prevent a game over when the user accidentally turns back on theirself
            if key == 'd' and (snake.direction == 'up' or snake.direction =='down'):
                snake.direction = "right"
    #add an extra condition so that when r is pressed, the game restarts
    if key == 'r':
        #accomplish this by making a new snake, a new food, resetting the score, and making sure game_over is False
        snake = Snake()
        food = Food(5.5, 16.5)
        score = 0
        game_over = False      
    #update the world according to the timer limit to prevent the snake from being too fast   
    if timer == limit:
        #reset the timer
        timer = 0
        #clear the screen
        dudraw.clear(dudraw.BLACK)
        #add Text to the top lef to display the score
        dudraw.set_pen_color(dudraw.WHITE)
        dudraw.set_font_size(15)
        dudraw.text(1.5, 19, f"Score: {score}")
        #draw and move the snake
        snake.move()
        #check to see if snake ate the fruit
        if snake.has_found_food(food):
            #if so, the snake grows and the food moves location. Score is also incremented
            snake.grow()
            food.generate()
            score += 1
        #check if the snake has crashed
        if snake.has_crashed():
            #if so, stop the snake by making the direction None. Change game_over to True
            snake.direction = None
            game_over = True
        #if the game is over, display a game over message in the middle of the screen
        if game_over:
            dudraw.set_pen_color(dudraw.RED)
            dudraw.set_font_size(20)
            dudraw.text(10, 10, "GAME OVER")
        #draw the updated version of the snake and the food
        snake.draw()
        food.draw()
    #show the canvas
    dudraw.show(100)