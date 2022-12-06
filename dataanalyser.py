import csv
from sys import argv

import matplotlib.pyplot as plt
import numpy as np

dict = {
    'A': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'B': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'C': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'D': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'E': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'F': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'G': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'H': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'I': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'J': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'K': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'L': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'M': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'N': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'O': {'asd': [0, 0, 0], 'control': [0, 0, 0]},
    'P': {'asd': [0, 0, 0], 'control': [0, 0, 0]}
}


def populateDict(file1, file2, new_grid, asd_checker_list, control_checker_list, seg_size):
    person_count = 0
    # Open asd.txt
    with open(file1) as asd_file:
        # Read lines
        lines = csv.reader(asd_file)
        # Ignores first line since it contains the headers
        next(lines)
        for line in lines:
            # Copy line into separate list in order to perform operations on it
            asd_fixation_list = line.copy()
            if int(asd_fixation_list[0]) == 0:
                person_count += 1
            # Find the position of fixation
            pos_x = int(asd_fixation_list[1]) // seg_size[0]
            pos_y = int(asd_fixation_list[2]) // seg_size[1]
            key = new_grid[pos_y][pos_x]
            # Ensuring total people doesn't increase if the same person views same segment
            for i in range(len(asd_checker_list)):
                for j in range(1):
                    if asd_checker_list[i][j] == key:
                        index = i

            checker = int(asd_checker_list[index][1])
            if checker == person_count:
                pass
            else:
                dict[key]['asd'][0] += 1
                asd_checker_list[index][1] = person_count

            dict[key]['asd'][1] += int(asd_fixation_list[3])
            dict[key]['asd'][2] += 1
            # Clear list before reading next line
            asd_fixation_list.clear()

        # Close asd.txt
        asd_file.close()

    person_count = 0

    # Open Control.txt
    with open(file2) as control_file:
        # Read lines
        lines = csv.reader(control_file)
        # Ignores first line since it contains the headers
        next(lines)
        for line in lines:
            # Copy line into separate list in order to perform operations on it
            control_fixation_list = line.copy()
            if int(control_fixation_list[0]) == 0:
                person_count += 1
            # Find the position of fixation
            pos_x = int(control_fixation_list[1]) // seg_size[0]
            pos_y = int(control_fixation_list[2]) // seg_size[1]
            # Using the position we find the segment name which will be the key
            key = new_grid[pos_y][pos_x]

            # Ensuring total people doesn't increase if the same person views same segment
            for i in range(len(control_checker_list)):
                for j in range(1):
                    if control_checker_list[i][j] == key:
                        index = i
            checker = int(control_checker_list[index][1])
            if checker == person_count:
                pass
            else:
                dict[key]['control'][0] += 1
                control_checker_list[index][1] = person_count

            dict[key]['control'][1] += int(control_fixation_list[3])
            dict[key]['control'][2] += 1
            # Clear list before reading next line
            control_fixation_list.clear()
        # Close asd.txt

        control_file.close()


