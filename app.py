# -*- coding: utf-8 -*-
"final project info II"

streamlit

import math
import matplotlib.pyplot as plt

def identify_triangle_type(sides, angles_deg):
    side_a = sides['a']
    side_b = sides['b']
    side_c = sides['c']
    angle_A = angles_deg['A']
    angle_B = angles_deg['B']
    angle_C = angles_deg['C']

    # Classify by sides
    side_type = "Scalene"
    if math.isclose(side_a, side_b) and math.isclose(side_b, side_c):
        side_type = "Equilateral"
    elif math.isclose(side_a, side_b, rel_tol=1e-5) or \
         math.isclose(side_b, side_c, rel_tol=1e-5) or \
         math.isclose(side_a, side_c, rel_tol=1e-5):
        side_type = "Isosceles"

    # Classify by angles
    angle_type = "Acute"
    if math.isclose(angle_A, 90, rel_tol=1e-5) or \
       math.isclose(angle_B, 90, rel_tol=1e-5) or \
       math.isclose(angle_C, 90, rel_tol=1e-5):
        angle_type = "Right-angled"
    elif angle_A > 90 or angle_B > 90 or angle_C > 90:
        angle_type = "Obtuse"

    return f"Type of triangle: {angle_type} and {side_type}."

def draw_triangle(sides, angles_deg):
    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')

    # Use side c as the base on the x-axis
    c = sides['c']
    a = sides['a']
    b = sides['b']
    angle_A_rad = math.radians(angles_deg['A'])

    # Coordinates of vertices
    P1 = (0, 0) # Vertex A
    P2 = (c, 0) # Vertex B
    # Calculate Vertex C using side 'b' and angle 'A'
    P3_x = b * math.cos(angle_A_rad)
    P3_y = b * math.sin(angle_A_rad)
    P3 = (P3_x, P3_y) # Vertex C

    # Plot the triangle
    plt.plot([P1[0], P2[0], P3[0], P1[0]], [P1[1], P2[1], P3[1], P1[1]], 'k-') # 'k-' for black line

    # Add vertex labels
    plt.text(P1[0] - 0.2, P1[1] - 0.2, 'A', fontsize=12)
    plt.text(P2[0] + 0.1, P2[1] - 0.2, 'B', fontsize=12)
    plt.text(P3[0] + 0.1, P3[1] + 0.1, 'C', fontsize=12)

    # Add side labels (midpoints)
    plt.text((P1[0] + P3[0]) / 2 - 0.1, (P1[1] + P3[1]) / 2 + 0.1, f"b={b:.2f}", fontsize=10)
    plt.text((P2[0] + P3[0]) / 2 + 0.1, (P2[1] + P3[1]) / 2 + 0.1, f"a={a:.2f}", fontsize=10)
    plt.text((P1[0] + P2[0]) / 2, (P1[1] + P2[1]) / 2 - 0.2, f"c={c:.2f}", fontsize=10)


    # Set title and adjust limits
    plt.title('Resulting Triangle')
    min_x = min(P1[0], P2[0], P3[0])
    max_x = max(P1[0], P2[0], P3[0])
    min_y = min(P1[1], P2[1], P3[1])
    max_y = max(P1[1], P2[1], P3[1])

    # Add some padding to the limits
    padding_x = (max_x - min_x) * 0.1
    padding_y = (max_y - min_y) * 0.1
    plt.xlim(min_x - padding_x - 1, max_x + padding_x + 1)
    plt.ylim(min_y - padding_y - 1, max_y + padding_y + 1)

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.show()

