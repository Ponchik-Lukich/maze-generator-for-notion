from PIL import Image
import numpy as np

# Load the PNG image
maze_image = Image.open("maze2.jpg")

# Convert the image to a numpy array
maze_array = np.array(maze_image)

# Get the size of the image
height, width, _ = maze_array.shape

# Create an empty matrix to represent the maze
maze_matrix = np.zeros((height, width), dtype=int)

# Iterate over the pixels in the image and set the corresponding value in the matrix
for y in range(height):
    for x in range(width):
        pixel = maze_array[y, x]
        if np.array_equal(pixel, [0, 0, 0, 255]):
            maze_matrix[y, x] = 1
        else:
            maze_matrix[y, x] = 0

# Calculate the new size of the maze
size = 2
while size * 14 + (size - 1) * 2 + 4 != width:
    size += 1
size = size + size - 1

# Create a new maze-matrix of size*size
new_maze_matrix = np.zeros((size, size), dtype=int)

# Cut the first 2 rows and 2 last rows and 2 first columns and 2 last columns from the maze_matrix
cut_maze_matrix = maze_matrix[2:height-2, 2:width-2]
# print(cut_maze_matrix[1, 46])
# for row in cut_maze_matrix:
#     print(row)

# Cycle cutted maze_matrix
for y in range(size):
    for x in range(size):
        if x % 2 == 0 and y % 2 == 0:
            new_maze_matrix[y, x] = cut_maze_matrix[(y//2) * 16, (x//2) * 16]
        elif x % 2 == 0 and y % 2 == 1:
            new_maze_matrix[y, x] = cut_maze_matrix[(y//2 + 1) * 16 - 1, x//2 * 16]
        elif x % 2 == 1 and y % 2 == 0:
            new_maze_matrix[y, x] = cut_maze_matrix[y//2 * 16, (x//2 + 1) * 16 - 1]
        else:
            new_maze_matrix[y, x] = cut_maze_matrix[(y//2 + 1) * 16 - 1, (x//2 + 1) * 16 - 1]

print("width: ", width)
print("height: ", height)
print("size: ", size)

# add one row above and one row below and one column left and one column right with 1
new_maze_matrix = np.insert(new_maze_matrix, 0, 1, axis=0)
new_maze_matrix = np.insert(new_maze_matrix, size + 1, 1, axis=0)
new_maze_matrix = np.insert(new_maze_matrix, 0, 1, axis=1)
new_maze_matrix = np.insert(new_maze_matrix, size + 1, 1, axis=1)

if len(new_maze_matrix) % 2 == 0:
    new_maze_matrix[0, len(new_maze_matrix) // 2 - 1] = 0
    new_maze_matrix[len(new_maze_matrix)-1, len(new_maze_matrix)//2 + 1] = 0
else:
    new_maze_matrix[0, len(new_maze_matrix) // 2] = 0
    new_maze_matrix[len(new_maze_matrix)-1, len(new_maze_matrix)//2] = 0

# print new_maze_matrix
for row in new_maze_matrix:
    print(row)

# Create a new image with the same size as the matrix
maze_image = Image.new("RGB", (width, height), color="white")

# Iterate over the cells in the matrix and set the corresponding pixels in the image
for y in range(height):
    for x in range(width):
        if maze_matrix[y, x] == 1:
            maze_image.putpixel((x, y), (0, 0, 0))
        else:
            maze_image.putpixel((x, y), (255, 255, 255))

maze_image.save("result.png")