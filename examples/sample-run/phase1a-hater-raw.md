# Phase 1A: Hater Mode Critical Feedback — mega-eval

## 1. Product Hunt Critic

**Perspective:** Seen 500 "AI-powered analysis" tools launch this year alone. Filters hard for differentiation.

**Main criticism:** This is a prompt chain packaged as a product. There's no proprietary model, no unique data, no moat — anyone who reads your SKILL.md can rebuild this in an afternoon. The output is 6 Word docs, which feels like a 2005 deliverable format for a 2026 AI tool.

**Specific concern:** What happens when Claude's built-in reasoning gets good enough that "run hater-mode + competitive analysis + synthesis" is just... a single prompt? You're packaging a workflow that the underlying model will absorb.

**What would change their mind:** A hosted version with persistent history, so I can track how my product evaluation changes over time. Or a unique evaluation framework that can't be trivially replicated — proprietary scoring, benchmark data, something defensible.

## 2. Hacker News Commenter

**Perspective:** Immediately skeptical of anything that wraps an LLM in more LLM calls and calls it a pipeline.

**Main criticism:** This is a SKILL.md file that tells Claude to call itself three times in parallel and then merge the results into Word docs. The "pipeline" is just prompt engineering with extra steps. The ingest.py script is a thin wrapper around pdftotext and pandoc — tools that already exist. What engineering actually happened here?

**Specific concern:** The subagent prompts contain `<hater-mode-skill-path>` and `<workspace>` placeholders. Who resolves these? Is there any actual runtime that does this, or does Claude just... guess the paths? This feels undertested.

**What would change their mind:** Show me the evaluation output on a real product next to a human analyst's review. If the output quality is genuinely comparable, the simplicity of the implementation is actually a strength.

## 3. Reddit User (r/ClaudeAI)

**Perspective:** Practical, has tried dozens of Claude workflows, low tolerance for things that don't actually work.

**Main criticism:** 10-15 minutes for 6 Word docs that I could get by just asking Claude "evaluate this product from every angle"? The README promises a lot but there's zero sample output. Show me what these docs actually look like. For all I know this produces 6 files of generic fluff.

**Specific concern:** The Dependencies section and Prerequisites section say the same thing. Also, if the dependent skills aren't installed, it "uses built-in prompt templates" — so are the dependencies required or not? Pick one.

**What would change their mind:** A before/after comparison. Show me what Claude produces with a naked prompt vs. this pipeline on the same input. If there's a meaningful quality gap, I'll install it today.

## 4. X/Twitter User

**Perspective:** Snappy, meme-literate, punches up at overengineered AI tools.

**Main criticism:** "We built a 6-phase pipeline to tell Claude to think harder" is peak AI slop tooling. You literally wrote a prompt that says "be a hater" and another that says "search the web" and called it a product. The output is .docx files. In 2026.

**Specific concern:** The README has a beautiful ASCII flowchart for a process that boils down to "ask Claude three questions, combine the answers, format as Word docs."

**What would change their mind:** If the output was actually fire — like, if someone posted a mega-eval of a real YC startup and it surfaced genuinely non-obvious insights — this would go viral. The packaging is the problem, not the concept.

## 5. Facebook User

**Perspective:** Non-technical, just wants to know if this helps them.

**Main criticism:** I don't understand what this is or who it's for. The README jumps straight into "phases" and "subagents" and "SKILL.md" without ever telling me in plain language: what do I get, and why is it better than just asking ChatGPT to review my business idea?

**Specific concern:** I need to install Claude Code, clone a git repo, copy files to a hidden .claude directory, and also install three other "skills"? That's not a product, that's homework. I'll just ask Claude directly.

**What would change their mind:** A one-click install or a web interface. Or at minimum, a "here's what the output looks like" section with screenshots of the actual Word docs.

## 6. LinkedIn User

**Perspective:** Enterprise-minded, cares about reliability, repeatability, and whether this can scale to a team.

**Main criticism:** There's no versioning on the evaluation framework itself. If I run this on a product today and again in 3 months, will the methodology be consistent? There's no scoring rubric, no quantitative metrics — just qualitative text. That makes it impossible to track improvement or compare across products. No executive I work with will read 6 Word docs without a dashboard or a score.

**Specific concern:** The "executive summary" is generated last and synthesizes everything, but there's no validation step. What if the hater-mode output contradicts the strengths output and the synthesis just picks a side? Where's the quality gate?

**What would change their mind:** A structured scoring framework (even simple 1-10 ratings per dimension), version-stamped outputs, and a comparison mode so I can run it quarterly and see trends.

## 7. Indie Hackers Member

**Perspective:** Fellow builder, respects the hustle, but questions the business model.

**Main criticism:** This is a cool side project but it's not a business. You're giving away the entire methodology as an MIT-licensed SKILL.md file. Anyone can fork it, tweak it, and call it their own. There's no recurring revenue angle, no premium tier, no data flywheel. What's the plan beyond "put it on GitHub and hope people star it"?

**Specific concern:** The skill depends on three other skills (hater-mode, long-form-outline, docx). If any of those change their interface or stop being maintained, your pipeline breaks and you have no control over it. You're building on someone else's foundation with no fallback.

