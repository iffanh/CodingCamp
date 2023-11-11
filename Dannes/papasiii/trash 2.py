depth = 1500
depth_list = []
for y in range (depth, -150, -150):
    step = y
    delta_y = depth - y
    depth_list.append(delta_y)
print(depth_list)