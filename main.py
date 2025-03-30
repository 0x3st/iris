'''
GOAL: balance between clean code, coding style and performance
	- Efficient logic can be developed to determine if two shapes overlap, intersect, 
		or if one is contained within the other, using one or two functions. 
		However, this logic tends to be complex and challenging 
		to read and follow. Additionally, testing the logic can be difficult, 
		particularly when it comes to evaluating the internal structure of the function.
	- Instead, break down the problem into smaller sub-problems, and solve each sub-problem
		one by one, using simple and easy-to-read functions, combining the proper usage of function
		parameters to enhance reusability and maintainability, and finally integrating them
		together to produce the solution to the original problem.
	- To acheive optimal efficiency and performance, analyses the code structure and flow to ensure the correct
		order of execution and avoid unnecessary calculations.

Process: 
	Pick a random polygon shape and a color
	Stretch the chosen polygon
	Repeatedly pick a random x,y position and try to fit the choosen shape so that
		1/ it doesn't touch any other shapes
		2/ it doesn't overlap with any other shapes
		3/ it doesn't hide inside another shape
'''
import turtle
import random
import time

# global constants
YOUR_ID = 'xxxxxx'   # TODO: your student id
COLORS = ('green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown')
SHAPE_FILE = 'shapes.txt'
SCREEN_DIM_X = 0.7  # screen width factor
SCREEN_DIM_Y = 0.7  # screen height factor
XY_SPAN = 0.8       # canvas factor 
XY_STEP = 10        # step size of x,y coordinates
MIN_DURATION = 5    
MAX_DURATION = 30
MIN_STRETCH = 1
MAX_STRETCH = 10
MIN_SEED = 1
MAX_SEED = 99

# global variables
g_shapes = []       # list of polygons displayed on canvas
g_screen = None
g_range_x = None
g_range_y = None

def box(shape:turtle.Turtle) -> tuple[tuple[float, float], tuple[float, float]]:
    '''
    Calculate the bounding box of a turtle shape.
    
    Args:
        shape (turtle.Turtle): The turtle shape to calculate the bounding box for.
    
    Returns:
        tuple: A tuple containing the coordinates of the bounding box
        in the format ((x_min, x_max), (y_min, y_max)).
    '''
    shapepoly = shape.get_shapepoly()
    xs = [x for x,y in shapepoly]
    ys = [y for x,y in shapepoly]
    return (min(xs), max(xs)), (min(ys), max(ys))

def box_check(bounding_box1: tuple, bounding_box2: tuple) -> bool:
    '''
	Check if two bounding boxes overlap.
	
	Args:
        bounding_box1 (tuple): The first bounding box.
        bounding_box2 (tuple): The second bounding box.
		
	Returns:
        bool: True if the bounding boxes overlap, False otherwise.
    '''
    x1_min, x1_max = bounding_box1[0]
    y1_min, y1_max = bounding_box1[1]
    x2_min, x2_max = bounding_box2[0]
    y2_min, y2_max = bounding_box2[1]

    return not (x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min)

def is_separating_axis(poly1: list[tuple[float, float]], poly2: list[tuple[float, float]], axis: tuple[float, float]) -> bool:
    '''
    Check if the given axis is a separating axis for the two polygons.
	
    Args:
        poly1 (list[tuple[float, float]]): The first polygon represented as a list of vertices.
        poly2 (list[tuple[float, float]]): The second polygon represented as a list of vertices.
        axis (tuple[float, float]): The axis to check for separation.
		
	Return:
        bool: True if the axis is a separating axis, False otherwise.
    '''
    # calculate the projection of poly1
    min1 = max1 = poly1[0][0] * axis[0] + poly1[0][1] * axis[1]
    for point in poly1[1:]:
        projection = point[0] * axis[0] + point[1] * axis[1]
        min1 = min(min1, projection)
        max1 = max(max1, projection)
    
    # calculate the projection of poly2
    min2 = max2 = poly2[0][0] * axis[0] + poly2[0][1] * axis[1]
    for point in poly2[1:]:
        projection = point[0] * axis[0] + point[1] * axis[1]
        min2 = min(min2, projection)
        max2 = max(max2, projection)
    
    # check if the projections overlap
    return not (max1 < min2 or max2 < min1)

