---
type: Article
title: Core dump epidemiology: fixing an 18-year-old bug
source: openai-news
resource: https://openai.com/index/core-dump-epidemiology-data-infrastructure-bug
published: 2026-06-30
tags: []
detected: 2026-07-01T00:04:17+08:00
---

(摘要生成失败)

> 失败原因：RuntimeError: claude 退出码 1: Not logged in · Please run /login

## Full Text

Core dump epidemiology: fixing an 18-year-old bug | OpenAI
Skip to main content
Research
Products
Business
Developers
Company
Foundation
(opens in a new window)
Log in
Try ChatGPT
(opens in a new window)
Research
Products
Business
Developers
Company
Foundation
(opens in a new window)
Try ChatGPT
(opens in a new window)
Login
OpenAI
June 30, 2026
Engineering
Core dump epidemiology: fixing an 18-year-old bug
Using population-level analysis to debug tricky crashes in our data infrastructure.
Loading…
Share
First debugging attempt: carefully examining a few core dumps
First debugging attempt: carefully examining a few core dumps
Clues from the stack
Doctor or epidemiologist?
Cleaning the data
Bug #1: the bad host
Exception handling is a dynamic control transfer
Undoing one last assumption
Bug #2: the libunwind bug
Why the cores masked as ordinary bad returns
A single-instruction race window
Why did the libunwind bug appear now?
The power of a population-level diagnosis
Table of contents
First debugging attempt: carefully examining a few core dumps
Clues from the stack
Doctor or epidemiologist?
Cleaning the data
Bug #1: the bad host
Exception handling is a dynamic control transfer
Undoing one last assumption
Bug #2: the libunwind bug
Why the cores masked as ordinary bad returns
A single-instruction race window
Why did the libunwind bug appear now?
The power of a population-level diagnosis
OpenAI’s models and agents increasingly rely on scalable data infrastructure in order to search for relevant data at inference time: when the models are thinking about your question. Some of these services are written in C++, whose low-level control of the system lets us maximize performance and minimize memory usage. Those efficiency benefits are important as we scale, but C++’s lack of memory safety means that bugs can cause crashes by writing to incorrect or non-existent memory addresses.
A few months ago we observed some crashes from inside the Rockset service, a bespoke part of our ChatGPT data infrastructure which is key to many data plugins and to searching over conversations. In each of these crashes, a normal C++ function seemed to finish and then return to a bogus address, causing the kernel to stop the program because the instruction pointer no longer pointed at code. Sometimes the return address slot in the stack frame was NULL. Sometimes the stack pointer CPU register itself seemed to be off by 8 bytes, as if
%rsp
had somehow been decremented in the middle of normal execution. In both cases the crash happened on return.
These are not normal failure modes for application code. A stray write that lands only on a saved return address is possible, but extremely unlikely. A bug that misaligns
%rsp
by 8 without involving inline assembly,
setcontext
, or
longjmp
(none of which we use) is even stranger, because compiled code only adjusts that register directly in the function prologue and epilogue. Every hypothesis we (or ChatGPT) could think of had strong evidence against it, so the bug seemed impossible.
What we assumed was one problem eventually turned out to be two unrelated bugs, coincidentally discovered at the same time. First, silent hardware corruption on one Azure host, where the CPU just didn’t do math correctly. Second, an 18-year-old race condition in GNU libunwind, an unnoticed bug in a widely used open source library.
This post is the story of how we identified and fixed seemingly inexplicable crashes by thinking like an epidemiologist and building a high-quality data set about the entire population of crashes.
First debugging attempt: carefully examining a few core dumps
First, let’s go deeper on Rockset. It’s a cloud-native data system for search and real-time analytics that we use for many internal use cases at OpenAI, such as sync connectors (Rockset was acquired by OpenAI in 2024). Streaming updates are used to maintain an up-to-date index of a workspace’s knowledge base so that ChatGPT can search for relevant information when answering questions or performing actions.
Rockset’s execution layer is written in C++. The C++ language provides low-level access to the CPU, which is good for performance and efficiency, but it means that application bugs can lead to invalid memory accesses and segfaults. To help track these down we use folly’s fatal signal handler to log a stack trace when a crash happens, and we upload the corresponding core dumps (a snapshot of the state of the program when it crashed) to Azure blob storage for later analysis. All of Rockset’s query processing leaves are replicated, which minimizes the client impact of a crash. However, each segfault corresponds to a bug that needs to be fixed to meet our reliability and quality goals.
Our initial approach was to treat these cores like a conventional debugging problem: inspect a few core dumps very closely, form hypotheses, and rule them out one by one.
Most of the crashes occurred in a method called
DocumentTree::updateDocument
. In these crashes it appeared that
updateDocument
had called some unknown function X, the stack had become corrupted while X was active, then X had returned to an address that wasn’t executable code. In some cases X’s just-popped frame looked valid except that its saved return address was NULL. In other cases the stack pointer itself looked wrong, but the next valid frame still seemed to be
updateDocument
.
We didn’t know when the stack was getting corrupted, which left a huge search space.
updateDocument
is a large method that undergoes a lot of inlining, so the number of candidates for X was overwhelming.
Was this a bug in our C++ code? A compiler or linkage issue? A problem in one of our runtime libraries? A Linux kernel bug around signal delivery or context switching? Something even rarer? If this was a stray write, why wasn’t it caught by our ASAN staging environment?
We tried to use our application-level logs to identify all occurrences of the problem, but stack-corruption bugs are hard to classify from logs alone because the logged stack traces are themselves corrupted or missing. We weren’t able to construct a log query that didn’t have both false positives and false negatives. We manually inspected more cores and found some additional examples, but that process was too labor-intensive to give us a trustworthy data set.
At this stage of the investigation, we (incorrectly) ruled out a hardware bug, because we saw crashes across multiple regions and multiple hardware types, so we were still looking for software-only causes. For a few days, we went super-deep on a single misaligned-
%rsp
crash, reconstructing the pre-crash history using stack and register contents. This produced some possible clues, but because we didn’t let go of our initial conclusions that all of the bugs had the same cause, this didn’t get us unstuck.
Clues from the stack
Before getting to the turning point of our investigation, it’s important to explain what kind of information we were extracting from the core files.
Rockset is compiled with
-fno-omit-frame-pointer
, so the active stack frame is always reachable through
%rbp
, and callers form a linked list of frame pointers.
On Linux
x86_64
, the AMD64 System V ABI also reserves 128 bytes below
%rsp
as the red zone. That region is available to userspace code and, importantly, the kernel promises not to clobber it when it delivers a signal, as part of the ABI contract.
The red zone was central to our debugging of a post-return crash, because it preserves some information from before the return. When a
SIGSEGV
is triggered, folly’s fatal signal handler runs on the crashing thread’s stack. Stack frames that are no longer active (because their function has returned) will get clobbered by the signal handler, except for the last 128 bytes. That’s why we can say things like “X’s just-popped stack frame looked valid, except for a NULL return address.” The red zone preserves some of the inactive frames, or sometimes just the tail of one inactive frame.
We found one misaligned-stack crash in which all of the functions involved were very small. That let us see that
%rsp
had become misaligned during execution of a relatively simple function, and that more calls had succeeded afterward. The program only crashed when the active function finally tried to return. None of those code paths used exceptions, inline assembly,
setcontext
, or
longjmp
, so if the stack pointer truly changed in the way the core suggested, no plausible bug in userspace code explained the issue.
That pushed us toward the kernel.
Rockset uses signals more aggressively than most programs. Query execution is broken into many lightweight tasks that exchange data. This is important for handling high-QPS workloads efficiently, but it makes per-query CPU accounting awkward as work for many queries is multiplexed onto the same thread pool.
Our solution is something we call
coarse_thread_cputime_clock
, which approximates
clock_gettime(CLOCK_THREAD_CPUTIME_ID, ...)
cheaply enough to sample at every task boundary. The
timer_create
API can be used to schedule a periodic signal delivery based on several notions of the passage of time, including the accumulation of CPU time. We schedule a signal (SIGUSR2) to be delivered every few milliseconds of CPU time, at which point the signal handler updates a thread-local value. Even though many tasks don’t see the coarse clock advance while they are executing, summing all of the deltas produces an unbiased estimate of the actual CPU time for a query.
Because we deliver signals so often, a rare kernel bug around context switching or signal delivery seemed plausible. We spent time reading bug reports, kernel source code, and the Azure-specific kernel patches. We tried stress tests. We weren’t able to find anything that seemed related.
At that point we decided to step back and try a different approach.
Doctor or epidemiologist?
There are two broad ways to debug a problem like this.
One is to act like a doctor of sorts: focus on one patient, run lots of tests, and try to diagnose a single case from detailed evidence.
The other is to act more like an epidemiologist: look at the entire population and ask whether there are patterns that a single case cannot reveal. Did the bug start at a specific release? Does it correlate with one hardware SKU (the specific CPU and server model), one region, or one kernel version? Are there multiple distinct clusters hiding inside what looks like one syndrome?
We had mostly been in doctor mode. The key shift was deciding that we needed to gather high-quality population data.
Cleaning the data
Our previous attempts to automatically find all of the instances of the problem failed because we were trying to use text searches over the logs. The core dumps themselves have a lot more information, but looking at them manually didn’t scale. We decided to invest the effort to build a pipeline that could automatically analyze the core dumps.
We had ChatGPT write a script that downloaded a prefix of each core file, extracted the registers, filtered known false positives using the logs, and automatically labeled the crash as return-to-null, misaligned-stack, or other. Then we ran that script in parallel over every production Rockset core dump from the previous year.
This was the turning point.
Once we had a clean data set, correlations appeared immediately. What we had been treating as one weird bug was actually
two
separate crash populations.
The return-to-null cores were spread across many clusters and geographic regions. Their frequency had increased recently, but there was no crisp start date and no clean infrastructure boundary.
The misaligned-stack crashes looked completely different. They all came from one region, had a clear start date, and never happened on nodes that had been running for a long time. Even though they involved multiple Azure VMs (virtual machines hosted in the cloud), the pattern looked like one physical machine with bad hardware causing problems for whichever VM happened to land on it.
That was the moment we realized we had been mentally conflating two bugs. Because we had been mixing counterexamples from both bugs, we couldn’t find a single coherent explanation.
Bug #1: the bad host
Armed with a clean list of Kubernetes nodes and timestamps, we were able to trace the misaligned-stack crashes back to a single physical host, which was easy to denylist.
We were not able to reproduce the register corruption on that host in a controlled environment, even after several weeks of stress testing. Once the problematic host was taken out of service, however, the misaligned-stack crashes disappeared.
Removing the bad host isn’t a permanent solution, in the sense that it doesn’t prevent a new occurrence of the same problem. We can, however, change the software so that if a similar issue recurs, it is easily detected and handled. We improved our fatal signal handler to include register state so that we can detect recurrence only from the logs (no core dump needed). We changed the control plane so that VMs are usually reused instead of recycled, which makes bad-node detection much easier at our level of the infrastructure stack. We also updated our runbooks (and our team’s mental models) to include this possibility.
With the bad-host crashes separated out, the remaining return-to-null cores became much easier to reason about. Earlier we had ruled out exception unwinding because we thought we had counterexamples: crashes in code paths where exceptions were definitely not used. But those counterexamples were all from the hardware-corruption cluster.
Once we revisited the remaining cores with that in mind we found that this conclusion was exactly backward: the crashes were all happening during exception unwinding.
Exception handling is a dynamic control transfer
When C++ throws an exception, the runtime has to discover which catch block should receive it and which destructors or cleanup handlers should run along the way. The compiler emits this metadata, but the actual matching happens dynamically at runtime.
Exception unwinding is not actually performed by the function that invokes
throw
, but by helper functions called by the resulting compiled code. Those runtime routines examine the stack, fetch metadata about the functions found on the stack, dynamically look for cleanup handlers and catch blocks, and then transfer control to one of those locations. Transferring control includes unwinding all of the intervening stack frames (including those of the helper functions).
Operationally, this is much closer to a
longjmp
or a fiber switch than to a normal call and return. Callee save registers must be restored, as well as the stack frame registers
%rbp
and
%rsp
.
Our binary links against two libraries that contain implementations of the functions that perform C++ exception unwinding: libgcc and GNU libunwind. GNU libunwind’s definitions were the ones chosen by the dynamic linker. That surprised us; we had expected the libgcc implementation to win because of symbol versioning rules; however, inspecting running binaries showed that wasn’t the case.
Undoing one last assumption
At this point our working hypothesis changed, as we relaxed another assumption that we had made when we thought there was only one bug.
Maybe we were not seeing an ordinary function return to NULL. Maybe we were seeing an unwind transfer—effectively a
setcontext
-style register restore—where the destination instruction pointer had become NULL before control was transferred. In other words, incorrect data from the unwind library rather than an incorrect return address slot on the stack.
That narrowed the problem dramatically. Either GNU libunwind was computing the wrong destination state, or it was computing the right state and something was corrupting it before it could be applied.
We read the GNU libunwind source and found that it synthesizes a
ucontext_t
on the stack, fills in the desired register state for the cleanup handler’s frame, and then hands a pointer to that struct to an internal assembly routine:
_Ux86_64_setcontext
.
At this point we had all of the pieces.
The synthesized
ucontext_t
lives in one of the stack frames that is unwound by
_Ux86_64_setcontext
, during that function’s execution. Was
_Ux86_64_setcontext
reading from the struct after it changed
%rsp
, at which point the struct was no longer part of the active stack? That would make it vulnerable to being clobbered by a signal delivery, such as our frequent
SIGUSR2
.
Bug #2: the libunwind bug
The answer was yes.
Here are the last six instructions of
_Ux86_64_setcontext
in the version of GNU libunwind we were using, which consist mostly of
mov
instructions that load from memory to a destination register:
Plain Text
1
74:        mov    UC_MCONTEXT_GREGS_RSP(%rdi),%rsp
2
75:
3
76:        /* push the return address on the stack */
4
77:        mov    UC_MCONTEXT_GREGS_RIP(%rdi),%rcx
5
78:        push   %rcx
6
79:
7
80:        mov    UC_MCONTEXT_GREGS_RCX(%rdi),%rcx
8
81:        mov    UC_MCONTEXT_GREGS_RDI(%rdi),%rdi
9
82:        retq
(
%rdi
points at the stack-allocated
ucontext_t
, and the
UC_MCONTEXT_*
macros just expand to the fixed offset at which a particular register is stored.)
The first instruction is the beginning of the race window. It updates
%rsp
to point to the new bottom of the active stack. As soon as this happens, the struct pointed to by
%rdi
is no longer part of the active stack (or red zone), and it’s no longer off-limits to the kernel.
Usually this doesn’t cause problems, but if a signal arrives at exactly the right (wrong?) moment, the kernel will build the signal frame at
%rsp-128
. That can overwrite the memory pointed to by
%rdi
.
If that happens before the next instruction reads
UC_MCONTEXT_GREGS_RIP(%rdi)
, then the restored instruction pointer can be corrupted. In our crashes, it became NULL.
That’s the bug.
Why the cores masked as ordinary bad returns
This assembly also explains one of the observations that confused us: why function X had a NULL in the return address slot of the preceding stack frame.
setcontext
was written to restore all registers, including
%rdi
, so it can’t use that register to read
UC_MCONTEXT_GREGS_RIP(%rdi)
at the final moment of the control transfer. Instead, it reads the value earlier, saves it to the stack, restores a few more registers, then uses
retq
to read the saved value and transfer control.
What looked in the cores like “a function returned to NULL” was actually “the unwinder synthesized a target return address on the stack, but that target had been corrupted before the transfer completed.” We had assumed that corruption of the return address slot must happen in-place, because we didn’t know of any places where (corruptible) data was written to the return address slot on purpose.
A single-instruction race window
What makes this bug seem absurd is how narrow this race window is. In this kind of race condition, the external event (the signal) needs to happen in between two steps taken by another thread. The closer those steps are to each other, the less likely the race condition is to happen.
In this case the vulnerable window is literally one instruction wide! A signal must be delivered after
%rsp
has been changed, but before the next instruction loads
%rip
. Several simple instructions like this can be run per cycle on a modern super-scalar out-of-order CPU, so the race window is
roughly a hundred picoseconds.
When we found this race, our first reaction was that it must be too rare to explain the observed crash rate. We were seeing more than a dozen return-to-null crashes per day across the fleet. Could a one-instruction race during exception cleanup really account for that?
We turned to Fermat estimation. If the vulnerable window is on the order of
1
0
−
10
10^{-10}
1
0
−
10
seconds and SIGUSR2 arrives every
1
0
−
2
10^{-2}
1
0
−
2
seconds of CPU time, then each exception cleanup handler or catch block has a roughly
1
0
−
8
10^{-8}
1
0
−
8
probability of losing the race.
Rockset uses exceptions as part of its internal ingest backpressure mechanism. A single overloaded host can throw on the order of
1
0
4
10^{4}
1
0
4
exceptions per second. That implies the mean time between failures of a host using backpressure is
1
0
4
10^{4}
1
0
4
seconds, or one crash every few hours. At fleet scale, that is more than enough to explain the observed crash frequency.
Why did the libunwind bug appear now?
The GNU libunwind bug is old—more than 18 years old, present in the first
x86_64
version that supported C++ exception unwinding.
So why did it show up now?
The crash rate is roughly proportional to how many exceptions are thrown and how many signals are delivered. It’s also dependent on how much stack the signal handler consumes.
Rockset is unusual on all three axes. We throw exceptions at high rates as part of normal overload control; we deliver
SIGUSR2
unusually often because of
coarse_thread_cputime_clock
; and earlier this year we made the
SIGUSR2
handler use more stack by adding a call to
timer_getoverrun
, so we could account for merged signals.
That last change seems to have been important. If the handler uses little enough stack, it may not reach and overwrite the stale
ucontext_t
memory. Before that change, we do not observe these crashes at all. After the change the rate remained low until we ramped up load for some use cases that stressed the backpressure mechanism.
In other words, the libunwind bug has always been there, but the product of our exception rate, signal rate, and handler stack usage had only recently crossed the threshold where it became operationally visible.
This mechanism also explains the coincidence that both the hardware bug and the libunwind bug crashed mostly inside
DocumentTree::updateDocument
. Crashes from libunwind were heavily biased toward this method, because it’s always active at the point we throw an exception to apply ingest backpressure. It was also heavily selected for the
%rsp
-misalignment crashes because the bad hardware node was of a SKU that we use for bulk ingest, which spends the majority of its CPU time in that method.
Our immediate mitigation was to switch from GNU libunwind to libgcc’s unwinder. That was a good trade on its own: libgcc’s implementation has benefited from a lot of work to reduce lock contention, which matters when scaling to large VMs.
We also upstreamed a self-contained reproducer and a
fix
⁠
(opens in a new window)
to GNU libunwind, and verified that the other unwinders don’t have a similar issue.
The power of a population-level diagnosis
This debugging journey taught us a lot about the specific details of dynamic linking, DWARF unwind metadata, Linux signal delivery, the System V ABI, and C++ exception machinery. But the main lesson was simpler than any of that.
The most important step was not the clever assembly reading or deep knowledge of the details. It was building a high-quality data set. In the absence of this data set, we were mixing two distinct phenomena into one story and trying to reason our way out of the confusion. Once we had accurate and complete population data, the structure of the problem became obvious: one crash population belonged to a bad host, and the other belonged to a race in libunwind. Once the data got better, the debugging got easier.
For infrastructure systems like Rockset, that matters a lot. This investigation reinforced our commitment to deep instrumentation, automated investigations, and continual improvements in our operational tooling. Reliability is not just about fixing bugs after they happen – it’s about building the data, workflows, and skills that turn impossible problems into diagnosable and solvable ones.
2026
Author
OpenAI
Author
By Nathan Bronson, Member of Technical Staff
Keep reading
View all
Building self-improving tax agents with Codex
Engineering
May 27, 2026
Building a safe, effective sandbox to enable Codex on Windows
Engineering
May 13, 2026
Supercomputer networking to accelerate large scale AI training
Engineering
May 5, 2026
Research
Research Index
Research Overview
Economic Research
Latest Advancements
GPT-5.5
GPT-5.4
GPT-5.3 Instant
Safety
Safety Approach
Deployment Safety
(opens in a new window)
Security & Privacy
Trust & Transparency
Products
ChatGPT
(opens in a new window)
ChatGPT Business
(opens in a new window)
ChatGPT Enterprise
(opens in a new window)
ChatGPT for Education
(opens in a new window)
Codex
Release Notes
API Platform
Overview
API Log In
(opens in a new window)
Docs
(opens in a new window)
Business
Overview
Solutions
Resources
Customer Stories
Partner Network
Contact Sales
Developers
Apps SDK
(opens in a new window)
Open Models
Docs
(opens in a new window)
Resources
(opens in a new window)
Developer Forum
(opens in a new window)
Company
About Us
Our Charter
Careers
News
Support
Help Center
(opens in a new window)
More
Stories
Academy
Livestreams
Podcast
RSS
Terms & Policies
Terms of Use
Privacy Policy
Other Policies
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
OpenAI © 2015–2026
Your privacy choices
English
United States
