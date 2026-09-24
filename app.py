import math

import matplotlib.pyplot as plt
import streamlit as st


SIDE_KEYS = ("a", "b", "c")
ANGLE_KEYS = ("A", "B", "C")


def close_side(first, second, tolerance=1e-5):
    return abs(first - second) <= tolerance * max(abs(first), abs(second))


def triangle_from_sides(a, b, c):
    if not all(math.isfinite(x) and x > 0 for x in (a, b, c)):
        return None
    scale = max(a, b, c)
    x, y, z = a / scale, b / scale, c / scale
    if not (x + y > z and x + z > y and y + z > x):
        return None

    angle_a = math.degrees(math.acos(max(-1, min(
        1, (y * y + z * z - x * x) / (2 * y * z)
    ))))
    angle_b = math.degrees(math.acos(max(-1, min(
        1, (x * x + z * z - y * y) / (2 * x * z)
    ))))
    angle_c = 180 - angle_a - angle_b
    if not all(math.isfinite(x) and x > 0 for x in
               (angle_a, angle_b, angle_c)):
        return None
    return dict(a=a, b=b, c=c, A=angle_a, B=angle_b, C=angle_c)


def matches_given(triangle, values):
    return (
        all(values[key] is None or close_side(triangle[key], values[key])
            for key in SIDE_KEYS)
        and all(values[key] is None or
                abs(triangle[key] - values[key]) <= 0.001
                for key in ANGLE_KEYS)
    )


def solve_triangle_values(raw):
    """Return a list with one or two solutions, or raise ValueError."""
    values = {}
    for key in SIDE_KEYS + ANGLE_KEYS:
        value = raw.get(key)
        if value is None:
            values[key] = None
        elif not isinstance(value, (int, float)) or not math.isfinite(value) \
                or value <= 0 or (key in ANGLE_KEYS and value >= 180):
            if key in ANGLE_KEYS:
                raise ValueError(
                    "Each known angle must be greater than 0° and less than 180°."
                )
            raise ValueError("Each known side must be greater than zero.")
        else:
            values[key] = float(value)

    sides = [key for key in SIDE_KEYS if values[key] is not None]
    angles = [key for key in ANGLE_KEYS if values[key] is not None]
    if len(sides) + len(angles) < 3:
        raise ValueError("Enter at least three known values.")
    angle_sum = sum(values[key] for key in angles)
    if len(angles) == 3 and abs(angle_sum - 180) > 0.001:
        raise ValueError("The three angles must add up to 180°.")
    if len(angles) == 2 and angle_sum >= 180:
        raise ValueError("Two known angles must add up to less than 180°.")
    if not sides:
        raise ValueError(
            "Enter at least one side to determine the triangle's size."
        )

    candidates = []
    if len(sides) == 3:
        candidate = triangle_from_sides(*(values[key] for key in SIDE_KEYS))
        if candidate is None:
            raise ValueError("These side lengths cannot form a triangle.")
        candidates.append(candidate)

    elif len(angles) >= 2:
        found = {key: values[key] for key in ANGLE_KEYS}
        missing = next((key for key in ANGLE_KEYS if found[key] is None), None)
        if missing is not None:
            found[missing] = 180 - angle_sum
        if any(not 0 < found[key] < 180 for key in ANGLE_KEYS):
            raise ValueError("The provided angles cannot form a triangle.")
        first = sides[0]
        ratio = values[first] / math.sin(math.radians(
            found[ANGLE_KEYS[SIDE_KEYS.index(first)]]
        ))
        calculated = [
            ratio * math.sin(math.radians(found[ANGLE_KEYS[i]]))
            for i in range(3)
        ]
        candidates.append(triangle_from_sides(*calculated))

    elif len(sides) == 2 and len(angles) == 1:
        missing = next(key for key in SIDE_KEYS if values[key] is None)
        missing_index = SIDE_KEYS.index(missing)
        known_angle = angles[0]

        if known_angle == ANGLE_KEYS[missing_index]:
            # SAS: the half-angle form avoids subtracting two large squares.
            first, second = (values[key] for key in sides)
            scale = max(first, second)
            x, y = first / scale, second / scale
            third = math.hypot(
                x - y,
                2 * math.sqrt(x * y) *
                math.sin(math.radians(values[known_angle]) / 2)
            ) * scale
            completed = {key: values[key] for key in SIDE_KEYS}
            completed[missing] = third
            candidates.append(triangle_from_sides(
                *(completed[key] for key in SIDE_KEYS)
            ))
        else:
            # SSA can have zero, one, or two answers.
            pair_index = ANGLE_KEYS.index(known_angle)
            other_index = SIDE_KEYS.index(next(
                key for key in sides if key != SIDE_KEYS[pair_index]
            ))
            sine = (
                values[SIDE_KEYS[other_index]] *
                math.sin(math.radians(values[known_angle])) /
                values[SIDE_KEYS[pair_index]]
            )
            if sine <= 1 + 1e-12:
                acute = math.degrees(math.asin(max(-1, min(1, sine))))
                choices = (90,) if sine >= 1 - 1e-12 else (
                    acute, 180 - acute
                )
                for other_angle in choices:
                    remaining_angle = 180 - values[known_angle] - other_angle
                    if remaining_angle <= 0:
                        continue
                    third = (
                        values[SIDE_KEYS[pair_index]] *
                        math.sin(math.radians(remaining_angle)) /
                        math.sin(math.radians(values[known_angle]))
                    )
                    completed = {key: values[key] for key in SIDE_KEYS}
                    completed[missing] = third
                    candidates.append(triangle_from_sides(
                        *(completed[key] for key in SIDE_KEYS)
                    ))

    solutions = []
    for candidate in candidates:
        if candidate is None or not matches_given(candidate, values):
            continue
        if not any(all(close_side(
            old[key], candidate[key], 1e-9
        ) for key in SIDE_KEYS) for old in solutions):
            solutions.append(candidate)
    if not solutions:
        raise ValueError("The provided values cannot describe one triangle.")
    return solutions


