function getValue(id) {
    const value = document.getElementById(id).value;

    if (value === "") {
        return 0;
    }

    return Number(value);
}


function degreesToRadians(degrees) {
    return degrees * Math.PI / 180;
}


function radiansToDegrees(radians) {
    return radians * 180 / Math.PI;
}


function clamp(value) {
    return Math.max(-1, Math.min(1, value));
}


function solveTriangle() {

    let a = getValue("sideA");
    let b = getValue("sideB");
    let c = getValue("sideC");

    let A = getValue("angleA");
    let B = getValue("angleB");
    let C = getValue("angleC");

    const message = document.getElementById("message");
    const results = document.getElementById("results");

    message.innerHTML = "";
    results.classList.add("hidden");

    const knownCount =
        (a > 0 ? 1 : 0) +
        (b > 0 ? 1 : 0) +
        (c > 0 ? 1 : 0) +
        (A > 0 ? 1 : 0) +
        (B > 0 ? 1 : 0) +
        (C > 0 ? 1 : 0);

    if (knownCount < 3) {
        showError("You need at least three known values.");
        return;
    }


    // Validate individual angles

    if (A >= 180 || B >= 180 || C >= 180) {
        showError("Angles must be less than 180°.");
        return;
    }


    // Validate known angles

    const knownAngles = [];

    if (A > 0) knownAngles.push(A);
    if (B > 0) knownAngles.push(B);
    if (C > 0) knownAngles.push(C);

    if (knownAngles.length >= 2) {

        const angleSum = knownAngles.reduce(
            (sum, angle) => sum + angle,
            0
        );

        if (angleSum >= 180) {
            showError(
                "The known angles must have a sum less than 180°."
            );
            return;
        }
    }


    // --------------------------------------------------
    // SSS - Law of Cosines
    // --------------------------------------------------

    if (a > 0 && b > 0 && c > 0) {

        if (!(a + b > c && a + c > b && b + c > a)) {
            showError(
                "These side lengths cannot form a triangle."
            );
            return;
        }

        if (A === 0) {

            const cosA =
                (b * b + c * c - a * a) /
                (2 * b * c);

            A = radiansToDegrees(
                Math.acos(clamp(cosA))
            );
        }

        if (B === 0) {

            const cosB =
                (a * a + c * c - b * b) /
                (2 * a * c);

            B = radiansToDegrees(
                Math.acos(clamp(cosB))
            );
        }

        if (C === 0) {

            const cosC =
                (a * a + b * b - c * c) /
                (2 * a * b);

            C = radiansToDegrees(
                Math.acos(clamp(cosC))
            );
        }

    } else {

        // --------------------------------------------------
        // Two angles known
        // --------------------------------------------------

        if (A > 0 && B > 0 && C === 0) {
            C = 180 - A - B;
        }

        else if (A > 0 && C > 0 && B === 0) {
            B = 180 - A - C;
        }

        else if (B > 0 && C > 0 && A === 0) {
            A = 180 - B - C;
        }


        // --------------------------------------------------
        // SAS - Law of Cosines
        // --------------------------------------------------

        if (a > 0 && b > 0 && C > 0 && c === 0) {

            c = Math.sqrt(
                a * a +
                b * b -
                2 * a * b * Math.cos(degreesToRadians(C))
            );
        }

        else if (a > 0 && c > 0 && B > 0 && b === 0) {

            b = Math.sqrt(
                a * a +
                c * c -
                2 * a * c * Math.cos(degreesToRadians(B))
            );
        }

        else if (b > 0 && c > 0 && A > 0 && a === 0) {

            a = Math.sqrt(
                b * b +
                c * c -
                2 * b * c * Math.cos(degreesToRadians(A))
            );
        }


        // --------------------------------------------------
        // Law of Sines
        // --------------------------------------------------

        let ratio = null;

        if (a > 0 && A > 0) {
            ratio = a / Math.sin(degreesToRadians(A));
        }

        else if (b > 0 && B > 0) {
            ratio = b / Math.sin(degreesToRadians(B));
        }

        else if (c > 0 && C > 0) {
            ratio = c / Math.sin(degreesToRadians(C));
        }


        if (ratio !== null) {

            // Find missing sides

            if (A > 0 && a === 0) {
                a = ratio * Math.sin(
                    degreesToRadians(A)
                );
            }

            if (B > 0 && b === 0) {
                b = ratio * Math.sin(
                    degreesToRadians(B)
                );
            }

            if (C > 0 && c === 0) {
                c = ratio * Math.sin(
                    degreesToRadians(C)
                );
            }


            // Find missing angles

            if (a > 0 && A === 0) {

                const value = a / ratio;

                if (value < -1 || value > 1) {
                    showError(
                        "The provided information is inconsistent."
                    );
                    return;
                }

                A = radiansToDegrees(
                    Math.asin(clamp(value))
                );
            }

            if (b > 0 && B === 0) {

                const value = b / ratio;

                if (value < -1 || value > 1) {
                    showError(
                        "The provided information is inconsistent."
                    );
                    return;
                }

                B = radiansToDegrees(
                    Math.asin(clamp(value))
                );
            }

            if (c > 0 && C === 0) {

                const value = c / ratio;

                if (value < -1 || value > 1) {
                    showError(
                        "The provided information is inconsistent."
                    );
                    return;
                }

                C = radiansToDegrees(
                    Math.asin(clamp(value))
                );
            }


            // Final missing angle

            if (A > 0 && B > 0 && C === 0) {
                C = 180 - A - B;
            }

            else if (A > 0 && C > 0 && B === 0) {
                B = 180 - A - C;
            }

            else if (B > 0 && C > 0 && A === 0) {
                A = 180 - B - C;
            }
        }
    }


    // --------------------------------------------------
    // Final validation
    // --------------------------------------------------

    if (!(a > 0 && b > 0 && c > 0)) {
        showError(
            "The triangle could not be completely solved."
        );
        return;
    }

    if (!(A > 0 && B > 0 && C > 0)) {
        showError(
            "The triangle could not be completely solved."
        );
        return;
    }


    const totalAngles = A + B + C;

    if (Math.abs(totalAngles - 180) > 0.001) {
        showError(
            `The angles add up to ${totalAngles.toFixed(4)}°, not 180°.`
        );
        return;
    }


    // --------------------------------------------------
    // Display results
    // --------------------------------------------------

    document.getElementById("resultA").textContent =
        a.toFixed(4);

    document.getElementById("resultB").textContent =
        b.toFixed(4);

    document.getElementById("resultC").textContent =
        c.toFixed(4);

    document.getElementById("resultAngleA").textContent =
        A.toFixed(4) + "°";

    document.getElementById("resultAngleB").textContent =
        B.toFixed(4) + "°";

    document.getElementById("resultAngleC").textContent =
        C.toFixed(4) + "°";


    // Classification

    const triangleType =
        identifyTriangleType(a, b, c, A, B, C);

    document.getElementById("triangleType").textContent =
        triangleType;


    message.innerHTML =
        '<div class="success">Triangle solved successfully!</div>';

    results.classList.remove("hidden");


    // Draw triangle

    drawTriangle(a, b, c, A);
}


