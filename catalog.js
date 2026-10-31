/* Open Learning resource catalog. Edit this file to add or retitle a resource; index.html renders from it.
   builds_on lists the ids of sheets a resource assumes you already know; the page shows them as "Builds on" and the reverse as "Leads to". */
window.OPEN_LEARNING_CATALOG = {
 "site": {
  "name": "Open Learning",
  "by": "Learning Curve Collective",
  "base": "https://learningcurvecollective.github.io/learning-curve-collective-resources/",
  "home": "https://learningcurvecollective.com",
  "description": "A growing collection of free, interactive learning resources informed by rigorous academic curricula and designed to make challenging concepts accessible to every learner.",
  "updated": "2026-10-30"
 },
 "levels": [
  "Foundations",
  "High School",
  "Advanced High School",
  "College",
  "Advanced College",
  "Graduate"
 ],
 "formats": [
  "Cheat sheet",
  "Diagnostic",
  "Evaluation",
  "Interactive worksheet",
  "Organizer",
  "Playbook",
  "Practice set",
  "Practice test",
  "Step-through",
  "Study guide",
  "Study sheet",
  "Walkthrough"
 ],
 "areas": [
  {
   "key": "math",
   "name": "Mathematics",
   "page": "math.html",
   "blurb": "Algebra through multivariable calculus and statistics, listed in the order you meet it in a course."
  },
  {
   "key": "test-prep",
   "name": "Test Prep",
   "page": "test-prep.html",
   "blurb": "Diagnostics, topic practice, full tests, and test-day playbooks built around the digital SAT, the ACT, and the GRE."
  },
  {
   "key": "econ",
   "name": "Economics",
   "page": "economics.html",
   "blurb": "Principles, microeconomics, environmental and public economics, and econometrics."
  },
  {
   "key": "science",
   "name": "Science",
   "page": "science.html",
   "blurb": "Interactive physics labs, biology foundations, and clinical study sheets."
  },
  {
   "key": "ml",
   "name": "Machine Learning & Data",
   "page": "machine-learning.html",
   "blurb": "Algorithms stepped through by hand, plus the math and statistics behind them."
  },
  {
   "key": "social",
   "name": "Social Science",
   "page": "social-science.html",
   "blurb": "Psychology research methods and study sheets."
  }
 ],
 "subjects": [
  {
   "key": "algebra",
   "name": "Algebra",
   "area": "math",
   "blurb": "Foundations, functions, and symbolic reasoning."
  },
  {
   "key": "geometry",
   "name": "Geometry",
   "area": "math",
   "blurb": "Shapes, constructions, and spatial reasoning."
  },
  {
   "key": "precalc",
   "name": "Precalculus",
   "area": "math",
   "blurb": "The bridge from algebra to calculus."
  },
  {
   "key": "calculus",
   "name": "Calculus",
   "area": "math",
   "blurb": "Rates of change, integrals, and multivariable ideas."
  },
  {
   "key": "stats",
   "name": "Statistics",
   "area": "math",
   "blurb": "Describing data and reasoning about uncertainty."
  },
  {
   "key": "sat",
   "name": "SAT & PSAT",
   "area": "test-prep",
   "blurb": "Reading, writing, and math sheets built around the digital SAT."
  },
  {
   "key": "act",
   "name": "ACT",
   "area": "test-prep",
   "blurb": "Grammar, math, and science practice for the ACT."
  },
  {
   "key": "gre",
   "name": "GRE",
   "area": "test-prep",
   "blurb": "Quant topic sheets, a full practice test, and the Issue essay."
  },
  {
   "key": "econ",
   "name": "Economics",
   "area": "econ",
   "blurb": "Principles, micro, environmental, public econ, and econometrics."
  },
  {
   "key": "physics",
   "name": "Physics",
   "area": "science",
   "blurb": "Interactive labs for fields and circuits."
  },
  {
   "key": "biology",
   "name": "Biology",
   "area": "science",
   "blurb": "The chemistry of life and beyond."
  },
  {
   "key": "machine-learning",
   "name": "Machine Learning & Data",
   "area": "ml",
   "blurb": "Algorithms stepped through by hand, plus the math behind them."
  },
  {
   "key": "psychology",
   "name": "Psychology",
   "area": "social",
   "blurb": "Research methods and study sheets."
  },
  {
   "key": "medicine",
   "name": "Medicine",
   "area": "science",
   "blurb": "Graduate-level study sheets for clinical topics."
  }
 ],
 "resources": [
  {
   "id": "algebra--factoring-worksheet",
   "path": "algebra/factoring-worksheet.html",
   "title": "Factoring",
   "description": "Work through GCF, grouping, trinomials, squares and cubes with a cheat sheet, challenge problems, and timed practice that checks your answers.",
   "subject": "algebra",
   "topic": "Foundations",
   "order": 1,
   "levels": [
    "Foundations",
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "factoring",
    "gcf",
    "grouping",
    "trinomials",
    "difference of squares",
    "sum of cubes"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "algebra--algebra-review-solving-systems-and-quadratics",
   "path": "algebra/algebra-review-solving-systems-and-quadratics.html",
   "title": "Algebra Review: Solving Systems & Quadratics",
   "description": "Review 2x2 and 3x3 systems and quadratic forms, then explore parabolas with sliders and solve fitting and word problems.",
   "subject": "algebra",
   "topic": "Foundations",
   "order": 2,
   "levels": [
    "Foundations",
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "systems of equations",
    "3x3 systems",
    "quadratics",
    "parabolas",
    "word problems",
    "algebra review"
   ],
   "content": "theory+practice",
   "builds_on": [
    "algebra--factoring-worksheet"
   ]
  },
  {
   "id": "algebra--parent-functions-transformations-worksheet",
   "path": "algebra/parent_functions_transformations_worksheet.html",
   "title": "Parent Functions & Transformations",
   "description": "Explore a library of parent functions, use sliders to see how a, h and k shift graphs, then drag and practice.",
   "subject": "algebra",
   "topic": "Functions",
   "order": 3,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "parent functions",
    "transformations",
    "function graphs",
    "shifts and stretches",
    "key points"
   ],
   "featured": 2,
   "content": "theory+practice",
   "builds_on": [
    "algebra--algebra-review-solving-systems-and-quadratics"
   ]
  },
  {
   "id": "algebra--polynomials-rational-functions-worksheet",
   "path": "algebra/polynomials_rational_functions_worksheet.html",
   "title": "Polynomials & Rational Functions",
   "description": "Study polynomial functions and rational function asymptote rules with concept summaries, then check your understanding on a set of practice problems.",
   "subject": "algebra",
   "topic": "Functions",
   "order": 4,
   "levels": [
    "High School"
   ],
   "format": "Study sheet",
   "tags": [
    "polynomials",
    "rational functions",
    "asymptotes",
    "end behavior",
    "degree"
   ],
   "content": "theory+practice",
   "builds_on": [
    "algebra--factoring-worksheet",
    "algebra--parent-functions-transformations-worksheet"
   ]
  },
  {
   "id": "algebra--walkthrough-proof-rational-roots-theorem",
   "path": "algebra/walkthrough-proof-rational-roots-theorem.html",
   "title": "Rational Root Theorem: Proof Walkthrough",
   "description": "Step through a proof of the Rational Root Theorem, moving from key definitions and build-up examples to a concrete case and the general proof.",
   "subject": "algebra",
   "topic": "Proofs",
   "order": 5,
   "levels": [
    "High School",
    "Advanced High School"
   ],
   "format": "Walkthrough",
   "tags": [
    "rational root theorem",
    "proof",
    "polynomial roots",
    "factors",
    "integer coefficients"
   ],
   "content": "theory",
   "builds_on": [
    "algebra--polynomials-rational-functions-worksheet"
   ]
  },
  {
   "id": "geometry--triangle-centers",
   "path": "geometry/triangle_centers.html",
   "title": "Triangle Centers",
   "description": "Drag the vertices of a triangle to see how the centroid, incenter, circumcenter and orthocenter are built and where they move.",
   "subject": "geometry",
   "topic": "Triangles",
   "order": 1,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "centroid",
    "incenter",
    "circumcenter",
    "orthocenter",
    "triangle geometry",
    "medians"
   ],
   "content": "theory",
   "builds_on": []
  },
  {
   "id": "precalc--exponential-logarithmic-worksheet",
   "path": "precalc/exponential-logarithmic-worksheet.html",
   "title": "Exponential & Logarithmic Functions",
   "description": "Use interactive visualizers to explore exponential and logarithmic functions, then solve equations, apply growth formulas, and practice with checked problems.",
   "subject": "precalc",
   "topic": "Functions & their graphs",
   "order": 1,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "exponential functions",
    "logarithms",
    "solving equations",
    "growth and decay",
    "log properties"
   ],
   "content": "theory+practice",
   "builds_on": [
    "algebra--parent-functions-transformations-worksheet"
   ]
  },
  {
   "id": "precalc--asymptotes-discontinuities-worksheet",
   "path": "precalc/asymptotes-discontinuities-worksheet.html",
   "title": "Asymptotes & Discontinuities",
   "description": "Find holes, vertical, horizontal and slant asymptotes of rational functions using a cheat sheet, guided sections, practice problems, and a timed sprint.",
   "subject": "precalc",
   "topic": "Functions & their graphs",
   "order": 2,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "asymptotes",
    "holes",
    "rational functions",
    "end behavior",
    "slant asymptotes",
    "discontinuities"
   ],
   "content": "theory+practice",
   "builds_on": [
    "algebra--polynomials-rational-functions-worksheet"
   ]
  },
  {
   "id": "precalc--conic-sections-worksheet",
   "path": "precalc/conic_sections_worksheet.html",
   "title": "Conic Sections",
   "description": "Explore circles, parabolas, ellipses and hyperbolas with a 3D cone slicer, sliders, classification practice, polar form, and applications.",
   "subject": "precalc",
   "topic": "Analytic geometry",
   "order": 3,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "conic sections",
    "ellipse",
    "hyperbola",
    "parabola",
    "circle",
    "polar form"
   ],
   "content": "theory+practice",
   "builds_on": [
    "algebra--algebra-review-solving-systems-and-quadratics"
   ]
  },
  {
   "id": "precalc--polar-and-parametric-equations",
   "path": "precalc/polar_and_parametric_equations.html",
   "title": "Polar Graphs & Parametric Equations",
   "description": "Graph polar and parametric curves with a gallery and visualizer, practice converting coordinates, solve applied models, and try AP-style challenge problems.",
   "subject": "precalc",
   "topic": "Analytic geometry",
   "order": 4,
   "levels": [
    "High School",
    "Advanced High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "polar graphs",
    "parametric equations",
    "coordinate conversion",
    "rose curves",
    "applied models"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "precalc--sequences-series-worksheet",
   "path": "precalc/sequences_series_worksheet.html",
   "title": "Sequences & Series",
   "description": "Visualize sequences, learn arithmetic and geometric formulas, practice sigma notation and telescoping sums, and see series applied in real situations.",
   "subject": "precalc",
   "topic": "Sequences",
   "order": 5,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "arithmetic sequences",
    "geometric sequences",
    "sigma notation",
    "telescoping series",
    "series formulas"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "calculus--average-and-instantaneous-rate-of-change",
   "path": "calculus/average-and-instantaneous-rate-of-change.html",
   "title": "Average & Instantaneous Rate of Change",
   "description": "Drag h toward zero to watch a secant line become a tangent, then work examples and two practice rounds with new numbers.",
   "subject": "calculus",
   "topic": "Limits & derivatives",
   "order": 1,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "rate of change",
    "secant line",
    "tangent line",
    "difference quotient",
    "limits"
   ],
   "content": "theory+practice",
   "builds_on": [
    "algebra--parent-functions-transformations-worksheet"
   ]
  },
  {
   "id": "calculus--derivative-definition-continuity-differentiability-study-sheet",
   "path": "calculus/derivative-definition-continuity-differentiability-study-sheet.html",
   "title": "The Derivative: Definition, Continuity & Differentiability",
   "description": "Review the limit definition of the derivative, continuity, differentiability and the IVT with a cheat sheet, worked problems, flashcards, and timed practice.",
   "subject": "calculus",
   "topic": "Limits & derivatives",
   "order": 2,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "derivative definition",
    "continuity",
    "differentiability",
    "intermediate value theorem",
    "limits"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--average-and-instantaneous-rate-of-change"
   ]
  },
  {
   "id": "calculus--power-rule-study-sheet",
   "path": "calculus/power-rule-study-sheet.html",
   "title": "Power Rule Study Sheet: Derivative Shortcuts",
   "description": "Learn the power rule, rewrite roots and fractions before differentiating, and find tangent and normal lines using worked problems, flashcards, and timed practice.",
   "subject": "calculus",
   "topic": "Limits & derivatives",
   "order": 3,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "power rule",
    "derivatives",
    "tangent lines",
    "normal lines",
    "rewriting expressions"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--derivative-definition-continuity-differentiability-study-sheet"
   ]
  },
  {
   "id": "calculus--differentiation-part-1",
   "path": "calculus/differentiation-part-1.html",
   "title": "Derivatives Part 1: Rules & Toolkit",
   "description": "Build a derivative toolkit by reviewing foundations, then learning and practicing the power, product, quotient and chain rules with interactive graphs.",
   "subject": "calculus",
   "topic": "Limits & derivatives",
   "order": 4,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "power rule",
    "product rule",
    "quotient rule",
    "chain rule",
    "derivative rules"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--power-rule-study-sheet"
   ]
  },
  {
   "id": "calculus--product-and-quotient-rule-practice",
   "path": "calculus/product-and-quotient-rule-practice.html",
   "title": "Product & Quotient Rule Practice",
   "description": "Drill the product and quotient rules and then tangent lines in 18 problems with new numbers, with flashcards and a timer.",
   "subject": "calculus",
   "topic": "Limits & derivatives",
   "order": 5,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Practice set",
   "tags": [
    "product rule",
    "quotient rule",
    "tangent lines",
    "derivatives",
    "practice problems"
   ],
   "difficulty": "Core",
   "content": "practice",
   "builds_on": [
    "calculus--differentiation-part-1"
   ]
  },
  {
   "id": "calculus--differentiation-rules-study-sheet",
   "path": "calculus/differentiation-rules-study-sheet.html",
   "title": "Differentiation Rules: Power, Product, Quotient & Trig",
   "description": "Review the power, product, quotient and trig rules with proofs, table and graph problems, tangent lines, flashcards, a timed sprint and two mock tests.",
   "subject": "calculus",
   "topic": "Limits & derivatives",
   "order": 6,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "product rule",
    "quotient rule",
    "trig derivatives",
    "tangent lines",
    "derivative rules",
    "AP Calculus"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--differentiation-part-1"
   ]
  },
  {
   "id": "calculus--differentiation-part-2",
   "path": "calculus/differentiation-part-2.html",
   "title": "Derivatives Part 2: Chain Rule & Beyond",
   "description": "Practice nested chain rule, implicit and inverse function derivatives, log differentiation, related rates, and linear approximation with interactive graphs and mixed problems.",
   "subject": "calculus",
   "topic": "Limits & derivatives",
   "order": 7,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "chain rule",
    "implicit differentiation",
    "inverse functions",
    "log differentiation",
    "related rates",
    "linear approximation"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--differentiation-part-1",
    "calculus--product-and-quotient-rule-practice"
   ]
  },
  {
   "id": "calculus--related-rates-study-sheet",
   "path": "calculus/related-rates-study-sheet.html",
   "title": "Related Rates Study Sheet",
   "description": "Learn a step-by-step process for related rates, with a geometry toolbox, sign and snapshot practice, worked examples, flashcards, and practice problems.",
   "subject": "calculus",
   "topic": "Applications of derivatives",
   "order": 8,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "related rates",
    "implicit differentiation",
    "geometry formulas",
    "rates of change",
    "ap calculus"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--differentiation-part-2"
   ]
  },
  {
   "id": "calculus--ivt-evt-mvt-extrema-sheet",
   "path": "calculus/IVT_EVT_MVT_Extrema_Sheet.html",
   "title": "IVT, EVT, MVT & Extrema: Existence Theorems",
   "description": "Quick reference for the Intermediate Value, Extreme Value and Mean Value Theorems, with max and min rules, AP justification language, and practice.",
   "subject": "calculus",
   "topic": "Applications of derivatives",
   "order": 9,
   "levels": [
    "Advanced High School"
   ],
   "format": "Cheat sheet",
   "tags": [
    "intermediate value theorem",
    "extreme value theorem",
    "mean value theorem",
    "extrema",
    "ap justification"
   ],
   "content": "reference",
   "builds_on": [
    "calculus--derivative-definition-continuity-differentiability-study-sheet"
   ]
  },
  {
   "id": "calculus--practice-extrema-mvt-worksheet",
   "path": "calculus/practice-extrema-mvt-worksheet.html",
   "title": "Extrema & the Mean Value Theorem: Practice",
   "description": "Practice absolute and local extrema and the Mean Value Theorem using a one-page cheat sheet, a concept sprint, and problem sets.",
   "subject": "calculus",
   "topic": "Applications of derivatives",
   "order": 10,
   "levels": [
    "Advanced High School"
   ],
   "format": "Practice set",
   "tags": [
    "absolute extrema",
    "local extrema",
    "mean value theorem",
    "critical points",
    "ap calculus ab"
   ],
   "content": "practice",
   "builds_on": [
    "calculus--ivt-evt-mvt-extrema-sheet"
   ]
  },
  {
   "id": "calculus--derivative-tests-study-sheet",
   "path": "calculus/Derivative Tests Study Sheet.html",
   "title": "Derivative Tests & Justification Study Sheet",
   "description": "Use first and second derivative tests to find extrema and concavity, read graphs of f prime, analyze particle motion, and practice writing justifications.",
   "subject": "calculus",
   "topic": "Applications of derivatives",
   "order": 11,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "first derivative test",
    "second derivative test",
    "concavity",
    "inflection points",
    "particle motion",
    "justification"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--practice-extrema-mvt-worksheet"
   ]
  },
  {
   "id": "calculus--applications-of-differentiation",
   "path": "calculus/applications_of_differentiation.html",
   "title": "Applications of Differentiation",
   "description": "Explore extrema, the Mean Value Theorem, curve shape, sketching, and optimization with interactive visualizers, a reference tab, and practice problems.",
   "subject": "calculus",
   "topic": "Applications of derivatives",
   "order": 12,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "extrema",
    "mean value theorem",
    "curve sketching",
    "optimization",
    "concavity"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--derivative-tests-study-sheet",
    "calculus--related-rates-study-sheet"
   ]
  },
  {
   "id": "calculus--integration-methods-and-practice",
   "path": "calculus/integration_methods_and_practice.html",
   "title": "Integration: Methods & Practice",
   "description": "Approximate area under a curve, review theory, and learn integration techniques with practice sets organized by AB, BC, and advanced levels.",
   "subject": "calculus",
   "topic": "Integration",
   "order": 13,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "integration techniques",
    "riemann sums",
    "area under a curve",
    "integration by parts",
    "u-substitution",
    "ap calculus bc"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--differentiation-part-2"
   ]
  },
  {
   "id": "calculus--disk-washer-method-practice",
   "path": "calculus/disk-washer-method-practice.html",
   "title": "Disk vs Washer Method Organizer",
   "description": "Compare the disk and washer methods for volumes of revolution with a decision flow, common traps, and practice problems.",
   "subject": "calculus",
   "topic": "Integration",
   "order": 14,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Organizer",
   "tags": [
    "disk method",
    "washer method",
    "volume of revolution",
    "solids of revolution",
    "integration"
   ],
   "content": "reference",
   "builds_on": [
    "calculus--integration-methods-and-practice"
   ]
  },
  {
   "id": "calculus--moments-physics-and-probability",
   "path": "calculus/moments-physics-and-probability.html",
   "title": "Moments, Center of Mass & Expected Value",
   "description": "See how center of mass and expected value share one idea, with interactive rods, laminas, 3D solids, and second moments to practice.",
   "subject": "calculus",
   "topic": "Integration",
   "order": 15,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "center of mass",
    "expected value",
    "moments",
    "weighted averages",
    "lamina",
    "moment of inertia"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--integration-methods-and-practice"
   ]
  },
  {
   "id": "calculus--numerical-integration-convergence-with-taylor-series",
   "path": "calculus/numerical-integration-convergence-with-taylor-series.html",
   "title": "Midpoint Rule Convergence: Taylor Proof",
   "description": "Follow a Taylor series proof of midpoint rule convergence, with a visualizer and comparisons to left, right and trapezoidal sums.",
   "subject": "calculus",
   "topic": "Integration",
   "order": 16,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Walkthrough",
   "tags": [
    "midpoint rule",
    "numerical integration",
    "taylor series",
    "error bounds",
    "trapezoidal rule"
   ],
   "content": "theory",
   "builds_on": [
    "calculus--integration-methods-and-practice",
    "precalc--sequences-series-worksheet"
   ]
  },
  {
   "id": "calculus--directional-derivative-worksheet",
   "path": "calculus/directional_derivative_worksheet.html",
   "title": "Gradient & Directional Derivatives",
   "description": "Learn the gradient, directional derivatives, and constrained optimization from core formulas, with interactive graphs, drag activities, and practice problems.",
   "subject": "calculus",
   "topic": "Multivariable",
   "order": 17,
   "levels": [
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "gradient",
    "directional derivative",
    "partial derivatives",
    "constrained optimization",
    "multivariable calculus"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--differentiation-part-2"
   ]
  },
  {
   "id": "calculus--lagrange-multiplier-worksheet",
   "path": "calculus/lagrange_multiplier_worksheet.html",
   "title": "Lagrange Multipliers: Complete Guide",
   "description": "Learn constrained optimization with theory and geometry, a step-by-step algorithm, solved problems, Desmos graphs, and cases where the method fails.",
   "subject": "calculus",
   "topic": "Multivariable",
   "order": 18,
   "levels": [
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "lagrange multipliers",
    "constrained optimization",
    "gradient",
    "level curves",
    "multivariable calculus"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--directional-derivative-worksheet",
    "calculus--applications-of-differentiation"
   ]
  },
  {
   "id": "calculus--double-integrals",
   "path": "calculus/double_integrals.html",
   "title": "Double Integrals: Theory & Visualization",
   "description": "Understand double integrals through visuals, theory, and integration techniques, then practice problems including the Gaussian integral.",
   "subject": "calculus",
   "topic": "Multivariable",
   "order": 19,
   "levels": [
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "double integrals",
    "iterated integrals",
    "volume",
    "gaussian integral",
    "multivariable calculus"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--integration-methods-and-practice",
    "calculus--directional-derivative-worksheet"
   ]
  },
  {
   "id": "calculus--line-integral-worksheet",
   "path": "calculus/line_integral_worksheet.html",
   "title": "Line Integrals: Three Types",
   "description": "Work through line integrals with respect to arc length, coordinates, and vector fields, with practice for each type and a unifying summary.",
   "subject": "calculus",
   "topic": "Multivariable",
   "order": 20,
   "levels": [
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "line integrals",
    "arc length",
    "vector fields",
    "work",
    "parametrization",
    "calculus iii"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--double-integrals"
   ]
  },
  {
   "id": "calculus--projection-to-gradient-descent-conceptual-map",
   "path": "calculus/projection-to-gradient-descent-conceptual-map.html",
   "title": "From Projection to Gradient Descent",
   "description": "Follow a step-by-step chain from scalar components and directional derivatives to surface normals and the gradient descent algorithm used in machine learning.",
   "subject": "calculus",
   "topic": "Multivariable",
   "order": 21,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Walkthrough",
   "tags": [
    "gradient descent",
    "projection",
    "directional derivative",
    "surface normals",
    "optimization",
    "machine learning"
   ],
   "content": "theory",
   "builds_on": [
    "calculus--directional-derivative-worksheet"
   ]
  },
  {
   "id": "stats--variance-standard-deviation-standard-error-organizer",
   "path": "stats/variance-standard-deviation-standard-error-organizer.html",
   "title": "Variance, SD, SE + Covariance & Correlation",
   "description": "Compare variance, standard deviation, standard error, covariance and correlation side by side in a cheat sheet organizer with practice questions.",
   "subject": "stats",
   "topic": "Descriptive statistics",
   "order": 1,
   "levels": [
    "College"
   ],
   "format": "Organizer",
   "tags": [
    "variance",
    "standard deviation",
    "standard error",
    "covariance",
    "correlation"
   ],
   "content": "reference",
   "builds_on": []
  },
  {
   "id": "physics--electric-fields-interactive",
   "path": "physics/electric_fields_interactive.html",
   "title": "Electric Fields: Interactive Worksheet",
   "description": "Place and adjust point charges on a live field visualizer, then review the formulas and theory and check your understanding with practice questions.",
   "subject": "physics",
   "topic": "Electricity & magnetism",
   "order": 1,
   "levels": [
    "High School",
    "Advanced High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "electric fields",
    "electrostatics",
    "point charges",
    "coulomb's law",
    "physics"
   ],
   "featured": 3,
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "physics--circuits-interactive",
   "path": "physics/circuits-interactive.html",
   "title": "Circuits: Interactive Lab",
   "description": "Drag batteries and bulbs onto a board in series or parallel mode, watch current, voltage, and power change, then practice with problems.",
   "subject": "physics",
   "topic": "Electricity & magnetism",
   "order": 2,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "circuits",
    "series and parallel",
    "current",
    "voltage",
    "power",
    "physics"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "biology--chemistry-of-life-study-sheet",
   "path": "biology/Chemistry_of_Life_Study_Sheet.html",
   "title": "The Chemistry of Life: Atoms, Bonds & Water",
   "description": "Learn how atoms, bonds, and water underlie biology, with key terms, an atom builder, flashcards, and a self-quiz for review.",
   "subject": "biology",
   "topic": "Foundations",
   "order": 1,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "atoms",
    "chemical bonds",
    "water",
    "biochemistry",
    "intro biology"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "econ--econ-graphs-master-cheatsheet",
   "path": "econ/econ-graphs-master-cheatsheet.html",
   "title": "Econ Graphs: Master Cheat Sheet",
   "description": "Graph-by-graph reference for micro and macro, from supply and demand to AD-AS and exchange rates, with shifter tables, sliders, and quiz questions.",
   "subject": "econ",
   "topic": "Reference sheets",
   "order": 1,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Cheat sheet",
   "tags": [
    "graphs",
    "supply & demand",
    "cost curves",
    "aggregate demand",
    "shifters",
    "reference"
   ],
   "content": "reference",
   "builds_on": []
  },
  {
   "id": "econ--market-structure-organizer",
   "path": "econ/market_structure_organizer.html",
   "title": "Market Structure Organizer",
   "description": "Side-by-side comparison of perfect competition, monopolistic competition, oligopoly, and monopoly by firms, products, entry barriers, and price control, plus market dynamics.",
   "subject": "econ",
   "topic": "Reference sheets",
   "order": 2,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Organizer",
   "tags": [
    "market structure",
    "perfect competition",
    "monopoly",
    "oligopoly",
    "comparison"
   ],
   "difficulty": "Intro",
   "content": "reference",
   "builds_on": [
    "econ--cost-curves-profit-max-micro"
   ]
  },
  {
   "id": "econ--principles-of-econ--principles-of-econ-midterm-2-study-sheet",
   "path": "econ/Principles of Econ/Principles of Econ - Midterm 2 Study Sheet.html",
   "title": "Principles of Economics: Taxes, Firms, Labor & Consumer Choice",
   "description": "Cheat sheet, study guide, flashcards, and worked practice covering taxes, externalities, costs, competition, monopoly, labor, and consumer choice, with a numbers drill.",
   "subject": "econ",
   "topic": "Principles of economics",
   "order": 3,
   "levels": [
    "Advanced High School",
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "taxes",
    "externalities",
    "public goods",
    "monopoly",
    "labor",
    "consumer choice"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "econ--micro--micro-module0-math-foundations",
   "path": "econ/micro/Micro_Module0_Math_Foundations.html",
   "title": "Math Foundations for Microeconomics",
   "description": "Review of the math behind micro: derivatives, optimization, partial derivatives, exponents, logs, and systems of equations, with interactive graphs and a mixed practice set.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 4,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "derivatives",
    "optimization",
    "partial derivatives",
    "logarithms",
    "systems of equations",
    "micro math"
   ],
   "difficulty": "Intro",
   "content": "theory+practice",
   "builds_on": [
    "calculus--differentiation-part-1"
   ]
  },
  {
   "id": "econ--micro--preferences-utility-budget-micro",
   "path": "econ/micro/preferences-utility-budget-micro.html",
   "title": "Preferences, Utility & the Budget",
   "description": "Builds consumer theory from preferences, utility, marginal utility, and MRS through the budget line, using interactive graphs, a function tour, and bonus slope practice.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 5,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "preferences",
    "utility",
    "MRS",
    "budget line",
    "indifference curves",
    "consumer theory"
   ],
   "difficulty": "Core",
   "content": "theory+practice",
   "builds_on": [
    "econ--micro--micro-module0-math-foundations",
    "econ--principles-of-econ--principles-of-econ-midterm-2-study-sheet"
   ]
  },
  {
   "id": "econ--micro--consumer-optimum-micro",
   "path": "econ/micro/consumer-optimum-micro.html",
   "title": "Solving the Consumer's Problem",
   "description": "Combines preferences and the budget line to find the optimal bundle using the tangency rule, with Cobb-Douglas, quasilinear, substitutes, and complements cases plus practice.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 6,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "consumer optimum",
    "tangency",
    "Cobb-Douglas",
    "quasilinear",
    "Lagrange",
    "utility maximization"
   ],
   "difficulty": "Core",
   "content": "theory+practice",
   "builds_on": [
    "econ--micro--preferences-utility-budget-micro"
   ]
  },
  {
   "id": "econ--demand-curves-micro",
   "path": "econ/demand-curves-micro.html",
   "title": "From Optimum to Demand",
   "description": "Extends the consumer optimum to a full demand curve by varying price, with interactive graphs for Cobb-Douglas, quasilinear, complements, and substitutes.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 7,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "demand curves",
    "consumer theory",
    "Cobb-Douglas",
    "quasilinear",
    "complements",
    "substitutes"
   ],
   "difficulty": "Core",
   "content": "theory",
   "builds_on": [
    "econ--micro--consumer-optimum-micro"
   ]
  },
  {
   "id": "econ--elasticity-micro",
   "path": "econ/elasticity-micro.html",
   "title": "Elasticity & Market Demand",
   "description": "Explains elasticity and market demand along a line and with constant elasticity, linking revenue and marginal revenue to income and cross elasticities, with practice.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 8,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "elasticity",
    "market demand",
    "marginal revenue",
    "income elasticity",
    "cross elasticity",
    "revenue"
   ],
   "difficulty": "Core",
   "content": "theory+practice",
   "builds_on": [
    "econ--demand-curves-micro"
   ]
  },
  {
   "id": "econ--income-substitution-effects-micro",
   "path": "econ/income-substitution-effects-micro.html",
   "title": "Income & Substitution Effects",
   "description": "Splits a price change into substitution and income effects using the Slutsky and Hicks methods, with interactive graphs, comparison, and practice.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 9,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "income effect",
    "substitution effect",
    "Slutsky",
    "Hicks",
    "Giffen goods",
    "demand"
   ],
   "difficulty": "Core",
   "content": "theory+practice",
   "builds_on": [
    "econ--demand-curves-micro"
   ]
  },
  {
   "id": "econ--micro--giffen-vs-ordinary-goods-micro",
   "path": "econ/micro/giffen-vs-ordinary-goods-micro.html",
   "title": "Normal, Inferior & Giffen Goods",
   "description": "Sorts goods as normal, inferior, or Giffen by separating substitution and income effects, with a lab, a three-step chain, practice, and a classification game.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 10,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "Giffen goods",
    "inferior goods",
    "normal goods",
    "income effect",
    "substitution effect",
    "classification"
   ],
   "difficulty": "Challenge",
   "content": "theory+practice",
   "builds_on": [
    "econ--income-substitution-effects-micro"
   ]
  },
  {
   "id": "econ--micro--midterm1-review-micro",
   "path": "econ/micro/midterm1-review-micro.html",
   "title": "Advanced Microeconomics: Unit 1 Study Guide",
   "description": "Unit 1 consumer theory and exchange economy review with a formula cheat sheet, flashcards, box match, study guide tabs, practice, and timed quizzes.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 11,
   "levels": [
    "Advanced College"
   ],
   "format": "Study guide",
   "tags": [
    "consumer theory",
    "utility",
    "budget",
    "exchange economy",
    "formulas",
    "flashcards"
   ],
   "content": "theory+practice",
   "builds_on": [
    "econ--micro--giffen-vs-ordinary-goods-micro",
    "econ--micro--exchange-economy-ge-micro"
   ]
  },
  {
   "id": "econ--cost-curves-profit-max-micro",
   "path": "econ/cost-curves-profit-max-micro.html",
   "title": "Cost Curves, Revenue & Profit Maximization",
   "description": "Walks through production, revenue, cost curves, and profit maximization for a firm, with interactive graphs, practice problems, and a bonus on Nash versus Pareto.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 12,
   "levels": [
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "cost curves",
    "profit maximization",
    "production",
    "marginal revenue",
    "firm theory",
    "Pareto"
   ],
   "difficulty": "Core",
   "content": "theory+practice",
   "builds_on": [
    "econ--elasticity-micro"
   ]
  },
  {
   "id": "econ--game-theory--game-theory-micro",
   "path": "econ/game-theory/game-theory-micro.html",
   "title": "Game Theory",
   "description": "Introduces strategic behavior with definitions, simultaneous and sequential games, repeated games, mixed strategies, and a Cournot bridge, using interactive tools and practice.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 13,
   "levels": [
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "game theory",
    "Nash equilibrium",
    "sequential games",
    "repeated games",
    "mixed strategies",
    "Cournot"
   ],
   "difficulty": "Challenge",
   "featured": 4,
   "content": "theory+practice",
   "builds_on": [
    "econ--cost-curves-profit-max-micro"
   ]
  },
  {
   "id": "econ--micro--exchange-economy-ge-micro",
   "path": "econ/micro/exchange-economy-ge-micro.html",
   "title": "General Equilibrium in an Exchange Economy",
   "description": "Covers general equilibrium in an exchange economy with a sandbox, Edgeworth box, Pareto efficiency, contract curve, offer curves, and competitive equilibrium derivations.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 14,
   "levels": [
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "general equilibrium",
    "Edgeworth box",
    "Pareto efficiency",
    "contract curve",
    "offer curves",
    "exchange economy"
   ],
   "difficulty": "Challenge",
   "content": "theory",
   "builds_on": [
    "econ--micro--consumer-optimum-micro"
   ]
  },
  {
   "id": "econ--micro--exchange-economy-blueprints",
   "path": "econ/micro/Exchange Economy Blueprints.html",
   "title": "Exchange Economy Blueprints: Contract Curve, Core, Equilibrium & Taxes",
   "description": "Step-by-step blueprints for two-person exchange economy problems: contract curve, core, competitive equilibrium, and lump-sum taxes for every pairing of Cobb-Douglas, quasilinear, Leontief, and linear preferences, with worked examples, try-it problems, and a drag-and-drop Spot the Plan drill.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 15,
   "levels": [
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "Edgeworth box",
    "contract curve",
    "core",
    "competitive equilibrium",
    "lump-sum taxes",
    "exchange economy"
   ],
   "difficulty": "Challenge",
   "content": "theory+practice",
   "builds_on": [
    "econ--micro--exchange-economy-ge-micro"
   ]
  },
  {
   "id": "econ--micro--competitive-equilibrium-with-production-robinson-crusoe",
   "path": "econ/micro/Competitive Equilibrium with Production - Robinson Crusoe.html",
   "title": "Competitive Equilibrium with Production: The Robinson Crusoe Economy",
   "description": "Finds competitive equilibrium with production in the Robinson Crusoe economy, covering the planner, firm and consumer choices, welfare, a sprint, and a mock test.",
   "subject": "econ",
   "topic": "Microeconomics",
   "order": 16,
   "levels": [
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "Robinson Crusoe",
    "general equilibrium",
    "production",
    "welfare",
    "planner problem",
    "competitive equilibrium"
   ],
   "difficulty": "Challenge",
   "content": "theory+practice",
   "builds_on": [
    "econ--micro--exchange-economy-ge-micro",
    "econ--cost-curves-profit-max-micro"
   ]
  },
  {
   "id": "econ--environmental-econ--evolution-of-environmental-economics",
   "path": "econ/environmental-econ/Evolution of Environmental Economics.html",
   "title": "The Evolution of Environmental Economics",
   "description": "Compares two readings on how environmental economics developed as a field, with research trends, a timeline, a connections map, quiz questions, and flashcards.",
   "subject": "econ",
   "topic": "Environmental economics",
   "order": 16,
   "levels": [
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "environmental economics",
    "research trends",
    "history of the field",
    "readings",
    "flashcards"
   ],
   "content": "theory+practice",
   "builds_on": [
    "econ--principles-of-econ--principles-of-econ-midterm-2-study-sheet"
   ]
  },
  {
   "id": "econ--environmental-econ--comparing-environmental-policies",
   "path": "econ/environmental-econ/Comparing Environmental Policies.html",
   "title": "Comparing Environmental Policies (Fullerton 2001)",
   "description": "Turns the guide questions on Fullerton's policy comparison into a practice quiz with a model figure, area quiz, flashcards, and a table reference.",
   "subject": "econ",
   "topic": "Environmental economics",
   "order": 17,
   "levels": [
    "Advanced College"
   ],
   "format": "Practice set",
   "tags": [
    "environmental policy",
    "policy instruments",
    "taxes vs permits",
    "Fullerton",
    "welfare gains",
    "quiz"
   ],
   "content": "practice",
   "builds_on": [
    "econ--environmental-econ--evolution-of-environmental-economics"
   ]
  },
  {
   "id": "econ--environmental-econ--carbon-taxes-vs-cap-and-trade",
   "path": "econ/environmental-econ/Carbon Taxes vs Cap and Trade.html",
   "title": "Carbon Taxes vs. Cap and Trade",
   "description": "Compares carbon taxes with cap and trade using a model, guide-question quiz, exam-style graph questions, an area quiz, flashcards, and a side-by-side cheat sheet.",
   "subject": "econ",
   "topic": "Environmental economics",
   "order": 18,
   "levels": [
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "carbon tax",
    "cap and trade",
    "environmental policy",
    "Coase",
    "policy instruments",
    "flashcards"
   ],
   "content": "theory+practice",
   "builds_on": [
    "econ--environmental-econ--comparing-environmental-policies"
   ]
  },
  {
   "id": "econ--environmental-econ--carbon-tax-salience-and-polluter-lists",
   "path": "econ/environmental-econ/Carbon Tax Salience and Polluter Lists.html",
   "title": "Carbon Tax Salience & Polluter Lists",
   "description": "Studies how carbon tax salience and public polluter lists change behavior, with a salience model, identification notes, results reading, a cheat sheet, and flashcards.",
   "subject": "econ",
   "topic": "Environmental economics",
   "order": 19,
   "levels": [
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "carbon tax",
    "salience",
    "polluter lists",
    "identification",
    "environmental policy",
    "flashcards"
   ],
   "difficulty": "Challenge",
   "content": "theory+practice",
   "builds_on": [
    "econ--environmental-econ--carbon-taxes-vs-cap-and-trade"
   ]
  },
  {
   "id": "econ--environmental-econ--voluntary-and-information-based-approaches",
   "path": "econ/environmental-econ/Voluntary and Information-Based Approaches.html",
   "title": "Voluntary & Information-Based Approaches",
   "description": "Covers voluntary and information-based environmental policies such as eco-labels and disclosure programs, with a model, guide-question quizzes, flashcards, and a concept map.",
   "subject": "econ",
   "topic": "Environmental economics",
   "order": 20,
   "levels": [
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "voluntary approaches",
    "eco-labels",
    "disclosure",
    "environmental policy",
    "information-based policy",
    "flashcards"
   ],
   "content": "theory+practice",
   "builds_on": [
    "econ--environmental-econ--comparing-environmental-policies"
   ]
  },
  {
   "id": "econ--environmental-econ--monitoring-and-local-conditions",
   "path": "econ/environmental-econ/Monitoring and Local Conditions.html",
   "title": "Monitoring & Local Conditions",
   "description": "Examines how monitoring and local conditions shape regulator behavior through three theories, variables and signs, table reading, results, a cheat sheet, and flashcards.",
   "subject": "econ",
   "topic": "Environmental economics",
   "order": 21,
   "levels": [
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "monitoring",
    "enforcement",
    "regulation",
    "regression tables",
    "environmental policy",
    "flashcards"
   ],
   "difficulty": "Challenge",
   "content": "theory+practice",
   "builds_on": [
    "econ--environmental-econ--voluntary-and-information-based-approaches"
   ]
  },
  {
   "id": "econ--environmental-econ--bridging-the-energy-efficiency-gap",
   "path": "econ/environmental-econ/Bridging the Energy Efficiency Gap.html",
   "title": "Bridging the Energy Efficiency Gap",
   "description": "Explains the energy efficiency gap and whether it is real, with a model, quiz questions, a policy matcher, flashcards, and a gap map.",
   "subject": "econ",
   "topic": "Environmental economics",
   "order": 22,
   "levels": [
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "energy efficiency gap",
    "behavioral economics",
    "policy design",
    "energy",
    "flashcards"
   ],
   "content": "theory+practice",
   "builds_on": [
    "econ--environmental-econ--comparing-environmental-policies"
   ]
  },
  {
   "id": "econ--environmental-econ--rebound-effect-and-efficiency-standards",
   "path": "econ/environmental-econ/Rebound Effect and Efficiency Standards.html",
   "title": "The Rebound Effect & Efficiency Standards",
   "description": "Explores why per-unit efficiency standards may not cut total energy use, covering the rebound effect with a model, quiz questions, flashcards, and a map.",
   "subject": "econ",
   "topic": "Environmental economics",
   "order": 23,
   "levels": [
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "rebound effect",
    "efficiency standards",
    "command and control",
    "energy use",
    "flashcards"
   ],
   "content": "theory+practice",
   "builds_on": [
    "econ--environmental-econ--bridging-the-energy-efficiency-gap"
   ]
  },
  {
   "id": "econ--environmental-econ--econ-4800-exam-study-sheet-environmental-policy",
   "path": "econ/environmental-econ/ECON 4800 Exam Study Sheet - Environmental Policy.html",
   "title": "Environmental Policy: Review Study Sheet",
   "description": "Review of environmental policy with a cheat sheet, flashcards, graph gallery, and study tabs on externalities, Coase, Fullerton's eight policies, and taxes versus permits.",
   "subject": "econ",
   "topic": "Environmental economics",
   "order": 24,
   "levels": [
    "Advanced College"
   ],
   "format": "Study guide",
   "tags": [
    "environmental policy",
    "externalities",
    "Coase theorem",
    "taxes vs permits",
    "graph gallery",
    "flashcards"
   ],
   "content": "theory+practice",
   "builds_on": [
    "econ--environmental-econ--carbon-taxes-vs-cap-and-trade",
    "econ--environmental-econ--voluntary-and-information-based-approaches",
    "econ--environmental-econ--bridging-the-energy-efficiency-gap"
   ]
  },
  {
   "id": "econ--public-econ--public-econ-study-sheet-public-goods-and-local-finance",
   "path": "econ/public-econ/Public Econ Study Sheet - Public Goods and Local Finance.html",
   "title": "Public Goods & Local Finance Study Sheet",
   "description": "Review of public goods and local finance with a formula cheat sheet, flashcards, worked solutions, and tabs on decentralization, tax capitalization, and welfare loss.",
   "subject": "econ",
   "topic": "Public economics",
   "order": 25,
   "levels": [
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "public goods",
    "local finance",
    "tax capitalization",
    "welfare loss",
    "decentralization",
    "formulas"
   ],
   "content": "theory+practice",
   "builds_on": [
    "econ--principles-of-econ--principles-of-econ-midterm-2-study-sheet"
   ]
  },
  {
   "id": "econ--econometrics--econometrics-cheat-sheet",
   "path": "econ/econometrics/econometrics_cheat_sheet.html",
   "title": "Econometrics Master Cheat Sheet",
   "description": "Reviews OLS theory with an interactive regression line, slope and intercept sliders showing squared residuals, plus two cheat sheets of key econometrics results.",
   "subject": "econ",
   "topic": "Econometrics",
   "order": 26,
   "levels": [
    "Advanced College"
   ],
   "format": "Cheat sheet",
   "tags": [
    "econometrics",
    "OLS",
    "regression",
    "residuals",
    "cheat sheet"
   ],
   "content": "reference",
   "builds_on": [
    "stats--variance-standard-deviation-standard-error-organizer",
    "calculus--differentiation-part-1"
   ]
  },
  {
   "id": "psychology--observational-research-lecture2-study-sheet",
   "path": "psychology/Observational_Research_Lecture2_Study_Sheet.html",
   "title": "Observational Research: Types, Ethics & Data Quality",
   "description": "Review observational research with a one-page cheat sheet covering types, ethics, sampling, recording, and classic studies, plus practice questions and flashcards.",
   "subject": "psychology",
   "topic": "Research methods",
   "order": 1,
   "levels": [
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "observational research",
    "research methods",
    "research ethics",
    "sampling",
    "psychology"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "machine-learning--stats-for-ml-cheat-sheet",
   "path": "machine-learning/Stats-for-ML-Cheat-Sheet.html",
   "title": "Statistics for ML: Formula Cheat Sheet",
   "description": "Quick reference for the probability, expectation, distribution, maximum likelihood, entropy, and calculus results machine learning students should know, with interactive visuals.",
   "subject": "machine-learning",
   "topic": "Math & stats foundations",
   "order": 1,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Cheat sheet",
   "tags": [
    "probability",
    "expectation & variance",
    "mle",
    "entropy",
    "machine learning",
    "statistics"
   ],
   "content": "reference",
   "builds_on": [
    "stats--variance-standard-deviation-standard-error-organizer"
   ]
  },
  {
   "id": "machine-learning--matrix-calculus-worksheet",
   "path": "machine-learning/matrix-calculus-worksheet.html",
   "title": "Matrix Calculus: Gradients & Shapes",
   "description": "Work through matrix gradients and shape bookkeeping using one fixed running example, with visualizers, derivations, rule tables, and practice problems.",
   "subject": "machine-learning",
   "topic": "Math & stats foundations",
   "order": 2,
   "levels": [
    "Advanced College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "matrix calculus",
    "gradients",
    "jacobian",
    "tensor shapes",
    "machine learning"
   ],
   "content": "theory+practice",
   "builds_on": [
    "calculus--differentiation-part-2",
    "calculus--directional-derivative-worksheet"
   ]
  },
  {
   "id": "machine-learning--decision-tree-step-through",
   "path": "machine-learning/Decision_Tree_Step_Through.html",
   "title": "Growing a Decision Tree",
   "description": "Step through how a decision tree picks splits, experiment in a split lab, follow the proof that splits never hurt, and practice.",
   "subject": "machine-learning",
   "topic": "Algorithms, step by step",
   "order": 3,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Step-through",
   "tags": [
    "decision trees",
    "splitting",
    "classification",
    "impurity",
    "machine learning"
   ],
   "content": "theory+practice",
   "builds_on": [
    "machine-learning--stats-for-ml-cheat-sheet"
   ]
  },
  {
   "id": "machine-learning--neural-network-step-through",
   "path": "machine-learning/Neural_Network_Step_Through.html",
   "title": "Inside a Simple Neural Network",
   "description": "Step through a forward pass in a small sigmoid network, explore its geometry, see how training works, and practice with problems.",
   "subject": "machine-learning",
   "topic": "Algorithms, step by step",
   "order": 4,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Step-through",
   "tags": [
    "neural networks",
    "forward pass",
    "sigmoid",
    "backpropagation",
    "machine learning"
   ],
   "content": "theory+practice",
   "builds_on": [
    "machine-learning--matrix-calculus-worksheet",
    "calculus--projection-to-gradient-descent-conceptual-map"
   ]
  },
  {
   "id": "machine-learning--kmeans-image-compression-worksheet",
   "path": "machine-learning/kmeans_image_compression_worksheet.html",
   "title": "K-Means Image Compression",
   "description": "Treat a photo as data, watch k-means cluster its colors live, compress the image, and check your understanding of the theory.",
   "subject": "machine-learning",
   "topic": "Algorithms, step by step",
   "order": 5,
   "levels": [
    "College"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "k-means",
    "clustering",
    "image compression",
    "color space",
    "machine learning"
   ],
   "featured": 5,
   "content": "theory+practice",
   "builds_on": [
    "machine-learning--stats-for-ml-cheat-sheet"
   ]
  },
  {
   "id": "machine-learning--semi-supervised-em-step-through",
   "path": "machine-learning/semi_supervised_em_step_through.html",
   "title": "Semi-Supervised EM & Gaussian Mixtures",
   "description": "Watch the EM algorithm run live on labeled and unlabeled data, compare the objectives, study the theory, and test yourself.",
   "subject": "machine-learning",
   "topic": "Algorithms, step by step",
   "order": 6,
   "levels": [
    "Advanced College"
   ],
   "format": "Step-through",
   "tags": [
    "em algorithm",
    "gaussian mixtures",
    "semi-supervised learning",
    "unlabeled data",
    "machine learning"
   ],
   "content": "theory+practice",
   "builds_on": [
    "machine-learning--stats-for-ml-cheat-sheet",
    "machine-learning--kmeans-image-compression-worksheet"
   ]
  },
  {
   "id": "machine-learning--ml-study-guide",
   "path": "machine-learning/ml_study_guide.html",
   "title": "ML Study Guide",
   "description": "Nine-part review of machine learning math, from linear algebra and matrix calculus to regression, GLMs, bias and variance, trees, EM, kernels, and PCA.",
   "subject": "machine-learning",
   "topic": "Review",
   "order": 7,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Study guide",
   "tags": [
    "linear algebra",
    "regression",
    "glms",
    "bias-variance",
    "pca",
    "machine learning"
   ],
   "content": "theory",
   "builds_on": [
    "machine-learning--matrix-calculus-worksheet",
    "machine-learning--stats-for-ml-cheat-sheet"
   ]
  },
  {
   "id": "machine-learning--matrix-calculus-linear-algebra-toolkit",
   "path": "machine-learning/matrix-calculus-linear-algebra-toolkit.html",
   "title": "Matrix Calculus & Linear Algebra Toolkit",
   "description": "Scalar rules translated to matrix form, the chain rule with the right order and transposes, norms and the spectral norm with an interactive budget picture and power iteration, and Jacobians with a grid-warp explorer.",
   "subject": "machine-learning",
   "topic": "Math & stats foundations",
   "order": 8,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "matrix calculus",
    "chain rule",
    "spectral norm",
    "eigenvectors",
    "jacobian",
    "power iteration",
    "machine learning"
   ],
   "content": "theory+practice",
   "builds_on": [
    "machine-learning--matrix-calculus-worksheet",
    "calculus--differentiation-part-2"
   ]
  },
  {
   "id": "machine-learning--deep-learning-exam-review",
   "path": "machine-learning/deep-learning-exam-review.html",
   "title": "Deep Learning Exam Review",
   "description": "Cheat sheet, flashcards, and worked derivations for a deep learning exam: gradient descent variants, batch norm, L1 and L2, backprop Jacobians, vanishing gradients and residual blocks, CNN shapes and parameter counts, LoRA, reading loss curves, and hand-built networks, plus a 20-question quiz.",
   "subject": "machine-learning",
   "topic": "Review",
   "order": 9,
   "levels": [
    "College",
    "Advanced College"
   ],
   "format": "Study sheet",
   "tags": [
    "deep learning",
    "backpropagation",
    "batch normalization",
    "residual connections",
    "convolutional networks",
    "regularization",
    "lora",
    "machine learning"
   ],
   "content": "theory+practice",
   "builds_on": [
    "machine-learning--matrix-calculus-linear-algebra-toolkit",
    "machine-learning--neural-network-step-through",
    "machine-learning--ml-study-guide"
   ]
  },
  {
   "id": "medical-study-sheets--hematology--inherited-thrombophilias-ashsap-ch19-study-sheet",
   "path": "medical study sheets/hematology/Inherited_Thrombophilias_ASHSAP_Ch19_Study_Sheet.html",
   "title": "Inherited Thrombophilias: Mechanisms, Assays & Testing",
   "description": "Covers the five inherited thrombophilias, their mechanisms, assay pitfalls, and 2023 ASH testing recommendations, with a cheat sheet, practice questions, and flashcards.",
   "subject": "medicine",
   "topic": "Hematology",
   "order": 1,
   "levels": [
    "Graduate"
   ],
   "format": "Study sheet",
   "tags": [
    "thrombophilia",
    "hematology",
    "factor v leiden",
    "coagulation assays",
    "venous thromboembolism"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "test-prep--sat-psat-diagnostic",
   "path": "test-prep/SAT-PSAT-Diagnostic.html",
   "title": "PSAT / SAT Diagnostic",
   "description": "Untimed diagnostic covering SAT Reading & Writing and Math, with a built-in timer and Desmos, to show which skills to review next.",
   "subject": "sat",
   "topic": "Start here",
   "order": 1,
   "levels": [
    "High School"
   ],
   "format": "Diagnostic",
   "tags": [
    "SAT",
    "PSAT",
    "diagnostic",
    "reading & writing",
    "math",
    "skills assessment"
   ],
   "exams": [
    "SAT",
    "PSAT"
   ],
   "content": "practice",
   "builds_on": []
  },
  {
   "id": "test-prep--test-day-playbook-sat-psat-act",
   "path": "test-prep/Test-Day-Playbook-SAT-PSAT-ACT.html",
   "title": "Test Day Playbook: SAT, PSAT & ACT",
   "description": "Interactive guide to test-day strategy for the SAT, PSAT, and ACT using the CLEAR method, with a true or false warm up and flashcards.",
   "subject": "sat",
   "topic": "Start here",
   "order": 2,
   "levels": [
    "High School"
   ],
   "format": "Playbook",
   "tags": [
    "SAT",
    "PSAT",
    "ACT",
    "test-taking strategy",
    "pacing",
    "test day"
   ],
   "exams": [
    "SAT",
    "PSAT",
    "ACT"
   ],
   "content": "theory",
   "builds_on": []
  },
  {
   "id": "test-prep--sat--sat-reading-1-student-notes",
   "path": "test-prep/sat/SAT-Reading-1-Student-Notes.html",
   "title": "SAT Reading 1: Student Notes (SCORE)",
   "description": "Teaches the SCORE method for Student Notes questions on SAT Reading & Writing, with a game plan, timed sprint, practice section, and answers.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 4,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "SAT",
    "reading & writing",
    "student notes",
    "SCORE",
    "test strategy"
   ],
   "difficulty": "Core",
   "exams": [
    "SAT"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "test-prep--sat--sat-grammar-1-transitions",
   "path": "test-prep/sat/SAT-Grammar-1-Transitions.html",
   "title": "SAT Grammar 1: Transitions (LINK)",
   "description": "Teaches the LINK method for transition questions on SAT Reading & Writing, with a game plan, practice section, flashcards, and strategy tips.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 5,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "SAT",
    "grammar",
    "transitions",
    "LINK",
    "reading & writing"
   ],
   "difficulty": "Core",
   "exams": [
    "SAT"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "test-prep--sat--sat-grammar-2-sentence-boundaries",
   "path": "test-prep/sat/SAT-Grammar-2-Sentence-Boundaries.html",
   "title": "SAT Grammar 2: Sentence Boundaries",
   "description": "Teaches how to choose the right punctuation between sentence parts on the SAT, with fragment checks, eliminating twins, three boundary patterns, and practice.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 6,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "SAT",
    "grammar",
    "sentence boundaries",
    "punctuation",
    "fragments",
    "run-ons"
   ],
   "difficulty": "Core",
   "exams": [
    "SAT"
   ],
   "content": "theory+practice",
   "builds_on": [
    "test-prep--sat--sat-grammar-1-transitions"
   ]
  },
  {
   "id": "test-prep--sat--sat-words-in-context-1-words-1-40",
   "path": "test-prep/sat/SAT-Words-in-Context-1-Words-1-40.html",
   "title": "SAT Words in Context: Set 1 (Words 1–40)",
   "description": "Forty SAT vocabulary words with flashcards you can hide to quiz yourself, strategy tips, and 40 practice questions that test each word in context.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 7,
   "levels": [
    "High School"
   ],
   "format": "Practice set",
   "tags": [
    "SAT",
    "vocabulary",
    "words in context",
    "flashcards",
    "reading & writing"
   ],
   "exams": [
    "SAT"
   ],
   "content": "practice",
   "builds_on": []
  },
  {
   "id": "test-prep--sat--sat-words-in-context-2-words-41-80",
   "path": "test-prep/sat/SAT-Words-in-Context-2-Words-41-80.html",
   "title": "SAT Words in Context: Set 2 (Words 41–80)",
   "description": "Forty more SAT vocabulary words with hideable flashcards for self-quizzing, strategy tips, and 40 practice questions that test each word in context.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 8,
   "levels": [
    "High School"
   ],
   "format": "Practice set",
   "tags": [
    "SAT",
    "vocabulary",
    "words in context",
    "flashcards",
    "reading & writing"
   ],
   "exams": [
    "SAT"
   ],
   "content": "practice",
   "builds_on": [
    "test-prep--sat--sat-words-in-context-1-words-1-40"
   ]
  },
  {
   "id": "test-prep--sat--sat-words-in-context-3-words-81-120",
   "path": "test-prep/sat/SAT-Words-in-Context-3-Words-81-120.html",
   "title": "SAT Words in Context: Set 3 (Words 81–120)",
   "description": "Another forty SAT vocabulary words with hideable flashcards for self-quizzing, strategy tips, and 40 practice questions that test each word in context.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 9,
   "levels": [
    "High School"
   ],
   "format": "Practice set",
   "tags": [
    "SAT",
    "vocabulary",
    "words in context",
    "flashcards",
    "reading & writing"
   ],
   "exams": [
    "SAT"
   ],
   "content": "practice",
   "builds_on": [
    "test-prep--sat--sat-words-in-context-2-words-41-80"
   ]
  },
  {
   "id": "test-prep--sat--sat-desmos-strategies",
   "path": "test-prep/sat/SAT-Desmos-Strategies.html",
   "title": "SAT Math: Desmos Strategies",
   "description": "Shows how to use Desmos on every digital SAT Math question, with calculator basics, thirteen techniques, answer formatting tips, a formula list, practice, and a timed 15-question SAT Gauntlet.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 10,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "SAT",
    "math",
    "Desmos",
    "calculator",
    "graphing",
    "answer formatting"
   ],
   "difficulty": "Core",
   "exams": [
    "SAT"
   ],
   "featured": 1,
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "test-prep--sat--sat-math-1-linear-equations",
   "path": "test-prep/sat/SAT-Math-1-Linear-Equations.html",
   "title": "SAT Math 1: Linear Equations",
   "description": "Reviews slope, intercepts, linear forms, and systems on the SAT, with worked examples, fluency drills, a gauntlet, challenge questions, and an exit ticket.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 11,
   "levels": [
    "High School"
   ],
   "format": "Practice set",
   "tags": [
    "SAT",
    "math",
    "linear equations",
    "slope",
    "systems of equations",
    "Desmos"
   ],
   "difficulty": "Core",
   "exams": [
    "SAT"
   ],
   "content": "practice",
   "builds_on": [
    "test-prep--sat--sat-desmos-strategies"
   ]
  },
  {
   "id": "test-prep--sat--sat-math-2-quadratics",
   "path": "test-prep/sat/SAT-Math-2-Quadratics.html",
   "title": "SAT Math 2: Quadratics",
   "description": "Reviews the three forms of a parabola, factoring, the vertex, the discriminant, and line-parabola systems on the SAT, with worked examples, fluency drills, an SAT-style practice set, challenge questions, and an exit ticket.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 12,
   "levels": [
    "High School"
   ],
   "format": "Practice set",
   "tags": [
    "SAT",
    "math",
    "quadratics",
    "factoring",
    "discriminant",
    "parabola",
    "vertex",
    "systems of equations",
    "Desmos"
   ],
   "difficulty": "Core",
   "exams": [
    "SAT"
   ],
   "content": "practice",
   "builds_on": [
    "test-prep--sat--sat-math-1-linear-equations",
    "algebra--factoring-worksheet"
   ]
  },
  {
   "id": "test-prep--sat--practice-sat-full-test",
   "path": "test-prep/sat/Practice-SAT-Full-Test.html",
   "title": "Full-Length Practice SAT",
   "description": "Full-length digital SAT practice test with two Reading & Writing modules and two Math modules, built-in Desmos, and an option to export all sections.",
   "subject": "sat",
   "topic": "Reading, writing & math",
   "order": 13,
   "levels": [
    "High School"
   ],
   "format": "Practice test",
   "tags": [
    "SAT",
    "full-length test",
    "reading & writing",
    "math",
    "Desmos",
    "practice test"
   ],
   "exams": [
    "SAT"
   ],
   "content": "practice",
   "builds_on": [
    "test-prep--sat-psat-diagnostic"
   ]
  },
  {
   "id": "test-prep--sat--test-day-playbook-sat-psat",
   "path": "test-prep/sat/Test-Day-Playbook-SAT-PSAT.html",
   "title": "Test Day Playbook: SAT & PSAT",
   "description": "Interactive guide to test-day strategy for the SAT and PSAT using the CLEAR method, with a warm up, timers, flashcards, and Bluebook practice.",
   "subject": "sat",
   "topic": "Start here",
   "order": 3,
   "levels": [
    "High School"
   ],
   "format": "Playbook",
   "tags": [
    "SAT",
    "PSAT",
    "test-taking strategy",
    "pacing",
    "Bluebook",
    "test day"
   ],
   "exams": [
    "SAT",
    "PSAT"
   ],
   "content": "theory",
   "builds_on": [
    "test-prep--sat--practice-sat-full-test"
   ]
  },
  {
   "id": "test-prep--act--act-grammar-1-transitions",
   "path": "test-prep/act/ACT-Grammar-1-Transitions.html",
   "title": "ACT Grammar 1: Transitions (LINK)",
   "description": "Teaches the LINK method for transition questions in ACT English, with a game plan, practice section, flashcards, and strategy tips.",
   "subject": "act",
   "topic": "Grammar, math & science",
   "order": 1,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "ACT",
    "English",
    "grammar",
    "transitions",
    "LINK"
   ],
   "difficulty": "Core",
   "exams": [
    "ACT"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "test-prep--act--act-grammar-2-sentence-boundaries",
   "path": "test-prep/act/ACT-Grammar-2-Sentence-Boundaries.html",
   "title": "ACT Grammar 2: Sentence Boundaries",
   "description": "Teaches how to choose the right punctuation between sentence parts on the ACT, with fragment checks, eliminating twins, three boundary patterns, and practice.",
   "subject": "act",
   "topic": "Grammar, math & science",
   "order": 2,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "ACT",
    "English",
    "grammar",
    "sentence boundaries",
    "punctuation",
    "fragments"
   ],
   "difficulty": "Core",
   "exams": [
    "ACT"
   ],
   "content": "theory+practice",
   "builds_on": [
    "test-prep--act--act-grammar-1-transitions"
   ]
  },
  {
   "id": "test-prep--act--act-geometry-review",
   "path": "test-prep/act/ACT-Geometry-Review.html",
   "title": "ACT Math: Geometry Review",
   "description": "Reviews ACT geometry formulas for angles, triangles, polygons, circles, coordinate geometry, and trigonometry, with interactive diagrams and a mixed review.",
   "subject": "act",
   "topic": "Grammar, math & science",
   "order": 3,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "ACT",
    "math",
    "geometry",
    "circles",
    "triangles",
    "trigonometry"
   ],
   "difficulty": "Core",
   "exams": [
    "ACT"
   ],
   "content": "theory",
   "builds_on": []
  },
  {
   "id": "test-prep--act--act-stats-probability-review",
   "path": "test-prep/act/ACT-Stats-Probability-Review.html",
   "title": "ACT Math: Statistics & Probability Review",
   "description": "Reviews ACT formulas and concepts for data and graphs, center and spread, distributions, probability, and counting, with sliders and a mixed review.",
   "subject": "act",
   "topic": "Grammar, math & science",
   "order": 4,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "ACT",
    "math",
    "statistics",
    "probability",
    "distributions",
    "counting"
   ],
   "difficulty": "Core",
   "exams": [
    "ACT"
   ],
   "content": "theory",
   "builds_on": []
  },
  {
   "id": "test-prep--act--act-science-1-chart-core-data-skills",
   "path": "test-prep/act/ACT-Science-1-CHART-Core-Data-Skills.html",
   "title": "ACT Science 1: Core Data Skills (CHART)",
   "description": "Teaches the CHART method for reading ACT Science passages, graphs, and tables, with a game plan, strategy tips, a timed practice section, and scoring.",
   "subject": "act",
   "topic": "Grammar, math & science",
   "order": 5,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "ACT",
    "science",
    "data interpretation",
    "graphs",
    "CHART",
    "test strategy"
   ],
   "difficulty": "Core",
   "exams": [
    "ACT"
   ],
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "test-prep--act--act-science-2-impact-advanced-question-types",
   "path": "test-prep/act/ACT-Science-2-IMPACT-Advanced-Question-Types.html",
   "title": "ACT Science 2: Advanced Question Types (IMPACT)",
   "description": "Covers harder ACT Science question types with the IMPACT method, including missing data, inference, counting, plugging in, and averages, plus timed practice and scoring.",
   "subject": "act",
   "topic": "Grammar, math & science",
   "order": 6,
   "levels": [
    "High School"
   ],
   "format": "Interactive worksheet",
   "tags": [
    "ACT",
    "science",
    "question types",
    "IMPACT",
    "data interpretation",
    "test strategy"
   ],
   "difficulty": "Challenge",
   "exams": [
    "ACT"
   ],
   "content": "theory+practice",
   "builds_on": [
    "test-prep--act--act-science-1-chart-core-data-skills"
   ]
  },
  {
   "id": "test-prep--sat-tutor-evaluation",
   "path": "test-prep/SAT-Tutor-Evaluation.html",
   "title": "Tutor Skills Evaluation",
   "description": "Timed tutor evaluation covering SAT Reading & Writing and Math, with Desmos, used to assess a tutor's skills in a single sitting.",
   "subject": "sat",
   "topic": "For tutors",
   "order": 14,
   "levels": [
    "High School"
   ],
   "format": "Evaluation",
   "tags": [
    "SAT",
    "tutor evaluation",
    "reading & writing",
    "math",
    "tutoring"
   ],
   "exams": [
    "SAT"
   ],
   "content": "practice",
   "builds_on": []
  },
  {
   "id": "gre--gre-quant-formula-cards",
   "path": "gre/gre-quant-formula-cards.html",
   "title": "GRE Quant: Formula Sheet & Flash Cards",
   "description": "Memorize the 50 core GRE Quant formulas with a short list, a full formula reference, flash cards, and a review pile.",
   "subject": "gre",
   "topic": "Quant: reference",
   "order": 1,
   "levels": [
    "College"
   ],
   "format": "Cheat sheet",
   "tags": [
    "gre quant",
    "formulas",
    "flashcards",
    "arithmetic",
    "algebra",
    "geometry"
   ],
   "exams": [
    "GRE"
   ],
   "content": "reference",
   "builds_on": []
  },
  {
   "id": "gre--gre-exponents-sheet",
   "path": "gre/gre-exponents-sheet.html",
   "title": "GRE Quant: Simplifying Exponents",
   "description": "Learn the exponent rules with two worked examples each, then build fluency with timed drills, GRE-style questions, challenge problems, and an exit ticket.",
   "subject": "gre",
   "topic": "Quant: topic sheets",
   "order": 2,
   "levels": [
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "gre quant",
    "exponents",
    "powers",
    "algebra rules",
    "drills"
   ],
   "exams": [
    "GRE"
   ],
   "content": "theory+practice",
   "builds_on": [
    "gre--gre-quant-formula-cards"
   ]
  },
  {
   "id": "gre--gre-sequences-sheet",
   "path": "gre/gre-sequences-sheet.html",
   "title": "GRE Quant: Sequences",
   "description": "Translate between sequence rules and terms using worked examples, then practice with fluency drills, GRE-style questions, challenge problems, and an exit ticket.",
   "subject": "gre",
   "topic": "Quant: topic sheets",
   "order": 3,
   "levels": [
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "gre quant",
    "sequences",
    "arithmetic sequences",
    "geometric sequences",
    "drills"
   ],
   "exams": [
    "GRE"
   ],
   "content": "theory+practice",
   "builds_on": [
    "gre--gre-quant-formula-cards"
   ]
  },
  {
   "id": "gre--gre-interest-sheet",
   "path": "gre/gre-interest-sheet.html",
   "title": "GRE Quant: Interest & Percent Change",
   "description": "Treat interest problems as percent change, with worked examples, fluency drills, GRE-style questions, challenge problems, and an exit ticket.",
   "subject": "gre",
   "topic": "Quant: topic sheets",
   "order": 4,
   "levels": [
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "gre quant",
    "interest",
    "percent change",
    "compound interest",
    "drills"
   ],
   "exams": [
    "GRE"
   ],
   "content": "theory+practice",
   "builds_on": [
    "gre--gre-quant-formula-cards"
   ]
  },
  {
   "id": "gre--gre-circles-sheet",
   "path": "gre/gre-circles-sheet.html",
   "title": "GRE Quant: Circles",
   "description": "Learn the circle rules for radius, diameter, and central angles with worked examples, then practice using drills, GRE-style questions, and challenges.",
   "subject": "gre",
   "topic": "Quant: topic sheets",
   "order": 5,
   "levels": [
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "gre quant",
    "circles",
    "arc and sector",
    "geometry",
    "drills"
   ],
   "exams": [
    "GRE"
   ],
   "content": "theory+practice",
   "builds_on": [
    "gre--gre-quant-formula-cards"
   ]
  },
  {
   "id": "gre--gre-triangles-sheet",
   "path": "gre/gre-triangles-sheet.html",
   "title": "GRE Quant: Triangles",
   "description": "Master eight triangle rules with worked examples, then practice using fluency drills, GRE-style questions, challenge problems, and an exit ticket.",
   "subject": "gre",
   "topic": "Quant: topic sheets",
   "order": 6,
   "levels": [
    "College"
   ],
   "format": "Study sheet",
   "tags": [
    "gre quant",
    "triangles",
    "pythagorean theorem",
    "geometry",
    "drills"
   ],
   "exams": [
    "GRE"
   ],
   "content": "theory+practice",
   "builds_on": [
    "gre--gre-quant-formula-cards",
    "gre--gre-circles-sheet"
   ]
  },
  {
   "id": "gre--gre-essay-sheet",
   "path": "gre/GRE-Essay-Sheet.html",
   "title": "GRE Essay: The Issue Essay Roadmap",
   "description": "Learn what separates each Issue essay score, then use the architecture, prompt types, example and prompt banks, model essays, and drills to improve.",
   "subject": "gre",
   "topic": "Writing & full practice",
   "order": 7,
   "levels": [
    "College"
   ],
   "format": "Study guide",
   "tags": [
    "gre writing",
    "issue essay",
    "essay structure",
    "prompt bank",
    "model essays"
   ],
   "exams": [
    "GRE"
   ],
   "featured": 6,
   "content": "theory+practice",
   "builds_on": []
  },
  {
   "id": "gre--gre-practice-test-full",
   "path": "gre/GRE_Practice_Test_Full.html",
   "title": "Full-Length GRE Practice Test",
   "description": "Take a timed 54-question practice test covering Quantitative and Verbal Reasoning, then review your results.",
   "subject": "gre",
   "topic": "Writing & full practice",
   "order": 8,
   "levels": [
    "College"
   ],
   "format": "Practice test",
   "tags": [
    "gre",
    "practice test",
    "quantitative reasoning",
    "verbal reasoning",
    "timed"
   ],
   "exams": [
    "GRE"
   ],
   "content": "practice",
   "builds_on": [
    "gre--gre-exponents-sheet",
    "gre--gre-triangles-sheet",
    "gre--gre-interest-sheet"
   ]
  }
 ],
 "content_types": [
  {
   "key": "theory",
   "label": "Theory",
   "blurb": "Explains the ideas; little or no practice"
  },
  {
   "key": "theory+practice",
   "label": "Theory + practice",
   "blurb": "Explains, then drills with checking"
  },
  {
   "key": "practice",
   "label": "Practice",
   "blurb": "Problems, tests, or diagnostics only"
  },
  {
   "key": "reference",
   "label": "Reference",
   "blurb": "Formulas, comparisons, cheat sheets"
  }
 ]
};
