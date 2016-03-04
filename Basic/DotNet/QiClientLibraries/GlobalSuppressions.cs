// This file is used by Code Analysis to maintain SuppressMessage
// attributes that are applied to this project.
// Project-level suppressions either have no target or are given
// a specific target and scoped to a namespace, type, member, etc.

using System.Diagnostics.CodeAnalysis;

[assembly:
    SuppressMessage("Potential Code Quality Issues",
        "RECS0022:A catch clause that catches System.Exception and has an empty body", Justification = "<Pending>",
        Scope = "member", Target = "~M:QiLibsSample.Program.Main(System.String[])")]
[assembly:
    SuppressMessage("Redundancies in Symbol Declarations",
        "RECS0004:An empty public constructor without paramaters is redundant.", Justification = "<Pending>",
        Scope = "member", Target = "~M:QiLibsSample.WaveData.#ctor")]