// --------------------------------------------------
// Triangle classification
// --------------------------------------------------

function identifyTriangleType(a, b, c, A, B, C) {

    const equalAB = Math.abs(a - b) < 0.00001;
    const equalBC = Math.abs(b - c) < 0.00001;
    const equalAC = Math.abs(a - c) < 0.00001;


    let sideType;

    if (equalAB && equalBC) {
        sideType = "Equilateral";
    }

    else if (equalAB || equalBC || equalAC) {
        sideType = "Isosceles";
    }

    else {
        sideType = "Scalene";
    }


    let angleType;

    if (
        Math.abs(A - 90) < 0.00001 ||
        Math.abs(B - 90) < 0.00001 ||
        Math.abs(C - 90) < 0.00001
    ) {
        angleType = "Right-angled";
    }

    else if (A > 90 || B > 90 || C > 90) {
        angleType = "Obtuse";
    }

    else {
        angleType = "Acute";
    }


    return `${angleType} and ${sideType}`;
}


// --------------------------------------------------
// Draw triangle
// --------------------------------------------------

function drawTriangle(a, b, c, A) {

    const canvas =
        document.getElementById("triangleCanvas");

    const ctx = canvas.getContext("2d");

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    const angleRadians =
        degreesToRadians(A);


    // Coordinates based on side c as the base

    let x1 = 80;
    let y1 = 350;

    let x2 = 520;
    let y2 = 350;


    const scale =
        440 / c;


    let x3 =
        x1 +
        b * Math.cos(angleRadians) * scale;

    let y3 =
        y1 -
        b * Math.sin(angleRadians) * scale;


    // Draw triangle

    ctx.beginPath();

    ctx.moveTo(x1, y1);

    ctx.lineTo(x2, y2);

    ctx.lineTo(x3, y3);

    ctx.closePath();

    ctx.strokeStyle = "#222";
    ctx.lineWidth = 3;

    ctx.stroke();


    // Vertex labels

    ctx.font = "bold 18px Arial";

    ctx.fillText("A", x1 - 20, y1 + 20);
    ctx.fillText("B", x2 + 10, y2 + 20);
    ctx.fillText("C", x3 + 10, y3 - 10);


    // Side labels

    ctx.font = "16px Arial";

    ctx.fillText(
        `c = ${c.toFixed(2)}`,
        (x1 + x2) / 2 - 20,
        y1 + 30
    );

    ctx.fillText(
        `b = ${b.toFixed(2)}`,
        (x1 + x3) / 2 - 20,
        (y1 + y3) / 2
    );

    ctx.fillText(
        `a = ${a.toFixed(2)}`,
        (x2 + x3) / 2 + 10,
        (y2 + y3) / 2
    );
}


// --------------------------------------------------
// Error message
// --------------------------------------------------

function showError(text) {

    document.getElementById("message").innerHTML =
        `<div class="error">${text}</div>`;

    document.getElementById("results")
        .classList.add("hidden");
}
