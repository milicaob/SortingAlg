import enum
import re
from turtle import left
import pygame
import random
import math
import time

pygame.init()

class Program:
    #defining colors that are used in this program
    
    PINKS = [
        (255, 204, 255),
        (255, 153, 255),
    ]
    
    BLACK = 0,0,0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    PURPLE = 102, 0, 102
    
    #fonts for the program
    FONT1 = pygame.font.SysFont('msgothic', 13)
    FONT2 = pygame.font.SysFont('msgothic', 30)

    #paddings on the side and top padding
    SIDE = 100
    TOP = 150

    def __init__(self, width, height, curr_list):
        """inicijalizacija

       
        curr_list (lista): random list that we need to generate
        """
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))

        pygame.display.set_caption("SortingAlg")
        self.set_list(curr_list)

    def set_list(self, curr_list):
        
        
        self.curr_list = curr_list
        self.v_min = min(curr_list)
        self.v_max = max(curr_list)
        
        #one pink block that defines one number 
        self.num_width = round((self.width - self.SIDE) / len(curr_list))
        self.num_height = math.floor((self.height - self.TOP) / (self.v_max - self.v_min)) #lower value
        self.low_coord = self.SIDE // 2

def draw(p_information, algorithm_name, time, expl):
    
    p_information.window.fill(p_information.WHITE)
    
    
    #title of the alghoritm that we is currently on
    title = p_information.FONT2.render(f"{algorithm_name}", 1, p_information.PURPLE)
    p_information.window.blit(title, (p_information.width/2 - title.get_width()/2 , 5))
    
    explanation = p_information.FONT1.render(f"{expl}", 1, p_information.BLACK)
    p_information.window.blit(explanation, (p_information.width/2 - explanation.get_width()/2, 40))
    
    #options for the program
    options1 = p_information.FONT1.render("Reset -> R", 1, p_information.BLACK)
    p_information.window.blit(options1, (p_information.width - options1.get_width() - p_information.SIDE//4,75))
    options2 = p_information.FONT1.render("Sort -> SPACE", 1, p_information.BLACK)
    p_information.window.blit(options2, (p_information.width - options2.get_width() - p_information.SIDE//4,90))
    
    
    sorting1 = p_information.FONT1.render("Insertion Sort -> I", 1, p_information.BLACK)
    p_information.window.blit(sorting1, (p_information.SIDE//4,75))
    sorting2 = p_information.FONT1.render("BubbleSort     -> B", 1, p_information.BLACK)
    p_information.window.blit(sorting2, (p_information.SIDE//4,90))
    sorting3 = p_information.FONT1.render("SelectionSort  -> S", 1, p_information.BLACK)
    p_information.window.blit(sorting3, (p_information.SIDE//4,105))
    sorting4 = p_information.FONT1.render("Merge Sort     -> M", 1, p_information.BLACK)
    p_information.window.blit(sorting4, (p_information.SIDE//4,120))
    sorting5 = p_information.FONT1.render("Quick Sort     -> Q", 1, p_information.BLACK)
    p_information.window.blit(sorting5, (p_information.SIDE//4,135))
    
    if time != 0:
        tm = round(time, 2)
        t = p_information.FONT1.render(f"Time of execution: {tm} seconds", 1, p_information.RED)
        p_information.window.blit(t, (p_information.width/2 - t.get_width()/2 ,100))
    
    number_drawing(p_information)
    pygame.display.update()
    
def number_drawing(p_information, color_positions={}, c_bg = False):
    curr_list = p_information.curr_list
    
    if c_bg:
        clear_rect = (p_information.SIDE//2, p_information.TOP, 
                      p_information.width - p_information.SIDE, p_information.height - p_information.TOP)
        pygame.draw.rect(p_information.window, p_information.WHITE, clear_rect)
    
    for i, val in enumerate(curr_list):
        x = p_information.low_coord + i * p_information.num_width
        y = p_information.height - (val - p_information.v_min) * p_information.num_height
        color = p_information.PINKS[i % 2]
        
        if i in color_positions:
            color = color_positions[i]
        
        pygame.draw.rect(p_information.window, color, (x,y, p_information.num_width, p_information.height))

    if c_bg:
        pygame.display.update()

def generate_starting_list(n, v_min, v_max):
    curr_list = []

    for _ in range(n):
        val = random.randint(v_min, v_max)
        curr_list.append(val)

    return curr_list

def bubble_sort(p_information):
    curr_list = p_information.curr_list
    
    for i in range(len(curr_list) - 1):
        for j in range(len(curr_list) - 1 - i):
            num1 = curr_list[j]
            num2 = curr_list[j + 1]
            if num1 > num2:
                curr_list[j], curr_list[j + 1] = curr_list[j+1], curr_list[j]
                #ovde su crno i ljubicasto dva uzastopna koja se medjusobno porede i trazi se veci
                number_drawing(p_information, {j: p_information.BLACK, j+1: p_information.PURPLE}, True)
                yield True
    
    return curr_list

def selection_sort(p_information):
    curr_list = p_information.curr_list
    for i in range(len(curr_list)):
        min = i
        
        for j in range(i+1,len(curr_list)):
            if curr_list[j] < curr_list[min]:
                min = j
        number_drawing(p_information, {i: p_information.PURPLE, min: p_information.BLACK}, True)
        (curr_list[i], curr_list[min]) = (curr_list[min], curr_list[i])
        
        yield True
        
    return curr_list

def insertion_sort(p_information):
    curr_list = p_information.curr_list
    for i in range(1, len(curr_list)):
        key_elem = curr_list[i]  #1
        h = i - 1
        #as long as the i-element is smaller than the elements that we are examining, we are pushing it left
        #key element is i-element
        #first time that i-element is bigger than h-element, it means that i-element should be to the right of the h-element and 
        while h >= 0 and key_elem < curr_list[h]:
            curr_list[h+1] = curr_list[h]
            h = h - 1
            
        curr_list[h + 1] = key_elem
        #key element je ljubicast koji se menja sa h+1 elementom liste koji je prvi element koji je desno od jedinog elementa koji je manji od key elementa 
        number_drawing(p_information, {key_elem: p_information.PURPLE, h+1: p_information.BLACK}, True)
        yield True
        
    return curr_list

def merge_sort(p_information):
    array = p_information.curr_list

    width = 1    
    n = len(array)                                          
    while (width < n):
        #starting is from the left
        left=0;
        while (left < n): 
            right= min(left+(width*2-1), n-1)         
            middle= min(left+width-1,n-1)        
            merge(array, left, middle, right)
            left += width*2
        width *= 2
        p_information.curr_list = array
        number_drawing(p_information, {middle: p_information.BLACK}, True)    
        yield True
    return array
    
def merge(array, left, middle,right): 
    n1 = middle- left + 1
    n2 = right- middle
    L = [0] * n1 
    R = [0] * n2 
    for i in range(0, n1): 
        L[i] = array[left + i] 
    for i in range(0, n2): 
        R[i] = array[middle+ i + 1] 
  
    i, j, k = 0, 0, left 
    while i < n1 and j < n2: 
        if L[i] <= R[j]: 
            array[k] = L[i] 
            i += 1
        else: 
            array[k] = R[j]
            j += 1
        k += 1
  
    while i < n1: 
        array[k] = L[i] 
        i += 1
        k += 1
  
    while j < n2: 
        array[k] = R[j] 
        j += 1
        k += 1

def partition_alg(p_information, left, right):
    curr_list = p_information.curr_list
    i = (left - 1)
    a = curr_list[right]
    for j in range(left, right):
        if curr_list[j] <= a:
            i+=1
            curr_list[i], curr_list[j] = curr_list[j], curr_list[i]
            
    curr_list[i+1], curr_list[right] = curr_list[right], curr_list[i+1]
    return (i+1)

def quick_sort(p_information):
    curr_list = p_information.curr_list
    
    left = 0
    right = len(curr_list)-1
    
    num = right - left + 1
    s = num * [0]
  
    s[0] = left
    s[1] = right
    
    r = 1
    while r >= 0:
        
        right = s[r]
        r-=1
        left = s[r]
        r-=1
        
        pivot = partition_alg(p_information, left, right)
        
        #pivot is to the right of the left side
        if pivot > left + 1:
            r+=1
            s[r] = left
            
            r+=1
            s[r] = pivot - 1
            
        if pivot < right - 1:
            r+=1
            s[r] = pivot + 1
            
            r+=1
            s[r] = right
        number_drawing(p_information, {pivot: p_information.BLACK}, True)    
        yield True

def main():

    run = True
    clock = pygame.time.Clock()

    n = 80
    v_min = 0
    v_max = 100

    curr_list = generate_starting_list(n, v_min, v_max)
    p_information = Program(1080, 720, curr_list)
    sorting = False

    speed = 20
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None    
    ind = 0
    t = 0
    expl = ""
    while run:
        
        clock.tick(5)
        
        if sorting and ind == 0:
            ind = 1
            start_time = time.time()
            
        if not sorting and ind == 1:
            ind = 0
            t = (time.time() - start_time)
            draw(p_information, sorting_algorithm_name,t,expl)
            
        
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(p_information, sorting_algorithm_name,t, expl)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type != pygame.KEYDOWN:
                continue
    
            if event.key == pygame.K_r:
                curr_list = generate_starting_list(n, v_min, v_max)
                p_information.set_list(curr_list)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(p_information)
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection Sort"
                expl = "BLACK is minimum of the elements to the right of the PURPLE element"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
                expl = "BLACK and PURPLE elements are two adjacent elements which are compared"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
                expl = "BLACK element is the first one on the left side that is smaller from the PURPLE key element"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algorithm_name = "Merge Sort"
                expl = "BLACK is the middle element that divides array to two arrays"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algorithm_name = "Quick Sort"
                expl = "BLACK is pivot"
                              
    pygame.quit()


if __name__ == "__main__":
    main()

