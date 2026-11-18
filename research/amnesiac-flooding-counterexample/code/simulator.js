"use strict";

function compareMessages(left, right) {
  return (
    left.from.localeCompare(right.from) ||
    left.to.localeCompare(right.to) ||
    (left.residual ?? 0) - (right.residual ?? 0)
  );
}

function assertGraphShape(graph) {
  if (!graph || !Array.isArray(graph.vertices) || !Array.isArray(graph.edges)) {
    throw new TypeError("graph must contain vertices and edges arrays");
  }
  if (
    graph.vertices.length === 0 ||
    graph.vertices.some(
      (vertex) => typeof vertex !== "string" || vertex.length === 0,
    )
  ) {
    throw new Error("vertices must be non-empty strings");
  }

  const vertices = new Set(graph.vertices);
  if (vertices.size !== graph.vertices.length) {
    throw new Error("vertices must be unique");
  }

  const seenEdges = new Set();
  for (const edge of graph.edges) {
    if (!vertices.has(edge.u) || !vertices.has(edge.v) || edge.u === edge.v) {
      throw new Error(`invalid edge ${edge.u}-${edge.v}`);
    }
    if (!Number.isInteger(edge.weight) || edge.weight < 1) {
      throw new Error(`edge ${edge.u}-${edge.v} must have a positive integer weight`);
    }

    const key = [edge.u, edge.v].sort().join("\0");
    if (seenEdges.has(key)) {
      throw new Error(`duplicate edge ${edge.u}-${edge.v}`);
    }
    seenEdges.add(key);
  }
}

function buildAdjacency(graph) {
  assertGraphShape(graph);
  const adjacency = new Map(graph.vertices.map((vertex) => [vertex, []]));

  for (const { u, v, weight } of graph.edges) {
    adjacency.get(u).push({ vertex: v, weight });
    adjacency.get(v).push({ vertex: u, weight });
  }
  for (const neighbors of adjacency.values()) {
    neighbors.sort((left, right) => left.vertex.localeCompare(right.vertex));
  }

  return adjacency;
}

/**
 * Simulate synchronous fixed-delay amnesiac flooding.
 *
 * A send in round r across a weight-w edge is delivered in round r + w - 1.
 * State S_r is sampled after round-r sends and deliveries. It contains all
 * deliveries in r and every still in-flight directed message, represented by
 * the positive number of rounds remaining until delivery.
 */
function simulate(graph, sources, roundCount) {
  if (!Number.isInteger(roundCount) || roundCount < 1) {
    throw new Error("roundCount must be a positive integer");
  }

  const adjacency = buildAdjacency(graph);
  if (!Array.isArray(sources)) {
    throw new TypeError("sources must be an array");
  }
  const sourceSet = new Set(sources);
  if (sourceSet.size !== sources.length) {
    throw new Error("sources must be unique");
  }
  for (const source of sourceSet) {
    if (!adjacency.has(source)) {
      throw new Error(`unknown source ${source}`);
    }
  }

  const states = [];
  let previousDeliveries = [];
  let inFlight = [];

  for (let round = 1; round <= roundCount; round += 1) {
    const deliveries = [];
    const stillInFlight = [];

    for (const message of inFlight) {
      if (message.deliveryRound === round) {
        deliveries.push({ from: message.from, to: message.to });
      } else {
        stillInFlight.push(message);
      }
    }
    inFlight = stillInFlight;

    const receivedFrom = new Map();
    if (round > 1) {
      for (const { from, to } of previousDeliveries) {
        if (!receivedFrom.has(to)) {
          receivedFrom.set(to, new Set());
        }
        receivedFrom.get(to).add(from);
      }
    }

    const activeVertices =
      round === 1
        ? [...sourceSet].sort()
        : [...receivedFrom.keys()].sort();

    for (const from of activeVertices) {
      const excludedNeighbors = receivedFrom.get(from) ?? new Set();
      for (const { vertex: to, weight } of adjacency.get(from)) {
        if (excludedNeighbors.has(to)) {
          continue;
        }

        const deliveryRound = round + weight - 1;
        if (deliveryRound === round) {
          deliveries.push({ from, to });
        } else {
          inFlight.push({ from, to, deliveryRound });
        }
      }
    }

    deliveries.sort(compareMessages);
    inFlight.sort(
      (left, right) =>
        left.deliveryRound - right.deliveryRound || compareMessages(left, right),
    );

    const state = {
      round,
      deliveries: deliveries.map(({ from, to }) => ({ from, to })),
      inFlight: inFlight
        .map(({ from, to, deliveryRound }) => ({
          from,
          to,
          residual: deliveryRound - round,
        }))
        .sort(compareMessages),
    };
    states.push(state);
    previousDeliveries = deliveries;
  }

  return states;
}

function stateKey(state) {
  const deliveries = state.deliveries
    .map(({ from, to }) => `${from}>${to}`)
    .join(",");
  const inFlight = state.inFlight
    .map(({ from, to, residual }) => `${from}>${to}@${residual}`)
    .join(",");
  return `D[${deliveries}] F[${inFlight}]`;
}

module.exports = {
  assertGraphShape,
  buildAdjacency,
  simulate,
  stateKey,
};
