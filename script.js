const SIDE_KEYS = ["a", "b", "c"];
const ANGLE_KEYS = ["A", "B", "C"];
const rad = degrees => degrees * Math.PI / 180;
const deg = radians => radians * 180 / Math.PI;
const clamp = value => Math.max(-1, Math.min(1, value));
const closeSide = (x, y, tolerance = 1e-5) =>
    Math.abs(x - y) <= tolerance * Math.max(Math.abs(x), Math.abs(y));
const formatSide = value => Number(value.toPrecision(10)).toString();

// Convert three sides into the unique corresponding triangle.
function fromSides(a, b, c) {
    if (![a, b, c].every(x => Number.isFinite(x) && x > 0)) return null;
    const scale = Math.max(a, b, c);
    const [x, y, z] = [a / scale, b / scale, c / scale];
    if (!(x + y > z && x + z > y && y + z > x)) return null;
    const A = deg(Math.acos(clamp((y * y + z * z - x * x) / (2 * y * z))));
    const B = deg(Math.acos(clamp((x * x + z * z - y * y) / (2 * x * z))));
    const C = 180 - A - B;
    if (![A, B, C].every(angle => Number.isFinite(angle) && angle > 0)) {
        return null;
    }
    return { a, b, c, A, B, C };
}

function matchesGiven(triangle, given) {
    return SIDE_KEYS.every(key => given[key] === null ||
        closeSide(triangle[key], given[key])) &&
        ANGLE_KEYS.every(key => given[key] === null ||
            Math.abs(triangle[key] - given[key]) <= 0.001);
}

// Pure solver. Returns { solutions: [...] } or { error: "..." }.
// SSS, SAS, ASA/AAS and the one/two-solution SSA cases are supported.
function solveTriangleValues(raw) {
    const v = {};
    for (const key of [...SIDE_KEYS, ...ANGLE_KEYS]) {
        const value = raw[key];
        if (value === null || value === undefined || value === "") {
            v[key] = null;
        } else if (typeof value !== "number" || !Number.isFinite(value) ||
                   value <= 0 || (ANGLE_KEYS.includes(key) && value >= 180)) {
            return { error: ANGLE_KEYS.includes(key)
                ? "Each known angle must be greater than 0° and less than 180°."
                : "Each known side must be greater than zero." };
        } else {
            v[key] = value;
        }
    }
    const sides = SIDE_KEYS.filter(key => v[key] !== null);
    const angles = ANGLE_KEYS.filter(key => v[key] !== null);
    if (sides.length + angles.length < 3) {
        return { error: "Enter at least three known values." };
    }
    const angleSum = angles.reduce((sum, key) => sum + v[key], 0);
    if (angles.length === 3 && Math.abs(angleSum - 180) > 0.001) {
        return { error: "The three angles must add up to 180°." };
    }
    if (angles.length === 2 && angleSum >= 180) {
        return { error: "Two known angles must add up to less than 180°." };
    }
    if (!sides.length) {
        return { error: "Enter at least one side to determine the triangle's size." };
    }

    const candidates = [];
    if (sides.length === 3) {
        const t = fromSides(v.a, v.b, v.c);
        if (!t) return { error: "These side lengths cannot form a triangle." };
        candidates.push(t);
    } else if (angles.length >= 2) {
        const found = { A: v.A, B: v.B, C: v.C };
        const missing = ANGLE_KEYS.find(key => found[key] === null);
        if (missing) found[missing] = 180 - angleSum;
        if (ANGLE_KEYS.some(key => !(found[key] > 0 && found[key] < 180))) {
            return { error: "The provided angles cannot form a triangle." };
        }
        const first = sides[0];
        const ratio = v[first] / Math.sin(rad(
            found[ANGLE_KEYS[SIDE_KEYS.indexOf(first)]]
        ));
        const calculated = SIDE_KEYS.map((_, i) =>
            ratio * Math.sin(rad(found[ANGLE_KEYS[i]])));
        candidates.push(fromSides(...calculated));
    } else if (sides.length === 2 && angles.length === 1) {
        const missing = SIDE_KEYS.find(key => v[key] === null);
        const missingIndex = SIDE_KEYS.indexOf(missing);
        const givenAngle = angles[0];
        if (givenAngle === ANGLE_KEYS[missingIndex]) {
            // SAS: stable half-angle form of the Law of Cosines.
            const [first, second] = sides.map(key => v[key]);
            const scale = Math.max(first, second);
            const [x, y] = [first / scale, second / scale];
            const third = Math.hypot(
                x - y, 2 * Math.sqrt(x * y) * Math.sin(rad(v[givenAngle]) / 2)
            ) * scale;
            const complete = { a: v.a, b: v.b, c: v.c };
            complete[missing] = third;
            candidates.push(fromSides(complete.a, complete.b, complete.c));
        } else {
            // SSA: arcsin has an acute and a supplementary possibility.
            const pair = ANGLE_KEYS.indexOf(givenAngle);
            const other = SIDE_KEYS.indexOf(
                sides.find(key => key !== SIDE_KEYS[pair])
            );
            const sine = v[SIDE_KEYS[other]] * Math.sin(rad(v[givenAngle])) /
                v[SIDE_KEYS[pair]];
            if (sine <= 1 + 1e-12) {
                const acute = deg(Math.asin(clamp(sine)));
                const choices = sine >= 1 - 1e-12 ?
                    [90] : [acute, 180 - acute];
                for (const otherAngle of choices) {
                    const remainingAngle = 180 - v[givenAngle] - otherAngle;
                    if (remainingAngle <= 0) continue;
                    const third = v[SIDE_KEYS[pair]] *
                        Math.sin(rad(remainingAngle)) / Math.sin(rad(v[givenAngle]));
                    const complete = { a: v.a, b: v.b, c: v.c };
                    complete[missing] = third;
                    candidates.push(fromSides(complete.a, complete.b, complete.c));
                }
            }
        }
    }
    const solutions = [];
    for (const t of candidates) {
        if (!t || !matchesGiven(t, v)) continue;
        if (!solutions.some(existing => SIDE_KEYS.every(key =>
            closeSide(existing[key], t[key], 1e-9)))) {
            solutions.push(t);
        }
    }
    return solutions.length ? { solutions } :
        { error: "The provided values cannot describe one triangle." };
}

