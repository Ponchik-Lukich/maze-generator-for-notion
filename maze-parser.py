from PIL import Image

# Load the PNG image
maze_image = Image.open("maze2.jpg")

# Get the size of the image
width, height = maze_image.size

# Create an empty matrix to represent the maze
maze_matrix = [[0 for x in range(width)] for y in range(height)]

# Iterate over the pixels in the image and set the corresponding value in the matrix
for y in range(height):
    for x in range(width):
        pixel = maze_image.getpixel((x, y))
        if pixel == (0, 0, 0, 255):
            maze_matrix[y][x] = 1
        else:
            maze_matrix[y][x] = 0

# merge white pixels in one line in the matrix

for row in maze_matrix:
    print (row)


width = len(maze_matrix[0])
height = len(maze_matrix)
print("width: ", width)
print("height: ", height)

# Create a new image with the same size as the matrix
maze_image = Image.new("RGB", (width, height), color="white")

# Iterate over the cells in the matrix and set the corresponding pixels in the image
for y in range(height):
    for x in range(width):
        if maze_matrix[y][x] == 1:  # Wall cell
            maze_image.putpixel((x, y), (0, 0, 0))
        else:  # Path cell
            maze_image.putpixel((x, y), (255, 255, 255))

# Save the image as a PNG file
maze_image.save("result.png")