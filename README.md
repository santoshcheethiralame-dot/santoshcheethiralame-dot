<pre>
  █████████    █████████   ██████   █████ ███████████    ███████     █████████  █████   █████
 ███░░░░░███  ███░░░░░███ ░░██████ ░░███ ░█░░░███░░░█  ███░░░░░███  ███░░░░░███░░███   ░░███
░███    ░░░  ░███    ░███  ░███░███ ░███ ░   ░███  ░  ███     ░░███░███    ░░░  ░███    ░███
░░█████████  ░███████████  ░███░░███░███     ░███    ░███      ░███░░█████████  ░███████████
 ░░░░░░░░███ ░███░░░░░███  ░███ ░░██████     ░███    ░███      ░███ ░░░░░░░░███ ░███░░░░░███
 ███    ░███ ░███    ░███  ░███  ░░█████     ░███    ░░███     ███  ███    ░███ ░███    ░███
░░█████████  █████   █████ █████  ░░█████    █████    ░░░███████░  ░░█████████  █████   █████
 ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░    ░░░░░    ░░░░░       ░░░░░░░     ░░░░░░░░░  ░░░░░   ░░░░░

[    0.000000] booting santosh 20.x-pesu (bengaluru, in)
[    0.000001] cpu: 1 core, overclocked on filter coffee
[    0.000420] mem: 51 repos mounted at ~/projects
[    0.001337] modules: python rust go typescript c wgsl ............ <b>ok</b>
[    0.002718] raft: shard 0 elected leader in term 1 ............... <b>ok</b>
[    0.003141] gpu: webgpu adapter found, writing shaders by hand ... <b>ok</b>
[    0.004096] agents: AGENTS.md is now enforced, not suggested ..... <b>ok</b>
[    0.005000] net: <a href="https://santoshcheethirala.vercel.app">portfolio</a> up · <a href="https://www.linkedin.com/in/santoshcheethirala/">linkedin</a> up
[    0.006000] ready. try <b>man santosh</b>
</pre>

<br>

**`~ $ man santosh`**

<pre>
SANTOSH(1)                      User Commands                      SANTOSH(1)

<b>NAME</b>
       santosh - builds systems that have to be right, and measures the
       AI systems that only claim to be

<b>SYNOPSIS</b>
       <b>santosh</b> [--systems] [--ai-safety] [--agents] [--shaders] <i>problem</i>