function readInput(id) {
    const text = document.getElementById(id).value.trim();
    return text === "" ? null : Number(text);
}

function solveTriangle() {
    const input = {
        a: readInput("sideA"), b: readInput("sideB"), c: readInput("sideC"),
        A: readInput("angleA"), B: readInput("angleB"), C: readInput("angleC")
    };
    const message = document.getElementById("message");
    const results = document.getElementById("results");
    const container = document.getElementById("solutions");
    message.replaceChildren();
    container.replaceChildren();
    results.classList.add("hidden");
    const outcome = solveTriangleValues(input);
    const note = document.createElement("div");
    note.className = outcome.error ? "error" : "success";
    note.textContent = outcome.error || (outcome.solutions.length === 2
        ? "Two valid triangles match these values."
        : "Triangle solved successfully!");
    message.appendChild(note);
    if (outcome.error) return;

    document.getElementById("solutionHeading").textContent =
        outcome.solutions.length === 2 ? "Triangle Solutions" : "Triangle Solution";
    outcome.solutions.forEach((t, index) => {
        const section = document.createElement("section");
        if (index > 0) {
            section.style.marginTop = "2rem";
            section.style.borderTop = "1px solid #ddd";
            section.style.paddingTop = "1rem";
        }
        if (outcome.solutions.length === 2) {
            const title = document.createElement("h3");
            title.textContent = "Solution " + (index + 1);
            section.appendChild(title);
        }
        const grid = document.createElement("div");
        grid.className = "results-grid";
        for (const group of [
            { name: "Sides", keys: SIDE_KEYS },
            { name: "Angles", keys: ANGLE_KEYS }
        ]) {
            const box = document.createElement("div");
            box.className = "result-box";
            const title = document.createElement("h3");
            title.textContent = group.name;
            box.appendChild(title);
            for (const key of group.keys) {
                const line = document.createElement("p");
                line.appendChild(document.createTextNode(
                    (group.name === "Sides" ? "Side " : "Angle ") + key + ": "
                ));
                const value = document.createElement("strong");
                value.textContent = group.name === "Sides" ?
                    formatSide(t[key]) : t[key].toFixed(4) + "°";
                line.appendChild(value);
                box.appendChild(line);
            }
            grid.appendChild(box);
        }
        section.appendChild(grid);
        const classification = document.createElement("div");
        classification.className = "classification";
        const title = document.createElement("h2");
        title.textContent = "Triangle Classification";
        const type = document.createElement("p");
        type.textContent = identifyTriangleType(t);
        classification.append(title, type);
        section.appendChild(classification);
        const diagramTitle = document.createElement("h2");
        diagramTitle.textContent = "Triangle Diagram";
        const canvas = document.createElement("canvas");
        if (index === 0) canvas.id = "triangleCanvas";
        canvas.width = 600;
        canvas.height = 450;
        canvas.style.display = "block";
        canvas.style.maxWidth = "100%";
        canvas.style.margin = "1rem auto";
        canvas.style.border = "1px solid #ddd";
        canvas.style.borderRadius = "8px";
        canvas.setAttribute("aria-label", "Diagram for solution " + (index + 1));
        section.append(diagramTitle, canvas);
        container.appendChild(section);
        drawTriangle(canvas, t);
    });
    results.classList.remove("hidden");
}

