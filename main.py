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
YOUR_ID = '124020372'   # TODO: your student id
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

def is_shape_overlapped_any(shape:turtle.Turtle, shapes:list[turtle.Turtle]) -> bool:
	'''
	Check if shape is overlapped with any of the shapes in the list.
	Uses problem decomposition by checking for various overlap conditions.

	Args:
		shape (turtle.Turtle): The shape to check for overlap.
		shapes (list[turtle.Turtle]): List of shapes to check overlap with.
	
	Returns:
		bool: True if the shape overlaps with any shape in the list, False otherwise.
	'''
	# Handle edge cases
	if is_empty_or_self_check(shape, shapes):
		return False
	
	# Get shape bounds
	shape_bounds = get_shape_bounds(shape)
	
	# Check against each existing shape
	for existing_shape in shapes:
		# Quick distance check first for efficiency
		if not are_shapes_potentially_overlapping(shape, existing_shape):
			continue
		
		# Get bounds of existing shape
		existing_bounds = get_shape_bounds(existing_shape)
		
		# Check for overlap or containment
		if is_bounds_overlap(shape_bounds, existing_bounds) or is_one_bound_inside_other(shape_bounds, existing_bounds):
			return True
	
	# No overlap found
	return False

def is_empty_or_self_check(shape:turtle.Turtle, shapes:list[turtle.Turtle]) -> bool:
	'''
	Check if the shapes list is empty or if we're checking against the shape itself.
	
	Args:
		shape (turtle.Turtle): The shape being checked.
		shapes (list[turtle.Turtle]): List of shapes to check against.
		
	Returns:
		bool: True if the list is empty or the shape is in the list, False otherwise.
	'''
	return not shapes or shape in shapes

def are_shapes_potentially_overlapping(shape1:turtle.Turtle, shape2:turtle.Turtle) -> bool:
	'''
	Quick check to see if two shapes are even close enough to potentially overlap.
	This is a performance optimization to avoid more expensive calculations.
	
	Args:
		shape1 (turtle.Turtle): First shape to check.
		shape2 (turtle.Turtle): Second shape to check.
		
	Returns:
		bool: True if shapes are close enough to potentially overlap.
	'''
	# Get center positions
	x1, y1 = shape1.xcor(), shape1.ycor()
	x2, y2 = shape2.xcor(), shape2.ycor()
	
	# Get shape dimensions
	w1, h1 = get_shape_dimensions(shape1)
	w2, h2 = get_shape_dimensions(shape2)
	
	# Calculate maximum possible distance for overlap
	max_distance_x = (w1 + w2) / 2
	max_distance_y = (h1 + h2) / 2
	
	# Check if they're too far apart
	return abs(x1 - x2) <= max_distance_x and abs(y1 - y2) <= max_distance_y

def get_shape_bounds(shape:turtle.Turtle) -> tuple[float, float, float, float]:
	'''
	Get the bounds (left, right, bottom, top) of a shape.
	
	Args:
		shape (turtle.Turtle): The shape to get bounds for.
		
	Returns:
		tuple[float, float, float, float]: The bounds as (left, right, bottom, top).
	'''
	x, y = shape.xcor(), shape.ycor()
	width, height = get_shape_dimensions(shape)
	half_width, half_height = width/2, height/2
	
	# Calculate the bounds
	left = x - half_width
	right = x + half_width
	bottom = y - half_height
	top = y + half_height
	
	return (left, right, bottom, top)

def get_shape_dimensions(shape:turtle.Turtle) -> tuple[float, float]:
	'''
	Get the width and height of a shape based on its stretch factors.
	
	Args:
		shape (turtle.Turtle): The shape to get dimensions for.
		
	Returns:
		tuple[float, float]: A tuple containing (width, height) of the shape.
	'''
	# Get shape's stretch factors
	stretch_wid, stretch_len, _ = shape.shapesize()
	
	# Get base dimensions based on shape type
	base_width, base_height = get_base_dimensions(shape)
	
	# Calculate actual dimensions
	width = base_width * stretch_len
	height = base_height * stretch_wid
	
	return width, height

def get_base_dimensions(shape:turtle.Turtle) -> tuple[float, float]:
	'''
	Get the base dimensions for a shape based on its type.
	
	Args:
		shape (turtle.Turtle): The shape to get base dimensions for.
		
	Returns:
		tuple[float, float]: Base width and height of the shape.
	'''
	shape_name = shape.shape()
	
	# For standard shapes
	if shape_name == 'circle':
		return 20, 20
	elif shape_name == 'square':
		return 20, 20
	elif shape_name == 'triangle':
		return 20, 20
	elif shape_name == 'classic': # Arrow shape
		return 20, 20
	
	# For custom shapes from the shapes.txt file
	if '_rect' in shape_name:
		return 30, 30  # Rectangles
	elif '_star' in shape_name:
		return 45, 45  # Stars (larger)
	
	# Default for other shapes
	return 30, 30

def is_bounds_overlap(bounds1:tuple[float, float, float, float], 
				  bounds2:tuple[float, float, float, float]) -> bool:
	'''
	Check if two bounds overlap.
	
	Args:
		bounds1 (tuple): First bounds (left, right, bottom, top).
		bounds2 (tuple): Second bounds (left, right, bottom, top).
		
	Returns:
		bool: True if the bounds overlap, False otherwise.
	'''
	left1, right1, bottom1, top1 = bounds1
	left2, right2, bottom2, top2 = bounds2
	
	# Check if bounds don't overlap on x-axis
	if right1 < left2 or right2 < left1:
		return False
	
	# Check if bounds don't overlap on y-axis
	if top1 < bottom2 or top2 < bottom1:
		return False
	
	# If we reach here, the bounds overlap
	return True

def is_one_bound_inside_other(bounds1:tuple[float, float, float, float], 
						  bounds2:tuple[float, float, float, float]) -> bool:
	'''
	Check if one bound is completely inside the other.
	
	Args:
		bounds1 (tuple): First bounds (left, right, bottom, top).
		bounds2 (tuple): Second bounds (left, right, bottom, top).
		
	Returns:
		bool: True if one bound is inside the other, False otherwise.
	'''
	# Check if bounds1 is inside bounds2
	is_bounds1_inside_bounds2 = is_bound_inside_another(bounds1, bounds2)
	
	# Check if bounds2 is inside bounds1
	is_bounds2_inside_bounds1 = is_bound_inside_another(bounds2, bounds1)
	
	return is_bounds1_inside_bounds2 or is_bounds2_inside_bounds1

def is_bound_inside_another(inner:tuple[float, float, float, float], 
					   outer:tuple[float, float, float, float]) -> bool:
	'''
	Check if the inner bound is completely inside the outer bound.
	
	Args:
		inner (tuple): Inner bounds (left, right, bottom, top).
		outer (tuple): Outer bounds (left, right, bottom, top).
		
	Returns:
		bool: True if inner is inside outer, False otherwise.
	'''
	left_in, right_in, bottom_in, top_in = inner
	left_out, right_out, bottom_out, top_out = outer
	
	# Check if all edges of inner are inside outer
	return (left_in >= left_out and 
			right_in <= right_out and 
			bottom_in >= bottom_out and 
			top_in <= top_out)

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
