# Shape Placement Optimizer

A Python-based tool for optimizing the placement of shapes within a given area, maximizing density while preventing overlaps. This project implements an efficient algorithm for placing various types of shapes (circles, rectangles, triangles, and polygons) in a way that minimizes wasted space.

## Features

- Support for multiple shape types:
  - Circles
  - Rectangles
  - Triangles
  - Polygons
- Efficient overlap detection using a two-phase approach:
  - Quick bounding box check
  - Precise shape-specific overlap detection
- Density optimization through strategic placement algorithms
- Visualization of placed shapes
- Configurable parameters for shape generation and placement

## Requirements

- Python 3.x
- Required packages:
  - numpy
  - matplotlib
  - shapely

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd shape-placement-optimizer
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Import the necessary modules:
```python
from shape_placement import ShapePlacement
```

2. Create a shape placement instance:
```python
placement = ShapePlacement(width=1000, height=1000)
```

3. Add shapes with desired parameters:
```python
# Add a circle
placement.add_shape('circle', radius=50)

# Add a rectangle
placement.add_shape('rectangle', width=100, height=50)

# Add a triangle
placement.add_shape('triangle', side_length=80)

# Add a polygon
placement.add_shape('polygon', num_sides=6, radius=60)
```

4. Place the shapes:
```python
placement.place_shapes()
```

5. Visualize the results:
```python
placement.visualize()
```

## Algorithm Details

The shape placement algorithm uses a two-phase approach for efficient overlap detection:

1. **Bounding Box Check**: A quick initial check using axis-aligned bounding boxes to eliminate obvious non-overlapping cases.
2. **Precise Overlap Detection**: Detailed shape-specific checks for potential overlaps that passed the bounding box test.

The placement strategy aims to maximize density by:
- Starting from the center and moving outward
- Using a spiral pattern for initial placement
- Adjusting positions based on local density
- Implementing a grid-based approach for efficient neighbor detection

## Performance Considerations

The implementation includes several optimizations:
- Grid-based spatial partitioning for faster neighbor detection
- Efficient overlap detection algorithms for each shape type
- Parallel processing capabilities for large numbers of shapes
- Memory-efficient data structures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your chosen license]

## Contact

[Your contact information]