def get_edges(poly:list[tuple[float, float]]) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    '''
	Get all the edges of the polygon.
	
	Args:
        poly (list[tuple[float, float]]): The polygon represented as a list of vertices.
	
	Return:
        list: A list of edges represented as tuples of vertices.
	'''
    edges = []
    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i+1) % len(poly)]
        edges.append( (p1, p2) )
    return edges

def normalize(vector:tuple[float, float]) -> tuple[float, float]:
    '''
	Normalize a vector to unit length.
    
	Args:
        vector (tuple[float, float]): The vector to normalize.
		
	Return:
        tuple: The normalized vector.
	'''
    x, y = vector
    length = (x**2 + y**2)**0.5
    if length == 0:
        return (0, 0)
    return (x / length, y / length)

def get_axes(poly:list[tuple[float, float]]) -> list[tuple[float, float]]:
    '''
	Get normal vectors of each edge of the polygon.
	
	Args:
        poly (list[tuple[float, float]]): The polygon represented as a list of vertices.
		
	Return:
        list: A list of normal vectors for each edge of the polygon.
	'''
    axes = []
    for (p1, p2) in get_edges(poly):
        # vector of edge
        edge_x = p2[0] - p1[0]
        edge_y = p2[1] - p1[1]
        # normal vector
        normal = (-edge_y, edge_x)
        axes.append( normalize(normal) )
    return axes

def sat_check(poly1:list[tuple[float, float]], poly2:list[tuple[float, float]]) -> bool:
    '''
    Use SAT check to tell if two polygons are overlapping.
	
	Args:
        poly1 (list[tuple[float, float]]): The first polygon represented as a list of vertices.
        poly2 (list[tuple[float, float]]): The second polygon represented as a list of vertices.
		
	Return:
        bool: True if the polygons overlap, False otherwise.
    '''
    axes = get_axes(poly1) + get_axes(poly2)
    
    for axis in axes:
        if is_separating_axis(poly1, poly2, axis):
            return False
    return True

def ray_check(point:tuple[float, float], polygon:list[tuple[float, float]]) -> bool:
    '''
    Check if a point is inside a polygon using the ray-casting algorithm.

    Args:
        point (tuple[float, float]): The point to check, represented as (x, y).
        polygon (list[tuple[float, float]]): The polygon represented as a list of coordinates.
    
    Returns:
        bool: True if the point is inside the polygon, False otherwise.
    '''
    x, y = point
    inside = False
    n = len(polygon)
    
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i+1) % n]
    
        if (y1 > y) == (y2 > y):
            continue
            
        x_intersect = (y - y1) * (x2 - x1) / (y2 - y1) + x1
        
        if x <= x_intersect:
            inside = not inside
    
    return inside

def contains(poly1: list[tuple[float, float]], poly2:list[tuple[float, float]], tolerance=1e-6) -> bool:
    '''
    Check if polygon1 contains polygon2.

    Args:
        poly1 (list[tuple[float, float]]): The first polygon represented as a list of coordinates.
        poly2 (list[tuple[float, float]]): The second polygon represented as a list of coordinates.
    
    Return:
        bool: True if polygon1 contains polygon2, False otherwise.
    '''
    for (x, y) in poly2:
        if not ray_check((x, y), poly1):
            return False
    return True