def solve_triangle_law_of_sines():
    print("\n--- Triangle Solver using Law of Sines and Cosines ---")
    print("This program solves a triangle given three known values (sides or angles).")
    print("Enter the known values for sides (a, b, c) and angles (A, B, C).")
    print("Angles must be entered in degrees. 'A' is opposite 'a', 'B' opposite 'b', 'C' opposite 'c'.")
    print("If a value is unknown, leave it blank or enter '0'.")
    print("At least three consistent known values are required to solve a unique triangle.")

    # Initialize side and angle values
    sides = {'a': 0.0, 'b': 0.0, 'c': 0.0}
    angles_deg = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    known_count = 0

    # Messages to ask inputs to user
    inputs_prompts = {
        'a': "side a", 'b': "side b", 'c': "side c",
        'A': "angle A (opposite to side a)",
        'B': "angle B (opposite to side b)",
        'C': "angle C (opposite to side c)"
    }


    # Get inputs from the user with validation
    for key, prompt_text in inputs_prompts.items():
        while True:
            try:
                user_input = input(f"Enter the value for {prompt_text}: ").strip()
                if not user_input or user_input == '0':
                    value = 0.0
                else:
                    value = float(user_input)
                    if value <= 0:
                        print("Error: Sides and angles must be positive. Enter '0' if unknown.")
                        continue
                    if key[0].isupper() and value >= 180:  # Angles must be < 180
                        print("Error: Angles must be less than 180 degrees. Enter '0' if unknown.")
                        continue

                if value > 0: # Only count postive values as known
                    known_count += 1

                if key[0].islower():  # It's a side
                    sides[key] = value
                else:  # It's an angle
                    angles_deg[key] = value

                break
            except ValueError:
                print("Invalid input. Please, enter a number or leave blank/enter '0'.")

    # Basic validation of the number of known values
    if known_count < 3:
        print("\nError: You need at least three known values (e.g., two angles and a side, or two sides and an opposite angle) to solve the triangle.")
        return

    # Warning for more than 3 inputs - consistency check not fully implemented
    if known_count > 3:
        print("\nWarning: More than three values were provided. The program will attempt to solve, but inconsistencies might lead to errors or unexpected results.")

    # Initial verification of the sum of known angles for consistency
    num_known_angles = sum(1 for angle in angles_deg.values() if angle > 0)
    if num_known_angles == 2:
        known_angle_sum = sum(angle for angle in angles_deg.values() if angle > 0)
        if known_angle_sum >= 180: # If two angles sum 180 or more, it's not a valid triangle
            print(f"\nError: The sum of two known angles ({known_angle_sum}°) is 180 degrees or more. This cannot form a valid triangle.")
            return
    elif num_known_angles == 3:
        total_angle_sum = sum(angles_deg.values())
        if not math.isclose(total_angle_sum, 180, abs_tol=1e-6):
            print(f"\nError: The sum of three known angles ({total_angle_sum}°) is not 180 degrees. Inconsistent data.")
            return
        # Specific error for AAA case (three angles, no sides)
        if all(s == 0 for s in sides.values()):
            print("\nError: Three angles are not enough to determine a unique triangle. At least one side is required.")
            return

    # Convert known angles to radians for mathematical calculations
    angles_rad = {k: math.radians(v) if v > 0 else 0.0 for k, v in angles_deg.items()}

    # Loop to try to solve the triangle iteratively
    progress_made = True
    while progress_made:
        progress_made = False

        # Step 1: Find the third angle if two are known
        if angles_deg['A'] and angles_deg['B'] and not angles_deg['C']:
            angles_deg['C'] = 180 - angles_deg['A'] - angles_deg['B']
            angles_rad['C'] = math.radians(angles_deg['C'])
            progress_made = True
        elif angles_deg['A'] and angles_deg['C'] and not angles_deg['B']:
            angles_deg['B'] = 180 - angles_deg['A'] - angles_deg['C']
            angles_rad['B'] = math.radians(angles_deg['B'])
            progress_made = True
        elif angles_deg['B'] and angles_deg['C'] and not angles_deg['A']:
            angles_deg['A'] = 180 - angles_deg['B'] - angles_deg['C']
            angles_rad['A'] = math.radians(angles_deg['A'])
            progress_made = True

        # Check if any newly calculated angle is invalid (e.g., >= 180 or <= 0)
        for ang_deg in angles_deg.values():
            if ang_deg > 0 and (ang_deg >= 180 or ang_deg <= 0):
                print(f"\nError: Calculated angle {ang_deg:.2f} degrees, which is not possible in a triangle. Inconsistent data.")
                return

        # --- Law of Cosines (SSS and SAS cases) ---

        # SSS Case: All sides known, find angles
        if sides['a'] > 0 and sides['b'] > 0 and sides['c'] > 0:
            # Triangle Inequality Check
            if not (sides['a'] + sides['b'] > sides['c'] and
                    sides['a'] + sides['c'] > sides['b'] and
                    sides['b'] + sides['c'] > sides['a']):
                print("\nError: The given side lengths do not satisfy the triangle inequality (e.g., a+b > c). A triangle cannot be formed with these sides.")
                return

            if not angles_deg['A']:
                try:
                    cos_A = (sides['b']**2 + sides['c']**2 - sides['a']**2) / (2 * sides['b'] * sides['c'])
                    cos_A = max(-1.0, min(1.0, cos_A)) # Clamp to avoid domain errors from floating point inaccuracies
                    angles_rad['A'] = math.acos(cos_A)
                    angles_deg['A'] = math.degrees(angles_rad['A'])
                    progress_made = True
                except ZeroDivisionError:
                    pass # Will be caught by other validations if sides are 0
            if not angles_deg['B']:
                try:
                    cos_B = (sides['a']**2 + sides['c']**2 - sides['b']**2) / (2 * sides['a'] * sides['c'])
                    cos_B = max(-1.0, min(1.0, cos_B))
                    angles_rad['B'] = math.acos(cos_B)
                    angles_deg['B'] = math.degrees(angles_rad['B'])
                    progress_made = True
                except ZeroDivisionError:
                    pass
            if not angles_deg['C']:
                try:
                    cos_C = (sides['a']**2 + sides['b']**2 - sides['c']**2) / (2 * sides['a'] * sides['b'])
                    cos_C = max(-1.0, min(1.0, cos_C))
                    angles_rad['C'] = math.acos(cos_C)
                    angles_deg['C'] = math.degrees(angles_rad['C'])
                    progress_made = True
                except ZeroDivisionError:
                    pass

        # SAS Case: Two sides and included angle known, find third side
        if sides['a'] > 0 and sides['b'] > 0 and angles_deg['C'] > 0 and not sides['c']:
            try:
                sides['c'] = math.sqrt(sides['a']**2 + sides['b']**2 - 2 * sides['a'] * sides['b'] * math.cos(angles_rad['C']))
                progress_made = True
            except ValueError: # math.sqrt of negative number if calculation error
                pass
        elif sides['a'] > 0 and sides['c'] > 0 and angles_deg['B'] > 0 and not sides['b']:
            try:
                sides['b'] = math.sqrt(sides['a']**2 + sides['c']**2 - 2 * sides['a'] * sides['c'] * math.cos(angles_rad['B']))
                progress_made = True
            except ValueError:
                pass
        elif sides['b'] > 0 and sides['c'] > 0 and angles_deg['A'] > 0 and not sides['a']:
            try:
                sides['a'] = math.sqrt(sides['b']**2 + sides['c']**2 - 2 * sides['b'] * sides['c'] * math.cos(angles_rad['A']))
                progress_made = True
            except ValueError:
                pass
        # --- End Law of Cosines ---

        # Step 2: Finding the ratio of the Law of Sines if a complete pair (opposite side-angle) is known
        current_ratio = 0.0
        if sides['a'] > 0 and angles_deg['A'] > 0: # Make sure the angle is not 0 to avoid division by zero
            current_ratio = sides['a'] / math.sin(angles_rad['A'])
        elif sides['b'] > 0 and angles_deg['B'] > 0:
            current_ratio = sides['b'] / math.sin(angles_rad['B'])
        elif sides['c'] > 0 and angles_deg['C'] > 0:
            current_ratio = sides['c'] / math.sin(angles_rad['C'])

        # If a valid ratio was found, try to find missing sides and angles.
        if current_ratio > 0:
            # Find missing sides
            if angles_deg['A'] > 0 and not sides['a']:
                sides['a'] = current_ratio * math.sin(angles_rad['A'])
                progress_made = True
            if angles_deg['B'] > 0 and not sides['b']:
                sides['b'] = current_ratio * math.sin(angles_rad['B'])
                progress_made = True
            if angles_deg['C'] > 0 and not sides['c']:
                sides['c'] = current_ratio * math.sin(angles_rad['C'])
                progress_made = True

            # Find missing angles
            for side_key, angle_key in zip(['a', 'b', 'c'], ['A', 'B', 'C']):
                if sides[side_key] > 0 and not angles_deg[angle_key]:
                    try:
                        sin_val = sides[side_key] / current_ratio
                        # Allow small floating-point deviations for comparison
                        if not (-1.000001 <= sin_val <= 1.000001):
                            print(f"\nError: The value of the sine for angle {angle_key} ({sin_val:.4f}) is out of range [-1, 1]. No triangle can be formed with this data (e.g., SSA case with no solution).")
                            return

                        # Adjust the value of sin_val to [-1, 1] to avoid domain errors in math.asin
                        sin_val = max(-1.0, min(1.0, sin_val))

                        angle_rad1 = math.asin(sin_val)
                        angle_deg1 = math.degrees(angle_rad1)

                        # Check for SSA ambiguity (two possible solutions)
                        # This condition implies that if the side opposite the *calculated* angle
                        # is smaller than the side *used to find the ratio* (which is opposite the known angle),
                        # and the calculated angle is acute, there might be two solutions.
                        # This program currently finds one solution.
                        # A more robust solution would involve finding both and presenting them.
                        # For now, we add a flag to indicate potential ambiguity.
                        # (This is a simplified check for potential ambiguity, not a full SSA solver)

                        angles_deg[angle_key] = angle_deg1
                        angles_rad[angle_key] = angle_rad1
                        progress_made = True

                    except ValueError as e:
                        print(f"\nError: Calculating angle {angle_key}: {e}. Inconsistent data.")
                        return

    # Final verification and results
    all_sides_known = all(s > 0 for s in sides.values())
    all_angles_known = all(a > 0 for a in angles_deg.values())

    if all_sides_known and all_angles_known:
        total_angle_sum = sum(angles_deg.values())
        if math.isclose(total_angle_sum, 180, abs_tol=1e-6):
            print("\n--- Triangle Solution ---")
            print(f"Side a: {sides['a']:.4f}")
            print(f"Side b: {sides['b']:.4f}")
            print(f"Side c: {sides['c']:.4f}")
            print(f"Angle A: {angles_deg['A']:.4f}°")
            print(f"Angle B: {angles_deg['B']:.4f}°")
            print(f"Angle C: {angles_deg['C']:.4f}°")

            print("\nNote on SSA (Side-Side-Angle) cases: If two sides and a non-included angle are given (SSA), there might be zero, one, or two possible triangles. This program finds one valid solution if it exists. If the known opposite side is shorter than the adjacent side and the given angle is acute, a second solution (180° - found_angle) might exist which this program does not explicitly calculate or display.")

            # New features: identify and draw the triangle
            print("\n" + identify_triangle_type(sides, angles_deg))
            draw_triangle(sides, angles_deg)

        else:
            print(f"\nError: The final sum of angles ({total_angle_sum:.4f}°) is not 180 degrees. There is a problem with the calculations or the input data.")
            print("The triangle could not be solved with the data provided or the data is inconsistent.")
    else:
        print("\nThe triangle could not be fully solved with the data provided or it is insufficient.")
        print("Make sure to provide enough consistent data (at least 3 values, including at least one side for AAA cases, and valid geometry for SSS/SSA).")
        print("\nPartial values (0.0 means unknown):")
        print(f"Side a: {sides['a']:.4f}, Angle A: {angles_deg['A']:.4f}°")
        print(f"Side b: {sides['b']:.4f}, Angle B: {angles_deg['B']:.4f}°")
        print(f"Side c: {sides['c']:.4f}, Angle C: {angles_deg['C']:.4f}°")

# Execute function
solve_triangle_law_of_sines()