**What would change their mind:** If this is intentionally open-source community tooling, great — but say that. If you're trying to build something commercial, you need a hosted version, saved evaluations, a team sharing layer, and a reason to pay.

## 8. Software Tester

**Perspective:** Thinks in edge cases, failure modes, and regression scenarios.

**Main criticism:** There are zero tests. No test inputs, no expected outputs, no way to validate that a run was successful. The pipeline-checklist.md is a manual checklist — there's nothing automated. If Phase 1B's web search returns garbage, how does Phase 2 know to discount it? The error handling section says "be honest about thin results" but that's a hope, not a mechanism.

**Specific concern:** The ingest.py script calls subprocess.run with user-provided file paths and no input sanitization. If someone passes a filename with shell metacharacters, pdftotext or pandoc could behave unexpectedly. Also, the 3000-character truncation in generate_brief_template is arbitrary — what if the critical information is at character 3001?

**What would change their mind:** A test suite with at least 3 reference inputs (a simple text block, a URL, a multi-source combo) and their expected outputs. Even golden-file tests would be a start. And sanitize those subprocess inputs.

## 9. Layperson

**Perspective:** Heard about AI tools, wants something simple that works.

**Main criticism:** I read the entire README and I still don't know what "mega eval" actually gives me in plain English. "6 structured Word documents covering critical feedback, competitive landscape..." — is this for my small bakery business? My app idea? A school project? The README talks about "subagents" and "Phase 1A" like I'm supposed to know what that means.

**Specific concern:** Why Word documents? I don't even have Microsoft Word. Can I get a PDF? A web page? Anything I can just open?

**What would change their mind:** A "Who is this for?" section with 2-3 concrete examples: "If you have a startup idea and want to stress-test it before building, mega-eval gives you X. If you're launching a product and want to find blind spots, it gives you Y."

## 10. Designer

**Perspective:** Obsessed with the experience, not just the output.

**Main criticism:** The deliverable is 6 separate Word documents with no visual design, no information hierarchy beyond markdown headings, and no consideration for how someone actually uses an evaluation. Nobody reads 6 docs linearly. The executive summary should link to or embed the key findings from each doc, not just reference them. And there's no thought given to the reading experience — no charts, no visual scoring, no comparison tables.

**Specific concern:** The pipeline produces text-heavy output with no visual artifacts. A competitive landscape without a positioning map? A strengths analysis without a radar chart? These are table-stakes deliverables in any real product evaluation.

**What would change their mind:** Even basic visual outputs — a 2x2 positioning matrix, a priority/impact chart for fixes, a simple score card. The content might be solid but the delivery format undermines it.

## 11. Late Adopter

**Perspective:** Conservative, doesn't trust AI-generated analysis, needs to see proof before adopting.

**Main criticism:** You're asking me to trust an AI to evaluate my business idea through 6 phases of... more AI? The competitive analysis is web searches run by Claude. The "hater mode" is Claude pretending to be 12 different people. The synthesis is Claude reading its own output. At what point does a human with domain expertise enter the picture? This is a hall of mirrors.

**Specific concern:** The README says "expect 10-15 minutes for a full run." I can get a human consultant's first impressions in 15 minutes, and they have actual market experience. What's the quality benchmark here?

**What would change their mind:** Validation data. Run this on 10 products where the outcome is known (succeeded, failed, pivoted) and show that the evaluation would have flagged the right issues. Without that, this is AI theater.

## 12. General Hater

**Perspective:** Contrarian who pokes holes in everything.

**Main criticism:** This is a README for a prompt. That's it. You wrote a detailed prompt, split it into files, added a Python script that calls pdftotext, and put it on GitHub with an MIT license and an ASCII flowchart. The repo has one commit. The "Cowork" install path references a .skill file that's just a zip of the same markdown. The Dependencies section is duplicated in Prerequisites. And you're linking to github.com/anthropics/claude-code/tree/main/skills/ for the dependent skills — do those paths even exist?

**Specific concern:** The whole thing is Claude-dependent with no portability. If someone uses a different LLM, this is useless. If Anthropic changes how skills work, this breaks. You've built a sandcastle on someone else's beach.

**What would change their mind:** Nothing about the packaging. But if someone posts "I ran mega-eval on my startup idea and it caught 3 things my advisors missed," that changes everything. Results beat packaging every time.

---

## Executive Roast Summary

| Dimension | Severity | Core Issue |
|-----------|----------|------------|
| **Differentiation** | High | It's a prompt chain with no moat — easily replicated |
| **Sample Output** | High | No examples of what the deliverables actually look like |
| **Target Audience** | Medium | README doesn't say who this is for in plain terms |
| **Output Format** | Medium | 6 Word docs feels dated; no visual artifacts |
| **Testing** | Medium | Zero tests, no validation, no golden-file references |
| **Duplicate Content** | Low | Prerequisites and Dependencies sections overlap |
| **Input Sanitization** | Low | ingest.py subprocess calls lack path sanitization |

**Recurring theme:** Show the output. Every critic's objection weakens dramatically if you can demonstrate that this pipeline produces meaningfully better analysis than a single Claude prompt. The README sells the process but not the result.
