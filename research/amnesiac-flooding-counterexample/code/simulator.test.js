"use strict";

const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const test = require("node:test");
const {
  alternateFixture,
  figure6Calibration,
  fixtures,
  primaryFixture,
} = require("./fixtures");
const { simulate, stateKey } = require("./simulator");
const {
  validateFixture,
  verifyCalibrationFixture,
  verifyFixture,
} = require("./verifier");

test("source sends in round 1 and weight determines the delivery round", () => {
  const graph = {
    vertices: ["x", "y", "z"],
    edges: [
      { u: "x", v: "y", weight: 1 },
      { u: "x", v: "z", weight: 3 },
    ],
  };

  const states = simulate(graph, ["x"], 3).map(stateKey);
  assert.deepEqual(states, [
    "D[x>y] F[x>z@2]",
    "D[] F[x>z@1]",
    "D[x>z] F[]",
  ]);
});

test("primary witness has the required graph properties and exact table", () => {
  assert.deepEqual(validateFixture(primaryFixture), {
    connected: true,
    bipartite: true,
    delayedEdge: { u: "a", v: "b", weight: 2 },
    sourceCount: 2,
  });
  assert.deepEqual(
    simulate(
      primaryFixture.graph,
      primaryFixture.sources,
      primaryFixture.expectedStates.length,
    ).map(stateKey),
    primaryFixture.expectedStates,
  );
  assert.deepEqual(verifyFixture(primaryFixture).repeat, {
    firstRound: 5,
    secondRound: 10,
    period: 5,
  });
});

test("alternate numeric witness has the exact table and S4 = S9", () => {
  assert.deepEqual(
    simulate(
      alternateFixture.graph,
      alternateFixture.sources,
      alternateFixture.expectedStates.length,
    ).map(stateKey),
    alternateFixture.expectedStates,
  );
  const certificate = verifyFixture(alternateFixture);
  assert.equal(certificate.state, "D[1>2,2>1] F[]");
  assert.deepEqual(certificate.repeat, {
    firstRound: 4,
    secondRound: 9,
    period: 5,
  });
});

test("paper Figure 6 calibrates the simulator with nonempty S5 = S13", () => {
  const states = simulate(
    figure6Calibration.graph,
    figure6Calibration.sources,
    13,
  ).map(stateKey);

  assert.equal(states[4], "D[3>1,3>2,3>5] F[]");
  assert.notEqual(states[4], "D[] F[]");
  assert.equal(states[4], states[12]);

  assert.deepEqual(verifyCalibrationFixture(figure6Calibration), {
    name: "paper-figure-6-calibration",
    calibrationOnly: true,
    delayedEdgeCount: 2,
    sourceCount: 1,
    repeat: { firstRound: 5, secondRound: 13, period: 8 },
    state: "D[3>1,3>2,3>5] F[]",
  });
  assert.throws(
    () => validateFixture(figure6Calibration),
    /exactly two sources/,
  );
});

test("all shipped fixtures verify", () => {
  assert.equal(fixtures.map(verifyFixture).length, fixtures.length);
});

test("CLI exits nonzero when an expected round is corrupted", () => {
  const script = [
    'const fixture = structuredClone(require("./fixtures").primaryFixture);',
    'fixture.expectedStates[0] = "corrupted";',
    'require("./cli").runCli([fixture]);',
  ].join("");
  const result = spawnSync(process.execPath, ["-e", script], {
    cwd: __dirname,
    encoding: "utf8",
  });

  assert.equal(result.status, 1);
  assert.match(result.stderr, /^FAIL .*exact round table mismatch/m);
});

test("fixture validation rejects each required-property violation", () => {
  const clone = () => structuredClone(primaryFixture);

  const disconnected = clone();
  disconnected.graph.edges = disconnected.graph.edges.filter(
    ({ u, v }) => u !== "e" && v !== "e",
  );
  assert.throws(() => validateFixture(disconnected), /connected/);

  const nonBipartite = clone();
  nonBipartite.graph.edges.push({ u: "a", v: "c", weight: 1 });
  assert.throws(() => validateFixture(nonBipartite), /bipartite/);

  const twoDelayedEdges = clone();
  twoDelayedEdges.graph.edges.find(
    ({ u, v }) => u === "b" && v === "c",
  ).weight = 2;
  assert.throws(() => validateFixture(twoDelayedEdges), /one delayed/);

  const oneSource = clone();
  oneSource.sources = ["c"];
  assert.throws(() => validateFixture(oneSource), /two sources/);
});
