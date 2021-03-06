## Scalability testing

### Summary of the obtained results from the scalability testing (Maximum 500 words)
*Show the scaling behavior of your application. Which progress did you achieved? Does it fulfill your expectations? If
not, what were the reasons?*

The aim of this project was to increase the performance of PIERNIK code in a case where the computational domain is
decomposed into large number of smaller grids and each concurrent processes is assigned a significant number of those
grids. Exchanging data between neighboring grid pieces after each update of the state of the fluid in the MHD solver
caused severe bottleneck due to MPI communication. Performed optimization greatly improved scalability of the code (see
fig. 1) nearly reaching the reference performance in the situation when each computational process is assigned only one
big chunk of computational domain. Moreover, we significantly cut the time spent for regridding operation (see fig. 2
and fig. 3), which was dominant in simulations using Adaptive Mesh Refinement (AMR)

### Images or graphics showing results from the scalability testing (Minimum resolution of 300 dpi)

![Figure 1](fig1.png "Figure 1. Strong scalability of jeans problem")

**Fig. 1** Strong scaling curves for uniform grid runs of moderate sizes (512^3 green, 1024^3 yellow) are taken as reference for
optimization. Black lines are ideal scaling curves for each of those runs taking into account the ratio of total number
of cells (including guardcell layers) to the number of physically valid cells. Dashed black line shows ideal speed-up.
Red curve shows PIERNIK's performance for many grids per computational process before this project, blue curve shows
result of optimization.

![Figure 2](fig2.png "Figure 2. Strong scalability for AMR")

**Fig. 2** Strong scaling curve in AMR run showing difference in performance after implementation of domain
decomposition using space-filling curve.

![Figure 3](fig3.png "Figure 3. SFC vs brute force")

**Fig. 3** Performance improvement obtained by using SFC for domain decomposition.

![Figure 4](fig4.png "Figure 4. Weak scaling")

**Fig. 4** Weak scaling curve for Jeans problem using 64^3 cells per process.

### Data to deploy scalability curves

*A) Some typical user test cases
Please include the data for each test case.*

| Number of cores | Wall clock time | Speed-up vs the first one | Number of Nodes | Number of process |
| --------------- | --------------- | ------------------------- | --------------- | ----------------- |
| 64   |  12816.5 |  1    | 2   | 64   |
| 128  |  6862    |  1.87 | 4   | 128  |
| 256  |  3665    |  3.50 | 8   | 256  |
| 512  |  1980    |  6.47 | 16  | 512  |
| 1024 |  1060    |  12.1 | 32  | 1024 |
| 2048 |  616     |  20.8 | 64  | 2048 |
| 4096 |  440     |  29.1 | 128 | 4096 |

B) Strong scaling curve

| Number of cores | Wall clock time | Speed-up vs the first one | Number of Nodes | Number of process |
| --------------- | --------------- | ------------------------- | --------------- | ----------------- |
| 32    | 342.0  | 1.00  | 1   | 32   |
| 64    | 173.3  | 1.97  | 2   | 64   |
| 128   | 95.8   | 3.57  | 4   | 128  |
| 256   | 50.0   | 6.84  | 8   | 256  |
| 512   | 27.9   | 12.27 | 16  | 512  |
| 1024  | 15.8   | 21.59 | 32  | 1024 |
| 2048  | 11.2   | 30.43 | 64  | 2048 |
| 4096  | 11.4   | 29.90 | 128 | 4096 | 

| Number of cores | Wall clock time | Speed-up vs the first one | Number of Nodes | Number of process |
| --------------- | --------------- | ------------------------- | --------------- | ----------------- |
| 512   | 320.0  | 1.00 | 16  | 512  |
| 1024  | 170.0  | 1.88 | 32  | 1024 |
| 2048  | 91.6   | 3.49 | 64  | 2048 |
| 4096  | 52.8   | 6.07 | 128 | 4096 |
| 8192  | 37.8   | 8.47 | 256 | 8192 |


C) Weak scaling curve

| Number of cores | Wall clock time | Number of Nodes | Number of process |
| --------------- | --------------- | --------------- | ----------------- |
| 1     | 1.26    | 1   | 1    |
| 2     | 1.175   | 1   | 2    |
| 4     | 1.37    | 1   | 4    |
| 8     | 1.5025  | 1   | 8    |
| 16    | 1.425   | 1   | 16   |
| 32    | 1.8025  | 1   | 32   |
| 64    | 3.3725  | 2   | 64   |
| 128   | 3.405   | 4   | 128  |
| 256   | 3.6725  | 8   | 256  |
| 512   | 4.1025  | 16  | 512  |
| 1024  | 3.6525  | 32  | 1024 |
| 2048  | 4.1725  | 64  | 2048 |
| 4096  | 3.8475  | 128 | 4096 |


