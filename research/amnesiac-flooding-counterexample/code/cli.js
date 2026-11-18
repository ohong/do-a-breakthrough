#!/usr/bin/env node
"use strict";

const { figure6Calibration, fixtures } = require("./fixtures");
const { verifyCalibrationFixture, verifyFixture } = require("./verifier");

function main(selectedFixtures = fixtures, stdout = process.stdout) {
  for (const fixture of selectedFixtures) {
    const certificate = verifyFixture(fixture);
    const delayed = certificate.properties.delayedEdge;
    const { firstRound, secondRound, period } = certificate.repeat;
    stdout.write(
      [
        "PASS",
        certificate.name,
        `V=${fixture.graph.vertices.length}`,
        `E=${fixture.graph.edges.length}`,
        "connected",
        "bipartite",
        `sources=${fixture.sources.join(",")}`,
        `delay=${delayed.u}-${delayed.v}:${delayed.weight}`,
        `S${firstRound}=S${secondRound}`,
        `period=${period}`,
        certificate.state,
      ].join(" ") + "\n",
    );
  }
}

function runCli(
  selectedFixtures = fixtures,
  stdout = process.stdout,
  stderr = process.stderr,
) {
  try {
    main(selectedFixtures, stdout);
    return true;
  } catch (error) {
    stderr.write(`FAIL ${error.message}\n`);
    process.exitCode = 1;
    return false;
  }
}

function printCalibration(
  calibration = figure6Calibration,
  stdout = process.stdout,
) {
  const certificate = verifyCalibrationFixture(calibration);
  const { firstRound, secondRound, period } = certificate.repeat;
  stdout.write(
    [
      "CALIBRATION",
      certificate.name,
      "not-target-witness",
      `sources=${certificate.sourceCount}`,
      `delayed-edges=${certificate.delayedEdgeCount}`,
      `S${firstRound}=S${secondRound}`,
      `period=${period}`,
      certificate.state,
    ].join(" ") + "\n",
  );
}

if (require.main === module) {
  if (runCli()) {
    try {
      printCalibration();
    } catch (error) {
      process.stderr.write(`FAIL ${error.message}\n`);
      process.exitCode = 1;
    }
  }
}

module.exports = { main, printCalibration, runCli };