def check(file1, file2, grid_size, seg_order):
    # To ensure correct grid size according to file is inputted for asd file
    max_x = 0
    max_y = 0
    with open(file1) as asd_file:
        # Read lines
        lines = csv.reader(asd_file)
        # Ignores first line since it contains the headers
        next(lines)
        for line in lines:
            maxlist = line.copy()
            if int(maxlist[1]) > max_x:
                max_x = int(maxlist[1])
            if int(maxlist[2]) > max_y:
                max_y = int(maxlist[2])
            maxlist.clear()
        asd_file.close()

    while grid_size[0] < max_x or grid_size[1] < max_y:
        print(f"ASD File contains point ({max_x},{max_y}). Please enter grid size larger or equal to these values")
        grid_size[0] = int(input("Please enter the x coordinate of the image:"))
        grid_size[1] = int(input("Please enter the y  coordinate of the image:"))

    # To ensure correct grid size according to file is inputted for control file
    max_x = 0
    max_y = 0
    with open(file2) as control_file:
        # Read lines
        lines = csv.reader(control_file)
        # Ignores first line since it contains the headers
        next(lines)
        for line in lines:
            maxlist = line.copy()
            if int(maxlist[1]) > max_x:
                max_x = int(maxlist[1])
            if int(maxlist[2]) > max_y:
                max_y = int(maxlist[2])
            maxlist.clear()
        control_file.close()

    while grid_size[0] < max_x or grid_size[1] < max_y:
        print(f"Control File contains point ({max_x},{max_y}). Please enter grid size larger or equal to these values")
        grid_size[0] = int(input("Please enter the x coordinate of the image:"))
        grid_size[1] = int(input("Please enter the y  coordinate of the image:"))

    # Checking Segmentation Order, should be >= 2,2 & <= 4,4
    while seg_order.item(0) < 2 or seg_order.item(0) > 4 or seg_order.item(1) < 2 or seg_order.item(1) > 4:
        print("Segmentation Size Incorrect. Try again")
        x = int(input("Please enter the x coordinate: "))
        y = int(input("Please enter the y coordinate: "))
        seg_order = np.array([x, y])
        if 2 <= seg_order.item(0) <= 4 and 2 <= seg_order.item(1) <= 4:
            continue

    else:
        # Checking if Grid_Size & Segmentation Order would work together
        while grid_size.item(0) % seg_order.item(1) != 0 and grid_size.item(1) % seg_order.item(0) != 0:
            print("Grid can not be segmented. Try again")

            Ix = int(input("Please enter the x coordinate of the image: "))
            Iy = int(input("Please enter the y coordinate or the image: "))
            grid_size = np.array([Ix, Iy])
            if grid_size.item(0) % seg_order.item(1) == 0 and grid_size.item(1) % seg_order.item(0) == 0:
                continue

        else:
            # Calculate the x,y coordinates of each segment
            nIx = grid_size.item(0) // seg_order.item(1)
            nIy = grid_size.item(1) // seg_order.item(0)

            # Size of each new Segment
            # Will be used to find which fixation is in which segment
            seg_size = np.array([nIx, nIy])

            # Array representation of Image with Segments
            new_grid = np.zeros([seg_order.item(0), seg_order.item(1)], str)
            # Using decimal value of char
            val = 64
            for i in range(seg_order.item(0)):
                for j in range(seg_order.item(1)):
                    val = val + 1
                    new_grid[i][j] = chr(val)

            # ASD Checker List to check the number of people doesn't increase if the same person is viewing a segment
            # again Using decimal value of char
            value = 64
            asd_checker_list = np.zeros([(seg_order.item(0) * seg_order.item(1)), 2], str)
            for i in range((seg_order.item(0) * seg_order.item(1))):
                value = value + 1
                asd_checker_list[i][0] = chr(value)
                asd_checker_list[i][1] = 0

            # Create a copy of the checker list for the control list
            control_checker_list = asd_checker_list

    populateDict(file1, file2, new_grid, asd_checker_list, control_checker_list, seg_size)


# Take command line arguments
file1 = argv[1]
file2 = argv[2]
image_size = argv[3]
section_size = argv[4]

# Split the image size in order to do processing
image_size_split = image_size.split('x')
Ix = int(image_size_split[0])
Iy = int(image_size_split[1])

# Split segment size in order to do processing
section_size_split = section_size.split('x')
x = int(section_size_split[0])
y = int(section_size_split[1])

seg_order = np.array([x, y])
grid_size = np.array([Ix, Iy])

check(file1, file2, grid_size, seg_order)

# -----------MENU-----------------
option = 0
while option != 3:
    print("1. Compare the total number of people, the total time viewed, and the total number of fixations "
          "for people with and without autism for a particular element on an image")
    print("2. Compare the total number of people, the total time viewed, and the total number of fixations "
          "for people with and without autism on an image")
    print("3.Exit")

    option = int(input("Please select option 1,2 or 3: "))

    # Create plot to compare People with or without autism for specific key segment in the image
    if option == 1:
        autism_fixations_segment = 0
        no_autism_fixations_segment = 0
        # Get segment name
        user_defined_key = input("Enter the particular segment name: ").upper()
        autism_fixations_segment += dict[user_defined_key]['asd'][1]
        no_autism_fixations_segment += dict[user_defined_key]['control'][1]
        groups = ["People with Autism", "People Without Autism"]

        values = [autism_fixations_segment, no_autism_fixations_segment]
        plt.bar(groups, values)
        plt.xlabel('Groups')
        plt.ylabel('Total Time Viewed')
        plt.title(f'Comparison Between People With & Without Autism for Element {user_defined_key}')
        plt.show()
    # Create plot to compare People with or without autism for entire image
    elif option == 2:
        autism_fixations = 0
        no_autism_fixations = 0
        for i in dict.keys():
            autism_fixations += dict[i]['asd'][1]
            no_autism_fixations += dict[i]['control'][1]

        groups = ["People with Autism", "People Without Autism"]

        values = [autism_fixations, no_autism_fixations]
        plt.bar(groups, values)
        plt.xlabel('Groups')
        plt.ylabel('Total Time Viewed')
        plt.title(f'Comparison Between People With & Without Autism for Image')
        plt.show()
    elif option == 3:
        print("Thank you! Bye")
    else:
        print("Invalid option! Please try again")