<b>DESCRIPTION</b>
       CS undergrad at PES University, Bengaluru (CSE '28). Researches
       hallucination attribution at PESU Labs.

       Prefers problems where the answer has to be shown, not asserted:
       lost writes reproduced under a linearizability checker, agent rules
       proven against git history, safety audits that come with an
       estimate of what they missed.

<b>OPTIONS</b>
       <b>--systems</b>      consensus, storage engines, breaking databases on purpose.
                      see <a href="https://github.com/santoshcheethiralame-dot/TESSERA">tessera</a>(1), <a href="https://github.com/santoshcheethiralame-dot/HighWater">highwater</a>(1)

       <b>--ai-safety</b>    interpretability, audit coverage, models that introspect.
                      see <a href="https://github.com/santoshcheethiralame-dot/GlassBox">glassbox</a>(1), <a href="https://github.com/santoshcheethiralame-dot/MissingMass">missingmass</a>(1)

       <b>--agents</b>       coding agents that follow the rules they were given.
                      see <a href="https://github.com/santoshcheethiralame-dot/INJUNCT">injunct</a>(1), <a href="https://github.com/santoshcheethiralame-dot/PRECEDENT">precedent</a>(1)

       <b>--shaders</b>      neural nets and stepwells, rendered on your GPU.
                      see <a href="https://github.com/santoshcheethiralame-dot/GRADIENT">gradient</a>(1), <a href="https://github.com/santoshcheethiralame-dot/BAOLI">baoli</a>(1)

<b>BUGS</b>
       READMEs are reliably longer than the code they describe.
       Does not trust "majority" durability. Has receipts.

<b>SEE ALSO</b>
       <a href="https://santoshcheethirala.vercel.app">portfolio</a>(7), <a href="https://www.linkedin.com/in/santoshcheethirala/">linkedin</a>(1), neofetch(1)

PESU                            November 2026                      SANTOSH(1)
</pre>

<br>

**`~ $ neofetch`**

<img alt="neofetch: an ascii cat next to OS, editor, languages, university, research, honours, hackathons and hobbies" src="assets/neofetch.svg" width="880">

<br>

**`~ $ tree ~/projects -L 2`**

<pre>
<b>~/projects</b>
├── <b>systems/</b>
│   ├── <a href="https://github.com/santoshcheethiralame-dot/TESSERA">tessera/</a>          sharded, replicated KV store. std-only rust, zero crates
│   └── <a href="https://github.com/santoshcheethiralame-dot/HighWater">highwater/</a>        made couchbase lose 56 acknowledged writes. on purpose
├── <b>agents/</b>
│   ├── <a href="https://github.com/santoshcheethiralame-dot/INJUNCT">injunct/</a>          your AGENTS.md is a suggestion. this makes it a rule
│   ├── <a href="https://github.com/santoshcheethiralame-dot/PRECEDENT">precedent/</a>        one failed run becomes a check the agent can't skip
│   ├── <a href="https://github.com/santoshcheethiralame-dot/LIFT">lift/</a>             revenue recovery that subtracts the money arriving anyway
│   └── <a href="https://github.com/santoshcheethiralame-dot/CallSheet">callsheet/</a>        render farm → grafana → agent that cuts shots to make review
├── <b>ai-safety/</b>
│   ├── <a href="https://github.com/santoshcheethiralame-dot/GlassBox">glassbox/</a>         microscope for LLMs. ablate a feature, watch the answer move
│   └── <a href="https://github.com/santoshcheethiralame-dot/MissingMass">missingmass/</a>      how much did the safety audit miss? capture-recapture
├── <b>data/</b>
│   ├── <a href="https://github.com/santoshcheethiralame-dot/ConRAG">conrag/</a>           RAG that notices when its sources disagree
│   └── <a href="https://github.com/santoshcheethiralame-dot/UNTANGLE">untangle/</a>         finds UPI mule rings by scoring the graph, not the hop
├── <b>gpu/</b>
│   ├── <a href="https://github.com/santoshcheethiralame-dot/GRADIENT">gradient/</a>         neural nets trained in WebGPU shaders, in a browser tab
│   ├── <a href="https://github.com/santoshcheethiralame-dot/BAOLI">baoli/</a>            60fps descent into an 18th-century jodhpur stepwell
│   └── <a href="https://github.com/santoshcheethiralame-dot/ShowMe">showme/</a>           ask anything, an LLM animates the answer live
├── <b>learning/</b>
│   ├── <a href="https://github.com/santoshcheethiralame-dot/EMBER-BOOK">ember-book/</a>       DSA textbook. 1,075,998 assertions, 0 failures
│   ├── <a href="https://github.com/santoshcheethiralame-dot/SMUDGE">smudge/</a>           detective game where only physics can catch the liar
│   ├── <a href="https://github.com/santoshcheethiralame-dot/ATTEST">attest/</a>           proof a human understood this. oral defense for essays
│   ├── <a href="https://github.com/santoshcheethiralame-dot/ATLAS">atlas/</a>            my ML study map, from the maths up to AI safety
│   ├── <a href="https://github.com/santoshcheethiralame-dot/ORBIT">orbit/</a>            local-first day planner for exam season
│   └── <a href="https://github.com/santoshcheethiralame-dot/CRUX">crux/</a>             exam-tuned notes, MCQs and flashcards
├── <b>misc/</b>
│   ├── <a href="https://github.com/santoshcheethiralame-dot/TERRACREST">terracrest/</a>       invite-only bengaluru real-estate platform
│   └── <a href="https://github.com/santoshcheethiralame-dot/skills">skills/</a>           33 portable claude code skills
└── <b>.private/</b>             dragnet  lineup  forge  hemlock  chronos

8 directories, 21 projects, 5 still cooking
</pre>

<br>

**`~ $ git diff HEAD~1 -- now.md`**

```diff
@@ santosh/now.md @@
- reading interpretability papers
+ writing one: MissingMass, arXiv preprint aimed at Dec 2026
- trusting "majority" durability
+ 56 acknowledged writes later: persistToMajority
- AGENTS.md as a polite suggestion
+ AGENTS.md as a pre-commit hook
- learning raft from the paper
+ watching the simulator find a split-brain on seed 99
```

<br>

**`~ $ cat src/main.rs`**

```rust
// std only. no crates were harmed.
fn main() {
    let mut me = Santosh::boot();            // cse '28, pes university

    loop {
        let thing = me.build();
        let bugs  = me.break_it(&thing);     // the fun part
        assert!(bugs.iter().all(|b| b.reproduces()));   // or it didn't happen
        me.write_readme(&thing);             // longer than the code. always.
        me.coffee += 1;                      // filter. non-negotiable.
    }
}
```

<br>

**`~ $ ./telemetry --since 1y`**

<!-- telemetry:start -->
```text
  warming up... the first run fills this in after the next push to main.
```
<!-- telemetry:end -->

<br>

**`~ $ snake --eat ~/.contributions`**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/santoshcheethiralame-dot/santoshcheethiralame-dot/output/snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/santoshcheethiralame-dot/santoshcheethiralame-dot/output/snake.svg">
  <img alt="a snake eating my contribution graph" src="https://raw.githubusercontent.com/santoshcheethiralame-dot/santoshcheethiralame-dot/output/snake-dark.svg" width="100%">
</picture>

<details>
<summary><code>~ $ pacman --eat ~/.contributions</code></summary>
<br>
<img alt="pac-man eating my contribution graph" src="https://raw.githubusercontent.com/santoshcheethiralame-dot/santoshcheethiralame-dot/output-arcade/pacman-contribution-graph.svg" width="100%">
</details>

<br>

<pre>
santosh@github:~$ exit
logout

[Process completed]
</pre>

<p align="right"><img alt="visitors" src="https://komarev.com/ghpvc/?username=santoshcheethiralame-dot&label=visitors&color=FFB454&style=flat-square"></p>