def identify_triangle_type(triangle):
    a, b, c = (triangle[key] for key in SIDE_KEYS)
    angles = (triangle[key] for key in ANGLE_KEYS)
    same = lambda x, y: close_side(x, y, 1e-8)
    if same(a, b) and same(b, c):
        side_type = "Equilateral"
    elif same(a, b) or same(b, c) or same(a, c):
        side_type = "Isosceles"
    else:
        side_type = "Scalene"
    if any(abs(angle - 90) <= 1e-7 for angle in angles):
        angle_type = "Right-angled"
    elif any(angle > 90 for angle in angles):
        angle_type = "Obtuse"
    else:
        angle_type = "Acute"
    return f"{angle_type} and {side_type}"


def draw_triangle(triangle):
    a, b, c = (triangle[key] for key in SIDE_KEYS)
    angle_a = math.radians(triangle["A"])
    points = ((0, 0), (c, 0), (b * math.cos(angle_a),
                               b * math.sin(angle_a)))
    (x1, y1), (x2, y2), (x3, y3) = points
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot([x1, x2, x3, x1], [y1, y2, y3, y1], "k-")
    ax.text(x1, y1, "A")
    ax.text(x2, y2, "B")
    ax.text(x3, y3, "C")
    ax.text((x1+x3)/2, (y1+y3)/2, f"b = {b:.10g}")
    ax.text((x2+x3)/2, (y2+y3)/2, f"a = {a:.10g}")
    ax.text((x1+x2)/2, y1, f"c = {c:.10g}")
    ax.set_aspect("equal", adjustable="datalim")
    ax.margins(0.15)
    ax.set_title("Resulting Triangle")
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)


def optional_number(text):
    if not text.strip():
        return None
    try:
        return float(text)
    except ValueError as error:
        raise ValueError("Enter numbers using a decimal point.") from error


st.set_page_config(page_title="Triangle Solver", page_icon="📐",
                   layout="centered")
st.title("📐 Triangle Solver")
st.write("Solve a triangle using the Law of Sines and Law of Cosines.")
st.info(
    "Enter at least three consistent values, including one side. "
    "Leave unknown values blank. Angles are in degrees. "
    "An SSA combination may have two valid triangles."
)
st.header("Enter the known values")
col1, col2 = st.columns(2)
with col1:
    raw_a = st.text_input("Side a")
    raw_b = st.text_input("Side b")
    raw_c = st.text_input("Side c")
with col2:
    raw_A = st.text_input("Angle A (opposite side a)")
    raw_B = st.text_input("Angle B (opposite side b)")
    raw_C = st.text_input("Angle C (opposite side c)")

if st.button("🔢 Solve Triangle", type="primary"):
    try:
        raw = (raw_a, raw_b, raw_c, raw_A, raw_B, raw_C)
        given = {
            key: optional_number(value)
            for key, value in zip(SIDE_KEYS + ANGLE_KEYS, raw)
        }
        solutions = solve_triangle_values(given)
    except ValueError as error:
        st.error(str(error))
    else:
        st.success(
            "Two valid triangles match these values." if len(solutions) == 2
            else "Triangle solved successfully!"
        )
        st.header("Triangle Solutions" if len(solutions) == 2
                  else "Triangle Solution")
        for index, triangle in enumerate(solutions, start=1):
            if len(solutions) == 2:
                st.subheader(f"Solution {index}")
            sides_col, angles_col = st.columns(2)
            with sides_col:
                st.subheader("Sides")
                for key in SIDE_KEYS:
                    st.write(f"**Side {key}:** {triangle[key]:.10g}")
            with angles_col:
                st.subheader("Angles")
                for key in ANGLE_KEYS:
                    st.write(f"**Angle {key}:** {triangle[key]:.4f}°")
            st.subheader("Triangle Classification")
            st.write(f"**Type:** {identify_triangle_type(triangle)}")
            st.subheader("Triangle Diagram")
            draw_triangle(triangle)
