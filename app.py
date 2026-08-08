
import streamlit as st
import math
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Triangle Solver",
    page_icon="📐",
    layout="centered"
)

st.title("📐 Triangle Solver")
st.write("Solve a triangle using the Law of Sines and Law of Cosines.")

st.info(
    "Enter at least three consistent values. "
    "You may enter sides, angles, or a combination of both. "
    "Angles must be in degrees."
)


# ---------------------------------------------------------
# Triangle classification
# ---------------------------------------------------------

def identify_triangle_type(sides, angles):
    a = sides["a"]
    b = sides["b"]
    c = sides["c"]

    A = angles["A"]
    B = angles["B"]
    C = angles["C"]

    # Classification by sides
    if (
        math.isclose(a, b, rel_tol=1e-5)
        and math.isclose(b, c, rel_tol=1e-5)
    ):
        side_type = "Equilateral"
    elif (
        math.isclose(a, b, rel_tol=1e-5)
        or math.isclose(b, c, rel_tol=1e-5)
        or math.isclose(a, c, rel_tol=1e-5)
    ):
        side_type = "Isosceles"
    else:
        side_type = "Scalene"

    # Classification by angles
    if (
        math.isclose(A, 90, abs_tol=1e-5)
        or math.isclose(B, 90, abs_tol=1e-5)
        or math.isclose(C, 90, abs_tol=1e-5)
    ):
        angle_type = "Right-angled"
    elif A > 90 or B > 90 or C > 90:
        angle_type = "Obtuse"
    else:
        angle_type = "Acute"

    return f"{angle_type} and {side_type}"


# ---------------------------------------------------------
# Draw triangle
# ---------------------------------------------------------

def draw_triangle(sides, angles):
    a = sides["a"]
    b = sides["b"]
    c = sides["c"]

    A = math.radians(angles["A"])

    # Coordinates
    P1 = (0, 0)
    P2 = (c, 0)

    P3_x = b * math.cos(A)
    P3_y = b * math.sin(A)

    P3 = (P3_x, P3_y)

    fig, ax = plt.subplots(figsize=(7, 7))

    # Triangle
    ax.plot(
        [P1[0], P2[0], P3[0], P1[0]],
        [P1[1], P2[1], P3[1], P1[1]],
        "k-"
    )

    # Vertex labels
    ax.text(P1[0] - 0.2, P1[1] - 0.2, "A", fontsize=13)
    ax.text(P2[0] + 0.1, P2[1] - 0.2, "B", fontsize=13)
    ax.text(P3[0] + 0.1, P3[1] + 0.1, "C", fontsize=13)

    # Side labels
    ax.text(
        (P1[0] + P3[0]) / 2,
        (P1[1] + P3[1]) / 2,
        f"b = {b:.2f}"
    )

    ax.text(
        (P2[0] + P3[0]) / 2,
        (P2[1] + P3[1]) / 2,
        f"a = {a:.2f}"
    )

    ax.text(
        (P1[0] + P2[0]) / 2,
        -0.2,
        f"c = {c:.2f}"
    )

    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Resulting Triangle")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.grid(True)

    padding_x = max((max(P1[0], P2[0], P3[0])
                     - min(P1[0], P2[0], P3[0])) * 0.15, 1)

    padding_y = max((max(P1[1], P2[1], P3[1])
                     - min(P1[1], P2[1], P3[1])) * 0.15, 1)

    ax.set_xlim(
        min(P1[0], P2[0], P3[0]) - padding_x,
        max(P1[0], P2[0], P3[0]) + padding_x
    )

    ax.set_ylim(
        min(P1[1], P2[1], P3[1]) - padding_y,
        max(P1[1], P2[1], P3[1]) + padding_y
    )

    st.pyplot(fig)


# ---------------------------------------------------------
# Input section
# ---------------------------------------------------------

st.header("Enter the known values")

col1, col2 = st.columns(2)