function identifyTriangleType({ a, b, c, A, B, C }) {
    const same = (x, y) => closeSide(x, y, 1e-8);
    const sides = same(a, b) && same(b, c) ? "Equilateral" :
        same(a, b) || same(b, c) || same(a, c) ? "Isosceles" : "Scalene";
    const angles = [A, B, C].some(x => Math.abs(x - 90) <= 1e-7) ?
        "Right-angled" : [A, B, C].some(x => x > 90) ? "Obtuse" : "Acute";
    return angles + " and " + sides;
}

function drawTriangle(canvas, { a, b, c, A }) {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const vertices = [
        { x: 0, y: 0 }, { x: c, y: 0 },
        { x: b * Math.cos(rad(A)), y: b * Math.sin(rad(A)) }
    ];
    const left = Math.min(...vertices.map(p => p.x));
    const right = Math.max(...vertices.map(p => p.x));
    const bottom = Math.min(...vertices.map(p => p.y));
    const top = Math.max(...vertices.map(p => p.y));
    const scale = Math.min(440 / (right - left), 290 / (top - bottom));
    const offsetX = (canvas.width - (right - left) * scale) / 2;
    const offsetY = (canvas.height - (top - bottom) * scale) / 2;
    const [P, Q, R] = vertices.map(p => ({
        x: offsetX + (p.x - left) * scale,
        y: canvas.height - offsetY - (p.y - bottom) * scale
    }));
    ctx.beginPath();
    ctx.moveTo(P.x, P.y);
    ctx.lineTo(Q.x, Q.y);
    ctx.lineTo(R.x, R.y);
    ctx.closePath();
    ctx.strokeStyle = "#222";
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.fillStyle = "#222";
    ctx.font = "bold 18px Arial";
    ctx.fillText("A", P.x - 20, P.y + 20);
    ctx.fillText("B", Q.x + 10, Q.y + 20);
    ctx.fillText("C", R.x + 10, R.y - 10);
    ctx.font = "16px Arial";
    ctx.fillText("c = " + formatSide(c), (P.x + Q.x) / 2 - 20, P.y + 30);
    ctx.fillText("b = " + formatSide(b), (P.x + R.x) / 2 - 20,
        (P.y + R.y) / 2);
    ctx.fillText("a = " + formatSide(a), (Q.x + R.x) / 2 + 10,
        (Q.y + R.y) / 2);
}
