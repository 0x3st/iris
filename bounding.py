import random
import turtle

class ShapeSimulator:
    def __init__(self, stretch_wid=1, stretch_len=1):
        # 模拟turtle的shapesize参数
        self.stretch_wid = stretch_wid  # 垂直拉伸
        self.stretch_len = stretch_len  # 水平拉伸
        self.x = 0
        self.y = 0
    
    def goto(self, x, y):
        self.x = x
        self.y = y

def get_bounding_box(shape):
    """计算形状的精确边界框"""
    base_size = 20  # 默认形状尺寸
    width = shape.stretch_len * base_size
    height = shape.stretch_wid * base_size
    
    left = shape.x - width/2
    right = shape.x + width/2
    top = shape.y + height/2
    bottom = shape.y - height/2
    
    return (top, right, bottom, left)

def is_overlap(shape1, shape2):
    """优化后的精确碰撞检测"""
    box1 = get_bounding_box(shape1)
    box2 = get_bounding_box(shape2)
    
    # X轴分离检测
    if box1[1] < box2[3] or box1[3] > box2[1]:
        return False
    
    # Y轴分离检测
    if box1[2] > box2[0] or box1[0] < box2[2]:
        return False
    
    return True

def visualize_boxes(shape1, shape2):
    """可视化边界框（控制台版）"""
    box1 = get_bounding_box(shape1)
    box2 = get_bounding_box(shape2)
    
    print(f"Shape1 Box: Top={box1[0]:.1f}, Right={box1[1]:.1f}, Bottom={box1[2]:.1f}, Left={box1[3]:.1f}")
    print(f"Shape2 Box: Top={box2[0]:.1f}, Right={box2[1]:.1f}, Bottom={box2[2]:.1f}, Left={box2[3]:.1f}")

# 测试用例
def test_case(pos1, pos2, stretch1, stretch2, expected):
    """运行单个测试用例"""
    s1 = ShapeSimulator(stretch1[0], stretch1[1])
    s1.goto(*pos1)
    
    s2 = ShapeSimulator(stretch2[0], stretch2[1])
    s2.goto(*pos2)
    
    print(f"\n=== Test Case {'PASS' if is_overlap(s1, s2)==expected else 'FAIL'} ===")
    print(f"Shape1: Position {pos1}, Stretch {stretch1}")
    print(f"Shape2: Position {pos2}, Stretch {stretch2}")
    visualize_boxes(s1, s2)
    print(f"Expected: {expected}, Actual: {is_overlap(s1, s2)}")

# 运行测试
if __name__ == "__main__":
    # 基础测试用例
    test_case((0,0), (30,0), (1,1), (1,1), False)   # 完全分离
    test_case((0,0), (15,0), (1,1), (1,1), True)    # 刚好接触
    test_case((0,0), (0,0), (1,1), (1,1), True)      # 完全重合
    
    # 拉伸测试
    test_case((0,0), (25,0), (1,2), (1,1), True)     # 横向拉伸后的重叠
    test_case((0,0), (0,15), (2,1), (1,1), True)     # 纵向拉伸后的接触
    
    # 复杂案例
    test_case((10,10), (15,15), (1,3), (2,2), True)  # 斜向重叠
    test_case((30,30), (50,50), (1,1), (1,1), False) # 对角分离