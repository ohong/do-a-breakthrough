"use strict";

const primaryFixture = {
  name: "abcde-nonadjacent-sources",
  graph: {
    vertices: ["a", "b", "c", "d", "e"],
    edges: [
      { u: "a", v: "b", weight: 2 },
      { u: "b", v: "c", weight: 1 },
      { u: "c", v: "d", weight: 1 },
      { u: "d", v: "a", weight: 1 },
      { u: "a", v: "e", weight: 1 },
    ],
  },
  sources: ["c", "e"],
  expectedStates: [
    "D[c>b,c>d,e>a] F[]",
    "D[a>d,d>a] F[a>b@1,b>a@1]",
    "D[a>b,a>e,b>a,d>c] F[a>b@1]",
    "D[a>b,a>d,a>e,b>c,c>b] F[]",
    "D[c>d,d>c] F[]",
    "D[c>b,d>a] F[]",
    "D[a>e] F[a>b@1,b>a@1]",
    "D[a>b,b>a] F[]",
    "D[a>d,a>e,b>c] F[]",
    "D[c>d,d>c] F[]",
  ],
  repeat: { firstRound: 5, secondRound: 10, period: 5 },
};

const alternateFixture = {
  name: "numeric-adjacent-sources",
  graph: {
    vertices: ["0", "1", "2", "3", "4"],
    edges: [
      { u: "0", v: "2", weight: 1 },
      { u: "0", v: "3", weight: 1 },
      { u: "0", v: "4", weight: 1 },
      { u: "1", v: "2", weight: 2 },
      { u: "1", v: "3", weight: 1 },
    ],
  },
  sources: ["0", "4"],
  expectedStates: [
    "D[0>2,0>3,0>4,4>0] F[]",
    "D[0>2,0>3,3>1] F[2>1@1]",
    "D[2>1,3>1] F[1>2@1,2>1@1]",
    "D[1>2,2>1] F[]",
    "D[1>3,2>0] F[]",
    "D[0>3,0>4,3>0] F[]",
    "D[0>2,0>4,3>1] F[]",
    "D[] F[1>2@1,2>1@1]",
    "D[1>2,2>1] F[]",
  ],
  repeat: { firstRound: 4, secondRound: 9, period: 5 },
};

const figure6Calibration = {
  name: "paper-figure-6-calibration",
  graph: {
    vertices: ["0", "1", "2", "3", "4", "5"],
    edges: [
      { u: "0", v: "1", weight: 1 },
      { u: "0", v: "2", weight: 1 },
      { u: "1", v: "3", weight: 1 },
      { u: "2", v: "3", weight: 3 },
      { u: "2", v: "4", weight: 3 },
      { u: "3", v: "5", weight: 1 },
      { u: "4", v: "5", weight: 1 },
    ],
  },
  sources: ["0"],
  expectedRepeatedState: "D[3>1,3>2,3>5] F[]",
  repeat: { firstRound: 5, secondRound: 13, period: 8 },
};

module.exports = {
  fixtures: [primaryFixture, alternateFixture],
  primaryFixture,
  alternateFixture,
  figure6Calibration,
};