with col1:
    a = st.number_input(
        "Side a",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

    b = st.number_input(
        "Side b",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

    c = st.number_input(
        "Side c",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

with col2:
    A = st.number_input(
        "Angle A (opposite side a)",
        min_value=0.0,
        max_value=179.999,
        value=0.0,
        step=0.1
    )

    B = st.number_input(
        "Angle B (opposite side b)",
        min_value=0.0,
        max_value=179.999,
        value=0.0,
        step=0.1
    )

    C = st.number_input(
        "Angle C (opposite side c)",
        min_value=0.0,
        max_value=179.999,
        value=0.0,
        step=0.1
    )


if st.button("🔢 Solve Triangle", type="primary"):

    sides = {
        "a": a,
        "b": b,
        "c": c
    }

    angles = {
        "A": A,
        "B": B,
        "C": C
    }

    known_count = sum(value > 0 for value in sides.values()) + \
                  sum(value > 0 for value in angles.values())

    # -----------------------------------------------------
    # Validate number of inputs
    # -----------------------------------------------------

    if known_count < 3:
        st.error(
            "You need at least three known values to solve the triangle."
        )
        st.stop()

    # -----------------------------------------------------
    # Validate known angles
    # -----------------------------------------------------

    known_angles = [x for x in angles.values() if x > 0]

    if len(known_angles) >= 2:

        if len(known_angles) == 3:
            if not math.isclose(sum(known_angles), 180, abs_tol=1e-5):
                st.error("The three angles must add up to 180°.")
                st.stop()

        elif sum(known_angles) >= 180:
            st.error(
                "The known angles must have a sum less than 180°."
            )
            st.stop()

    # -----------------------------------------------------
    # SSS - Law of Cosines
    # -----------------------------------------------------

    if a > 0 and b > 0 and c > 0:

        if not (
            a + b > c
            and a + c > b
            and b + c > a
        ):
            st.error(
                "These side lengths cannot form a triangle. "
                "They do not satisfy the triangle inequality."
            )
            st.stop()

        if A == 0:
            cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
            cos_A = max(-1, min(1, cos_A))
            A = math.degrees(math.acos(cos_A))
            angles["A"] = A

        if B == 0:
            cos_B = (a**2 + c**2 - b**2) / (2 * a * c)
            cos_B = max(-1, min(1, cos_B))
            B = math.degrees(math.acos(cos_B))
            angles["B"] = B

        if C == 0:
            cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
            cos_C = max(-1, min(1, cos_C))
            C = math.degrees(math.acos(cos_C))
            angles["C"] = C

    else:

        # -------------------------------------------------
        # Two angles known
        # -------------------------------------------------

        if A > 0 and B > 0 and C == 0:
            C = 180 - A - B
            angles["C"] = C

        elif A > 0 and C > 0 and B == 0:
            B = 180 - A - C
            angles["B"] = B

        elif B > 0 and C > 0 and A == 0:
            A = 180 - B - C
            angles["A"] = A

        # -------------------------------------------------
        # SAS - Law of Cosines
        # -------------------------------------------------

        if a > 0 and b > 0 and C > 0 and c == 0:

            c = math.sqrt(
                a**2 + b**2
                - 2 * a * b * math.cos(math.radians(C))
            )

            sides["c"] = c

        elif a > 0 and c > 0 and B > 0 and b == 0:

            b = math.sqrt(
                a**2 + c**2
                - 2 * a * c * math.cos(math.radians(B))
            )

            sides["b"] = b

        elif b > 0 and c > 0 and A > 0 and a == 0:

            a = math.sqrt(
                b**2 + c**2
                - 2 * b * c * math.cos(math.radians(A))
            )

            sides["a"] = a

        # -------------------------------------------------
        # Law of Sines
        # -------------------------------------------------

        pairs = [
            (a, A, "a"),
            (b, B, "b"),
            (c, C, "c")
        ]

        ratio = None

        for side, angle, key in pairs:
            if side > 0 and angle > 0:
                ratio = side / math.sin(math.radians(angle))
                break

        if ratio is not None:

            # Find missing sides
            if A > 0 and a == 0:
                a = ratio * math.sin(math.radians(A))
                sides["a"] = a

            if B > 0 and b == 0:
                b = ratio * math.sin(math.radians(B))
                sides["b"] = b

            if C > 0 and c == 0:
                c = ratio * math.sin(math.radians(C))
                sides["c"] = c

            # Find missing angles
            if a > 0 and A == 0:
                value = a / ratio

                if -1 <= value <= 1:
                    A = math.degrees(math.asin(value))
                    angles["A"] = A

            if b > 0 and B == 0:
                value = b / ratio

                if -1 <= value <= 1:
                    B = math.degrees(math.asin(value))
                    angles["B"] = B

            if c > 0 and C == 0:
                value = c / ratio

                if -1 <= value <= 1:
                    C = math.degrees(math.asin(value))
                    angles["C"] = C

            # Recalculate final angle if two are known
            if A > 0 and B > 0 and C == 0:
                C = 180 - A - B
                angles["C"] = C

            elif A > 0 and C > 0 and B == 0:
                B = 180 - A - C
                angles["B"] = B

            elif B > 0 and C > 0 and A == 0:
                A = 180 - B - C
                angles["A"] = A

    # -----------------------------------------------------
    # Final validation
    # -----------------------------------------------------

    if not all(value > 0 for value in sides.values()):
        st.error(
            "The triangle could not be completely solved "
            "with the provided information."
        )
        st.stop()

    if not all(value > 0 for value in angles.values()):
        st.error(
            "The triangle could not be completely solved "
            "with the provided information."
        )
        st.stop()

    total_angles = sum(angles.values())

    if not math.isclose(total_angles, 180, abs_tol=1e-4):
        st.error(
            f"The angles add up to {total_angles:.4f}°, "
            "not 180°. The provided information may be inconsistent."
        )
        st.stop()

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    st.success("Triangle solved successfully!")

    st.header("Triangle Solution")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.subheader("Sides")
        st.write(f"**Side a:** {a:.4f}")
        st.write(f"**Side b:** {b:.4f}")
        st.write(f"**Side c:** {c:.4f}")

    with result_col2:
        st.subheader("Angles")
        st.write(f"**Angle A:** {A:.4f}°")
        st.write(f"**Angle B:** {B:.4f}°")
        st.write(f"**Angle C:** {C:.4f}°")

    st.subheader("Triangle Classification")

    triangle_type = identify_triangle_type(
        sides,
        angles
    )

    st.write(f"**Type:** {triangle_type}")

    st.subheader("Triangle Diagram")

    draw_triangle(
        sides,
        angles
    )
```