def contain_check(poly1:list[tuple[float, float]], poly2:list[tuple[float, float]]) -> tuple[bool, bool]:
    '''
    Combines ray_check and contains functions to check if one polygon contains another.

    Args:
        poly1 (list[tuple[float, float]]): The first polygon represented as a list of coordinates.
        poly2 (list[tuple[float, float]]): The second polygon represented as a list of coordinates.
    
    Return:
        tuple: A tuple containing two boolean values:
            - True if poly1 contains poly2
            - True if poly2 contains poly1
    '''
    xs1 = [x for x,y in poly1]
    ys1 = [y for x,y in poly1]
    xs2 = [x for x,y in poly2]
    ys2 = [y for x,y in poly2]
    
    x1_min, x1_max = min(xs1), max(xs1)
    y1_min, y1_max = min(ys1), max(ys1)
    x2_min, x2_max = min(xs2), max(xs2)
    y2_min, y2_max = min(ys2), max(ys2)
    
    if (x2_min < x1_min or x2_max > x1_max or 
        y2_min < y1_min or y2_max > y1_max):
        contain_1to2 = False
    else:
        contain_1to2 = contains(poly1, poly2)
    
    if (x1_min < x2_min or x1_max > x2_max or 
        y1_min < y2_min or y1_max > y2_max):
        contain_2to1 = False
    else:
        contain_2to1 = contains(poly2, poly1)
    
    return contain_1to2, contain_2to1

def is_shape_overlapped_any(shape:turtle.Turtle, shapes:list[turtle.Turtle]) -> bool:
	'''
	TODO: check if shape is overlapped with any of the shapes
	TODO: problem decomposition, clean code, refactoring

	Args:
		shape (turtle.Turtle): The shape to check for overlap.
		shapes (list[turtle.Turtle]): List of shapes to check overlap with.
	
	Returns:
		bool: True if the shape overlaps with any shape in the list, False otherwise.
	'''
	# Pre-compute shape's polygon and bounding box to avoid recalculating
	shape_poly = shape.get_shapepoly()
	shape_bbox = box(shape)
	
	for other_shape in shapes:
		if other_shape == shape: 
			continue
			
		# Fast bounding box check first
		other_bbox = box(other_shape)
		if box_check(shape_bbox, other_bbox):
			# Only calculate polygon if bounding boxes overlap
			other_poly = other_shape.get_shapepoly()
			
			# Quick containment check using bounding box data
			xs1 = [x for x,y in shape_poly]
			ys1 = [y for x,y in shape_poly]
			xs2 = [x for x,y in other_poly]
			ys2 = [y for x,y in other_poly]
			
			x1_min, x1_max = min(xs1), max(xs1)
			y1_min, y1_max = min(ys1), max(ys1)
			x2_min, x2_max = min(xs2), max(xs2)
			y2_min, y2_max = min(ys2), max(ys2)
			
			# Check if one shape might be contained in the other
			possible_containment = ((x1_min >= x2_min and x1_max <= x2_max and 
									 y1_min >= y2_min and y1_max <= y2_max) or
									(x2_min >= x1_min and x2_max <= x1_max and 
									 y2_min >= y1_min and y2_max <= y1_max))
			
			if possible_containment:
				# Perform detailed containment check only if needed
				if contains(shape_poly, other_poly) or contains(other_poly, shape_poly):
					return True
			
			# Only perform SAT check if no containment was found
			elif sat_check(shape_poly, other_poly):
				return True
	
	return False

############################################
################## template ################
############################################

def create_shape(shape:turtle.Turtle, color:str, sz_x:int = 1, sz_y:int = 1) -> turtle.Turtle:
	'''
	Create a turtle shape with specified parameters.
	
	Args:
		shape (turtle.Turtle): The base shape for the turtle.
		color (str): The color to set for the turtle.
		sz_x (int, optional): Horizontal stretch factor for the shape. Defaults to 1.
		sz_y (int, optional): Vertical stretch factor for the shape. Defaults to 1.
	
	Returns:
		turtle.Turtle: A configured turtle object with specified shape, color, and size.
	'''
	t = turtle.Turtle(shape)
	t.up()
	t.color(color)
	t.shapesize(sz_y, sz_x)
	return t

