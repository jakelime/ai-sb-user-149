# Production and Planning Control System

## Quickstart

If you are working inside `GCP workbench`, then the github SSH connector has
already been set up for you.

```shell
# Run these commands in terminal (jupyter terminal, or from console, or from cells with '!')
git clone git@github.com:jakelime/ai-sb-user-149.git # to clone from the actual repository
git ac "my commit message" # this command will add all, and commit
git push origin main # this will push your updates to the repo
git fetch # to sync with online repo
git pull # to pull down the latest changes
```

If you want to work using your own private environment, and understood how SSH
keys to github work already, then do these steps.

1. Use SSH to connect git repos, using your own account
1. Get collaborator invite from Jake, to your own account
1. `git clone git@github.com:jakelime/ai-sb-user-149.git`
1. `git add . && git commit -m 'my message'`
1. `git push`


## Get Google working on your local environment



## Objectives

### Main Goals

- To develop a production planning and operations control system
- To design the system with great user experience, smart planning with AI

**In a MRO shop, it is a *Low volume, High mix environment***

- Planning for a MRO job is very tedious due to the dynamic nature, every
  engine is different - some are subjected to mild conditions, others are
  subjected to harsh conditions (more internal damage)
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

## Design Overview

 ![MRO Shop scheduling](docs/images/project_overview.png?raw=true "MRO Shop scheduling")

## Desired output

We would expect the PPCS to be able to generate schedules, which is basically a
`output_table` that looks like this:

|lo_id     |emp_id    |process_code                                |timestamp_in  |timestamp_out |
|----------|----------|--------------------------------------------|--------------|--------------|
|j000000001|st00000001|lpt_major_module-gate010-CUCEAA-binsp       |8/17/07 13:15 |8/17/07 17:19 |
|j000000001|st00000003|lpt_major_module-gate010-CUCEAA-clean       |8/25/07 8:00  |8/25/07 17:30 |
|j000000001|st00000004|lpt_major_module-gate010-CUCEAA-ndtest      |9/15/07 8:00  |9/15/07 21:00 |
|j000000001|st00000007|accessory_drive_module-gate010-CUCKAA-binsp |8/19/07 13:15 |8/19/07 17:47 |
|j000000001|st00000007|accessory_drive_module-gate030-CUCKAA-sbassm|1/30/08 8:52  |1/30/08 17:12 |
|j000000001|st00000017|engine_major-gate010-CUAAAD-binsp           |8/23/07 10:23 |8/23/07 17:30 |
|j000000001|st00000002|engine_major-gate010-CUAAAD-binsp           |8/20/07 8:00  |8/20/07 17:00 |
|j000000001|st00000007|fan_major_module-gate010-CUCJAA-binsp       |8/19/07 8:00  |8/19/07 13:18 |
|j000000001|st00000007|fan_major_module-gate030-CUCJAA-sbassm      |8/22/07 8:49  |8/22/07 17:45 |
|j000000001|st00000024|core_major_module-gate010-CUCBAA-binsp      |8/19/07 8:00  |8/19/07 21:00 |
|j000000001|st00000023|core_major_module-gate010-CUCBAA-clean      |8/21/07 8:00  |8/21/07 17:00 |
|j000000001|st00000050|others-gate022-CTAAAA-eiclean               |9/11/07 11:27 |9/11/07 17:00 |
|j000000001|st00000053|others-gate022-CVAAAA-eiinsp                |7/12/08 13:25 |7/12/08 15:42 |
|j000000001|st00000050|others-gate022-CVAAAA-eirepr                |9/13/07 10:21 |9/13/07 11:12 |
|j000000001|st00000059|core_major_module-gate022-CUBPAA-eatest     |9/15/07 8:00  |9/15/07 11:34 |
|j000000001|st00000059|core_major_module-gate022-CUBPAA-eatest     |9/14/07 8:00  |9/14/07 18:05 |
|j000000001|st00000069|engine_major-gate030-CUAAAA-enassm          |12/16/07 17:01|12/16/07 20:00|
|j000000001|st00000042|core_major_module-gate030-CUCAAA-hsgrnd     |5/31/08 8:00  |5/31/08 15:41 |
|j000000001|st00000072|fan_major_module-gate010-CUAXAA-inspt       |8/23/07 16:15 |8/23/07 18:28 |

A process/task would be assigned to `machine` and `man` required the get the job done.

### Visualization

To visualize, we can make use of a `gantt chart`.

Chart by job tasks:

 ![Gantt chart of a Job](docs/images/gantt-by_job_tasks.png?raw=true "Gantt chart of a Job")

Chart by manpower:

 ![Manpower assignment chart](docs/images/gantt-by_man.png?raw=true "Gantt chart of Manpower")

From the `manpower chart` above, we can see that there are opportunities to optimize manpower
better - by filling up the gaps between the assigned tasks.

## Details

### Shopfloor

Each `process` (also known as `task`) can be done only using specific machines, only using
specific manpower trained for the task.

Given a `process_code`, use `db_shopfloor table` to map the required shopfloor resources.

