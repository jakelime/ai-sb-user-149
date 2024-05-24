# Production and Planning Control System

## Objectives

### Main Goal

- To develop a production planning and operations control system
- To design the system with great user experience, smart planning with AI

**In a MRO shop, it is a *Low volume, High mix environment***

- Planning for a MRO job is very tedious due to the dynamic nature, every
  engine is different - some are subjected to mild conditions, others are subjected to very harsh conditions (more internal damage)
- A typical repair job consist of these processes - Strip, Repair, Build
- Resources are constraints. Typical resources are manpower, spare parts,
  machine availbility.

### The General Idea

- To use GCP `OR-Tools` such as the optimizer to determine the best
  way to schedule and plan for the tasks and resource allocation

Because of the highly complex multivariate relation, it is difficult
for humans to interface with the tool and/or understand the input/output required.

- To leverage AI technology, such as LLM to serve as a interface from human
  to the optimizer, such that the human can dynamically adjust planned schedules.

## Overview

 ![MRO Shop scheduling](docs/images/project_overview.png?raw=true "MRO Shop scheduling")

## Details

### Manpower

The company employ a 3-shift system, which can be obtained in the `shift_table`.

| shift_code | shift_description | shift_start_hour | shift_end_hour | shift_days                                   |
|------------|-------------------|------------------|----------------|----------------------------------------------|
| N          | normal shift      | 0800H            | 1730H          | Monday; Tuesday; Wednesday; Thursday; Friday |
| DS         | day shift         | 0700H            | 1630H          | Monday; Tuesday; Wednesday; Thursday; Friday |
| NS         | night shift       | 1600H            | 0130H          | Monday; Tuesday; Wednesday; Thursday; Friday |

**Accoding MOM laws:**

A defined shift (N,DS,NS) adhere's to requirements of 44hours a week.

A worker is allowed to OT, but capped at 72 OT hours a month. All
weekends are considered as OT hours and require 1.5x basic salary.

There must be 1 rest day a week.

For shift workers, the rest day can be a continuous period of 30 hours.
A 30-hour rest period that starts before 6pm on a Sunday is considered
as 1 rest day within the week, even if it extends into the Monday of
the following week.

A week is continuous period of 7 days starting from Monday and ending on Sunday.

Other than the rest day, the other days of the week which you don’t need
to work are not considered rest days.

If the worker is required to work on rest day,

 **If work is done**       | **For up to half your normal daily working hours** | **For more than half your normal daily working hours** | **Beyond your normal daily working hours**
---------------------------|----------------------------------------------------|--------------------------------------------------------|--------------------------------------------
 At the employer’s request | 1 day’s salary                                     | 2 days’ salary                                         | 2 days’ salary \+ overtime pay
 At the employee’s request | Half day’s salary                                  | 1 day’s salary                                         | 1 day’s salary \+ overtime pay
