"use strict";

const assert = require("node:assert/strict");
const { buildAdjacency, simulate, stateKey } = require("./simulator");

function validateFixture(fixture) {
  const adjacency = buildAdjacency(fixture.graph);
  assert.equal(fixture.sources.length, 2, "fixture must have exactly two sources");
  assert.equal(
    new Set(fixture.sources).size,
    2,
    "fixture sources must be distinct",
  );
  for (const source of fixture.sources) {
    assert(adjacency.has(source), `fixture source ${source} must be a vertex`);
  }

  const delayedEdges = fixture.graph.edges.filter(({ weight }) => weight > 1);
  assert.equal(
    delayedEdges.length,
    1,
    "fixture must have exactly one delayed bidirectional edge",
  );

  const firstVertex = fixture.graph.vertices[0];
  const visited = new Set([firstVertex]);
  const queue = [firstVertex];
  while (queue.length > 0) {
    const vertex = queue.shift();
    for (const { vertex: neighbor } of adjacency.get(vertex)) {
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
      }
    }
  }
  assert.equal(
    visited.size,
    fixture.graph.vertices.length,
    "fixture graph must be connected",
  );

  const colors = new Map();
  for (const start of fixture.graph.vertices) {
    if (colors.has(start)) {
      continue;
    }
    colors.set(start, 0);
    const colorQueue = [start];
    while (colorQueue.length > 0) {
      const vertex = colorQueue.shift();
      for (const { vertex: neighbor } of adjacency.get(vertex)) {
        if (!colors.has(neighbor)) {
          colors.set(neighbor, 1 - colors.get(vertex));
          colorQueue.push(neighbor);
        } else {
          assert.notEqual(
            colors.get(neighbor),
            colors.get(vertex),
            "fixture graph must be bipartite",
          );
        }
      }
    }
  }

  return {
    connected: true,
    bipartite: true,
    delayedEdge: delayedEdges[0],
    sourceCount: fixture.sources.length,
  };
}

function verifyFixture(fixture) {
  const properties = validateFixture(fixture);
  const { firstRound, secondRound, period } = fixture.repeat;
  assert.equal(
    secondRound - firstRound,
    period,
    "declared repeat rounds must differ by the declared period",
  );
  assert(
    fixture.expectedStates.length >= secondRound,
    "expected round table must include the repeated state",
  );

  const states = simulate(
    fixture.graph,
    fixture.sources,
    fixture.expectedStates.length,
  );
  const actualTable = states.map(stateKey);
  assert.deepEqual(
    actualTable,
    fixture.expectedStates,
    `${fixture.name}: exact round table mismatch`,
  );
  assert.equal(
    actualTable[firstRound - 1],
    actualTable[secondRound - 1],
    `${fixture.name}: S${firstRound} must equal S${secondRound}`,
  );

  const cycleStates = actualTable.slice(firstRound - 1, secondRound - 1);
  assert.equal(
    new Set(cycleStates).size,
    period,
    `${fixture.name}: claimed period must be minimal within the witnessed cycle`,
  );

  const continuation = simulate(
    fixture.graph,
    fixture.sources,
    secondRound + period,
  ).map(stateKey);
  for (let round = firstRound; round <= secondRound; round += 1) {
    assert.equal(
      continuation[round - 1],
      continuation[round + period - 1],
      `${fixture.name}: period does not continue from S${round}`,
    );
  }

  return {
    name: fixture.name,
    properties,
    roundCount: states.length,
    repeat: fixture.repeat,
    state: actualTable[firstRound - 1],
  };
}

function verifyCalibrationFixture(fixture) {
  const adjacency = buildAdjacency(fixture.graph);
  assert.equal(
    fixture.sources.length,
    1,
    `${fixture.name}: calibration must have one source`,
  );
  assert(adjacency.has(fixture.sources[0]), "calibration source must be a vertex");
  assert.equal(
    fixture.graph.edges.filter(({ weight }) => weight > 1).length,
    2,
    `${fixture.name}: calibration must have two delayed edges`,
  );

  const { firstRound, secondRound, period } = fixture.repeat;
  assert.equal(
    secondRound - firstRound,
    period,
    "calibration repeat rounds must differ by the declared period",
  );

  const stateKeys = simulate(
    fixture.graph,
    fixture.sources,
    secondRound + period,
  ).map(stateKey);
  const firstState = stateKeys[firstRound - 1];
  assert.notEqual(firstState, "D[] F[]", `${fixture.name}: repeated state is empty`);
  assert.equal(
    firstState,
    fixture.expectedRepeatedState,
    `${fixture.name}: calibrated S${firstRound} mismatch`,
  );
  assert.equal(
    firstState,
    stateKeys[secondRound - 1],
    `${fixture.name}: S${firstRound} must equal S${secondRound}`,
  );

  const cycleStates = stateKeys.slice(firstRound - 1, secondRound - 1);
  assert.equal(
    new Set(cycleStates).size,
    period,
    `${fixture.name}: claimed period must be minimal within the witnessed cycle`,
  );
  for (let round = firstRound; round <= secondRound; round += 1) {
    assert.equal(
      stateKeys[round - 1],
      stateKeys[round + period - 1],
      `${fixture.name}: period does not continue from S${round}`,
    );
  }

  return {
    name: fixture.name,
    calibrationOnly: true,
    delayedEdgeCount: 2,
    sourceCount: 1,
    repeat: fixture.repeat,
    state: firstState,
  };
}

module.exports = {
  validateFixture,
  verifyCalibrationFixture,
  verifyFixture,
};
