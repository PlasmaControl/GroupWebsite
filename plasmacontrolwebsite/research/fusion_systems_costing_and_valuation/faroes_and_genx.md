# FAROES and GenX

We need to optimize fusion reactors for their roles in future electricity markets.
There are two complementary efforts: one of fusion systems optimization and costing, and the other on a valuation of fusion for electricity systems.

## FAROES: Fusion Analysis, Research, and Optimization for Energy Systems

FAROES is an open-source fusion systems and costing code, written in python. It allows a user to optimize a reactor for a specified objective subject to physics and engineering constraints. It also includes a costing module for estimating the capital cost, variable cost, and LCOE for a fusion plant.

FAROES presently includes a steady-state tokamak model, which was used to study the influence of triangularity on plant economics, but modules could be built to support other reactor types.

FAROES is available at [github.com/PlasmaControl/faroes](https://github.com/PlasmaControl/faroes).

## Fusion valuation for a decarbonized US electricity market

In collaboration with Jesse Jenkins’ ZERO Lab, we implemented an operational model of a fusion reactor in the open-source electricity systems code GenX. We used this to study the value of fusion for a future decarbonized US Eastern Interconnection.

This model, or extensions of it, could be used for a wealth of future studies: with greater operational details, in new markets, with more detailed fusion build-out timelines, and so on.