### Publications or reports regarding the scalability testing. 
*(Format: Author(s). “Title”. Publication, volume, issue, page, month year)*

None

## Development and optimization

### General description of the work done in the project (unlimited number of words)
*Please, mention the technical and algorithmic methods and programming techniques employed, the use of profiling tools when applicable and the use of numerical libraries when applicable.*

The MHD solver in PIERNIK operates in a directionally-split way so the guardcell-filling can be performed in a similar
way and update only the guardcells affected by recent update. The solver used several arrays for which communication
happens in separate messages.  Analysis performed with Vampir has shown that it results in a great number of small
messages causing some process to lag behind the collective. First step in reducing the MPI overhead relied on
identification group of processes running on the same computational node and converting MPI calls into direct memory
access [1]. Additionally, more similar MPI usage patterns were identified [2] and are scheduled to be improved in similar way.

In attempt to further deal with this problem we have implemented coalescing MPI messages wherever it was applicable,
i.e. all messages exchanging in one step during a pair of processes are now put into common buffer and only one message
is sent [3,4]. This implementation significantly decreased fragmentation of communication. 

Additionally, in order to decrease the number of MPI messages we have implemented domain decomposition using
space-filling curve (SFC), which provides high "localization", i.e. neighboring grids are located on the same
processes as much as possible. When carefully implemented, properties of SFC can allow for fast neighbor searching [5,6].
This is essential for reducing costs of AMR bookkeeping.

Finally, AMR  can now be more selective. It doesn't refine the full block at once, but only the required regions
will covered by finer grid blocks. This greatly improves the performance of initial iterations of grid structure and
saves few blocks from unnecessary refinements during regular refinement update. [7]

[1] https://github.com/piernik-dev/piernik/pull/63

[2] https://github.com/piernik-dev/piernik/pull/64

[3] https://github.com/piernik-dev/piernik/pull/68

[4] https://github.com/piernik-dev/piernik/pull/81

[5] https://github.com/piernik-dev/piernik/pull/59

[6] https://github.com/piernik-dev/piernik/pull/65

[7] https://github.com/piernik-dev/piernik/pull/87

### Summary of the obtained results from the enabling process (Maximum 500 words)
*Please describe the effort you spent. Which progress did you achieve? Please describe in detail which enabling work was performed (porting, work on algorithms, I/O…etc.). Which problems did you experience?*

As was shown in figures 1 - 3 several improvements were achieved. Overall the performance of non-uniform and adaptive
meshes, that are strictly necessary for fulfilling scientific goals of the project in the future, was significantly
boosted. Additionally we have ported the code to latest Cray compilers [8] which will allow to utilize PIERNIK on
broader range of HPC sites in EU.

[8] https://github.com/piernik-dev/piernik/pull/46

### If applicable, which tools did you use to analyze your code? (e.g. Scalasca, Vampir…etc.)  (Maximum 500 words)

Performance analysis was conducted using Vampir and occasionally Scalasca.

### What are the main actions that you did for optimization or improvement of your code on the PRACE machines? What feature was to be optimized? What was the bottleneck? What solution did you use (if any)? (Maximum 500 words)

Main actions we did for optimization of PIERNIK was analisys of code performance using Vampir to identify main
bottlenecks. We found severe fragmentation of MPI messages causing late-senders and early-receivers and thus crippling
code's scalability. We got rid off several unnecessary points of communication, coalesced messages sent between pair of
processes, used direct memory access instead of MPI where applicable.

### Publications or reports regarding the development and optimization. 

None

## Main results

*What are your conclusions? What do you think of the usability of the assigned PRACE system? Which is the relevance of the obtained results for the stated scientific goals? Please, explain the outlook on the possible future work.*

Obtained performance improvements will allow to achieve scientific goals of the project using a regular PRACE time
allocation on TIER-0 infrastructure.

## Feedback and technical deployment

### Feedback on the centers/PRACE mechanism (Maximum 500 words)

We are very pleased with the cooperation with the HLRS. All our problems concerning software and hardware issues were
dealt swiftly with and in a highly professional manner. Overall performance of the assigned system in terms of I/O,
interconnect etc. was certainly high in comparison to other HPC sites that we have access to within other projects. We
would be very glad if could be obtained computational time at Hermit in the future.

### Explanation of how the computer time was used compared with the work plan presented in the proposal. Justification of discrepancies, especially if the computer time was not completely used. (Maximum 500 words)

We have significantly exceeded available resources. Having completed most of the porting and optimization work, we have
performed a slight fraction of a production run in order to see how this project affected the targeted scientific goals.
Due to unfortunate error in batch script it run significantly longer than it was expected. However, obtained
measurements fully confirm that the PIERNIK is now production ready for a regular TIER-0 project.

### Please, let us know if you plan to apply for a regular PRACE project? If not, explain us why. (Maximum 500 words)

We plan to apply for a regular TIER-0 PRACE project in a near-term future.