def get_random_home_position(range_x:list[int], range_y:list[int]) -> tuple[int,int]:
	'''
	Generates a random (x, y) coordinate tuple by sampling from 
	the provided x and y coordinate ranges.
	
	Args:
		range_x (list[int]): A list of possible x-coordinate values to sample from.
		range_y (list[int]): A list of possible y-coordinate values to sample from.
	
	Returns:
		tuple[int, int]: A randomly selected (x, y) coordinate pair.
	'''
	x = random.sample(range_x, 1)[0]
	y = random.sample(range_y, 1)[0]   
	return (x,y)

def place_a_random_shape(shape:turtle.Turtle, started:float, duration:int) -> None:
	'''
	Repeatedly tries to place the given shape at random coordinates 
	within the predefined canvas range.
	If the shape does not overlap with existing shapes, 
	it is added to the global shapes list and the screen is updated.
	
	Args:
		shape (turtle.Turtle): The turtle shape to be placed on the canvas.
		started (float): The timestamp when the placement process began.
		duration (int): The maximum time allowed for attempting to place the shape.
	'''
	while time.time() - started <= duration:
		x, y = get_random_home_position(g_range_x, g_range_y)
		shape.goto(x, y)
		if is_shape_overlapped_any(shape, g_shapes) is False:
			g_shapes.append(shape)
			g_screen.title(f'{YOUR_ID} - {len(g_shapes)}')
			g_screen.update()
			break

def fill_canvas_with_random_shapes(shapes:list[turtle.Turtle], colors:list[str], 
						 stretch_factor:int, duration:int) -> float:
	'''
	Fills the canvas with randomly positioned and colored shapes 
	within a specified time duration.
	
	Args:
		shapes (list[turtle.Turtle]): A list of available polygon shapes to choose from.
		colors (list[str]): A list of available colors to apply to the shapes.
		stretch_factor (int): The factor by which to stretch the shapes.
		duration (int): The maximum time allowed for placing shapes.
	
	Returns:
		float: The timestamp when the shape placement process started.
	'''
	started = time.time()
	while time.time() - started <= duration:
		shape = random.sample(shapes,1)[0]
		color = random.sample(colors,1)[0]
		turtle_obj = create_shape(shape, color, stretch_factor, stretch_factor)
		place_a_random_shape(turtle_obj, started, duration)

	return started


def import_custom_shapes(file_name:str) -> list[str]:
	'''
	Import custom turtle shapes from a file with predefined shape names and coordinates,
	where each line contains a shape name and its coordinates separated by a colon.
	
	Add each shape to the turtle screen and returns a list of imported shape names.

	Args:
		file_name (str): Path to the file containing custom shape definitions.

	Returns:
		list[str]: A list of names of the imported custom shapes.
	'''
	shapes = []
	with open(file_name, 'r') as f:
		for line in f.readlines():
			if line.find(':') == -1:
				continue
			name, coordinates = line.split(':')
			coordinates = eval(coordinates) # ok for internal use
			g_screen.addshape(name, coordinates)
			shapes.append(name)

	return shapes
	

def setup_canvas_ranges(w:int, h:int, span:float=0.8, step:int=10) -> tuple[list[int], list[int]]:
	'''
	Calculate valid coordinate ranges for canvas placement.
	
	Args:
		w (int): Canvas width.
		h (int): Canvas height.
		span (float, optional): Proportion of canvas to use. Defaults to 0.8.
		step (int, optional): Increment between coordinate values. Defaults to 10.
	
	Returns:
		tuple[list[int], list[int]]: A tuple containing x and y coordinate ranges, 
		centered at (0,0) within the specified canvas span.
	'''
	sz_w, sz_h = int(w/2*span), int(h/2*span)
	return range(-sz_w, sz_w, step), range(-sz_h, sz_h, step)

def setup_screen() -> turtle.Screen:
	'''
	Initialize and configure a turtle graphics screen with specific settings.

	Sets up a screen with auto-refresh disabled, predefined dimensions, 
	and logo mode orientation to prevent custom shape rotation.

	Returns:
		turtle.Screen: A configured turtle graphics screen ready for drawing.
	'''
	scrn = turtle.Screen()
	scrn.tracer(0)  # disable auto refresh
	scrn.setup(SCREEN_DIM_X, SCREEN_DIM_Y, starty=10)
	scrn.mode("logo") # heading up north to avoid rotation of custom shapes

	return scrn