|process_code|manhour_required_mean|machine_ids                                 |
|------------|---------------------|--------------------------------------------|
|accessory_drive_module-gate010-CUCKAA-binsp|9.157281746031746    |BSBAY01; BSBAY02; BSBAY03; BSBAY04          |
|core_major_module-gate010-CUBFAA-binsp|11.437521367521366   |BSBAY01; BSBAY02; BSBAY03; BSBAY04          |
|core_major_module-gate021-CUBGAA-rprpntg|10.680277777777777   |PLSMBAY01; PLSMBAY02; PLSMBAY03; PLSMBAY04; PLSMBAY05; PLSMBAY06|
|fan_major_module-gate021-CUAVAA-rprndt|10.950444444444445   |DARKRM01; DARKRM02; DARKRM03; DARKRM04; DARKRM05; DARKRM06; DARKRM07|
|fan_major_module-gate021-CUAVAA-rprsmtl|107.96520833333334   |RPRCELL01; RPRCELL02; RPRCELL03; RPRCELL04; RPRCELL05; RPRCELL06; RPRCELL07; RPRCELL08|
|fan_major_module-gate021-CUAVAA-rprpltg|21.072314814814813   |ELECTNK01; ELECTNK02; ELECTNK03; ELECTNK04; ELECTNK05|
|others-gate021-CUAJAA-rprweld|196.58774074074074   |RPRCELL01; RPRCELL02; RPRCELL03; RPRCELL04; RPRCELL05; RPRCELL06; RPRCELL07; RPRCELL08|
|others-gate022-CXAAAA-eaclean|10.1103125           |CLNTK01; CLNTK02; CLNTK03; CLNTK04; CLNTK05 |

### Manpower

#### Manpower to shift and skills table

Given a `process_code`, use `db_manpower table` to map the workers capable of performing the task.

|emp_id    |workshift |process_code                                |
|----------|----------|--------------------------------------------|
|st00000042|NORM      |core_major_module-gate030-CUCAAA-balnc;engine_major-gate030-CUAAAA-balnc;core_major_module-gate030-CUCAAA-hsgrnd;core_major_module-gate030-CUBFAA-hsgrnd|
|st00000099|NORM      |accessory_drive_module-gate021-CUCLAA-rprmach;accessory_drive_module-gate021-CUCLAA-rprsmtl;lpt_major_module-gate021-CUCDAA-rprwtjt|
|st00000070|NORM      |core_major_module-gate021-CUBQAA-rprinsp;others-gate021-CUAJAA-rprinsp;accessory_drive_module-gate021-CUCKAA-rprinsp|
|st00000087|NORM      |fan_major_module-gate021-CUAXAA-rprcln;fan_major_module-gate021-CUAXAA-rprsurft;fan_major_module-gate021-CUCJAA-rprmach|
|st00000101|NORM      |lpt_major_module-gate021-CUCEAA-rprmach;engine_major-gate021-CUAAAA-rprplsm;fan_major_module-gate999-CUAXAA-suppt|
|st00000015|DS        |core_major_module-gate010-CUBGAA-ndtest;fan_major_module-gate010-CUAXAA-ndtest;lpt_major_module-gate021-CUCEAA-rprndt;core_major_module-gate021-CUBPAA-rprndt;others-gate022-CUAJAA-eaclean;others-gate021-DBAAAA-rprndt|
|st00000024|DS        |core_major_module-gate010-CUCBAA-binsp;core_major_module-gate010-CUBFAA-binsp;core_major_module-gate010-CUBPAA-binsp;core_major_module-gate010-CUBFAA-utstrip;core_major_module-gate010-CUCBAA-utstrip|
|st00000060|DS        |engine_major-gate030-CUAAAA-entest;engine_major-gate030-CUAAAA-testderg|
|st00000120|DS        |core_major_module-gate030-CUBFAA-sbassm     |
|st00000104|DS        |fan_major_module-gate021-CUAXAA-rprweld     |
|st00000098|NS        |core_major_module-gate021-CUBGAA-rprmach;core_major_module-gate021-CUCBAA-rprplsm;core_major_module-gate021-CUBPAA-rprplsm;lpt_major_module-gate021-CUCDAA-rprplsm|
|st00000108|NS        |lpt_major_module-gate021-CUCCAA-rprplsm;fan_major_module-gate021-CUAWAA-rprplsm|
|st00000112|NS        |core_major_module-gate021-CUCAAA-rprplsm;lpt_major_module-gate021-CUCEAA-rprplsm|
|st00000091|NS        |core_major_module-gate021-CUBPAA-rprpntg;engine_major-gate021-CUAAAA-rprpntg|
|st00000085|NS        |core_major_module-gate021-CUCBAA-rprmach;core_major_module-gate021-CUBHAA-rprmach|
|st00000106|NS        |others-gate021-CSAAAA-rprpntg;core_major_module-gate021-CUBGAA-rprpntg|

The `process_code` column lists all the capable skill of that worker, separated by `;`.

#### Shift table

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
