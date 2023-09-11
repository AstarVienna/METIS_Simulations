# METIS_Simulations
Scripts for simulating METIS with ScopeSim.

In particular, simulations for
* The METIS-PIP delivery to ESO.
* To develop/test/validate the pipeline.
* Science case simulations.

These can overlap, but don't necessarily have too.

The idea is to store the (Python) scripts to create the simulations in this repository, not (necessarily) the simulated data itself.

## METIS Science Cases

[E-REP-ETH-MET-1014 METIS Science Case](https://polarion.astron.nl/polarion/#/project/METIS/workitem?id=METIS-6935) describes the METIS science cases ([v2, FDR](https://tc.astron.nl:3000/#/com.siemens.splm.clientfx.tcui.xrt.showObject?uid=wFOAQ1RjYbaBBD), [v1, PDR](https://tc.astron.nl:3000/#/com.siemens.splm.clientfx.tcui.xrt.showObject?uid=SjOAAxgkYbaBBD)).

Ralf presents 8 cases in his document referring to v1.0 where some information on the simulation and input data are given in the respective figure captions:

1. LMN imaging: Herbig Ae star protoplanetary disk  - v1.0 Fig 2-3, in v2.0 not more mentioned
2. HCI extended source imaging: eta CVR debris disk – v1.0 Fig. 2-12, v2.0 Fig 2-15
3. HCI point source imaging: Earth-twin around alpha Cen A – v1.0 Fig 3-7, v2.0 updated simulation Fig 3-9
4. LSS LM: comet 8P/Tuttle – v1.0 Fig 4-1 = v2.0 Fig 4-1
5. LSS N: QSO 3C249.1 – not covered, neither in v1.0 nor in v2.0
6. LMS: HD100546 disk – v1.0 Fig 2-7, in v2.0 not more mentioned
7. HCI LMS: Earth-twin around Proxima B – v1.0 Fig 3-9 = v2.0 Fig 3-8
8. HCI LMS extended: hot Jupiter Tau Bootis b – v1.0 Fig 3-5 = v2.0 Fig 3-5


There are a couple of things which need to be checked before starting any work:

- why have been some cases been dropped in v2.0 FDR version
- None of these cases have been simulated with SimMETIS, input data are heterogeneous some come obviously from simulations some are observations from other instruments given only as example but are not simulated METIS observations. It is unclear how suitable they are as input for ScopeSim for our purpose.

 