def get_time_str(time_sec) -> str:
	'''
	Convert a timestamp in seconds to a formatted time string.

	Args:
		time_sec (float): The timestamp in seconds since the epoch.

	Returns:
		str: A formatted time string in "HH:MM:SS" format.
	'''
	struct_time = time.localtime(time_sec)
	return time.strftime("%H:%M:%S", struct_time)

def show_result(started:float, count:int) -> None:
	'''
	Display the final results of the drawing process, 
	including student ID, start and end times, duration, and shape count.
	
	Args:
		started (float): The timestamp when the drawing process began.
		count (int): The total number of shapes drawn during the process.
	
	Side effects:
		- Updates the screen title with ID, timing and count information
		- Changes screen background color to black
		- Prints student ID and shape count to console
	'''
	ended = time.time()	# end time 
	start_time = get_time_str(started)
	end_time = get_time_str(ended)
	diff = round(ended-started,2)

	g_screen.title(f'{YOUR_ID} {start_time} - {end_time} - {diff} - {count}')
	g_screen.bgcolor('black')
	print(f'{YOUR_ID},{count}')	# output your student id and shape count

def prompt(prompt:str, default:any) -> str:
	'''
	Prompts the user for input with a default value.
	
	Args:
		prompt (str): The input prompt message to display.
		default (any): The default value to return if no input is provided.
	
	Returns:
		str: The user's input, or the default value if no input is given.
	'''
	ret = input(f'{prompt} (default is {default}) >')
	return default if ret == "" else ret

def prompt_input() -> tuple[int,int,int,str]:
	'''
	Interactively prompt the user for drawing configuration parameters.
	
	Prompts for and validates user inputs for:
	- Minimum shape stretch value
	- Random seed for reproducibility
	- Drawing duration
	- Termination preference
	
	Returns:
		tuple[int,int,int,str]: A tuple containing (min_stretch, seed, duration, termination)
		with each value validated against predefined constraints.
	
	Raises:
		AssertionError: If any input value is outside its allowed range.
	'''
	min_stretch = int(prompt("Stretch Value", 1))
	assert MIN_STRETCH <= min_stretch <= MAX_STRETCH, \
		f"Stretch Value out of range {MIN_STRETCH} - {MAX_STRETCH}"
	
	seed = int(prompt("Random Seed", 1))
	assert MIN_SEED <= seed <= MAX_SEED, \
		f"Invalid Random Seed out of range {MIN_SEED} - {MAX_SEED}"
	
	duration = int(prompt("Duration (s)", 5))
	assert MIN_DURATION <= duration <= MAX_DURATION, \
		f"Invalid Duration out of range {MIN_DURATION} - {MAX_DURATION}"
	
	termination = prompt("Terminate", 'n')
	assert termination in ('y', 'n'), "Invalid Termination, must be y or n"

	return min_stretch, seed, duration, termination

def main() -> None:
	'''
	Main function to orchestrate the polygon drawing process.
	
	Configures the screen and canvas, imports custom shapes, prompts user for drawing parameters,
	initializes random seed, fills canvas with random shapes, and handles optional termination.
	
	Global variables are used to manage screen and drawing range state.
	
	Args:
		None
	
	Returns:
		None
	'''
	global g_screen, g_range_x, g_range_y
   
	g_screen = setup_screen()

	g_range_x, g_range_y = setup_canvas_ranges(g_screen.window_width(), 
											   g_screen.window_height(),
											   XY_SPAN, XY_STEP)
	
	shapes = import_custom_shapes(SHAPE_FILE)

	min_stretch, seed, duration, termination = prompt_input()

	random.seed(seed)

	started = fill_canvas_with_random_shapes(shapes, COLORS, min_stretch, duration)
	
	show_result(started, len(g_shapes))
	
	if termination == 'y':
		turtle.bye()

if __name__ == '__main__':
	main()
	g_screen.mainloop()

