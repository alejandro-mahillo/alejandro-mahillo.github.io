---
title: "Discrete variational calculus for accelerated optimization"
collection: publications
category: manuscripts
permalink: /publication/2023-01-23-discrete-variational-calculus
excerpt: "We introduce variational integrators using Hamilton’s and Lagrange-d’Alembert’s principle to derive optimization methods generalizing Polyak’s heavy ball and Nesterov’s accelerated gradient."
date: 2023-01-23
venue: "Journal of Machine Learning Research (JMLR)"
paperurl: "https://jmlr.org/papers/v24/21-1323.html"
citation: "Campos, C.M., Mahillo, A., Martín de Diego, D. (2023). Discrete variational calculus for accelerated optimization. J. Mach. Learn. Res., 24(25), 1–33."
---

Many of the new developments in machine learning are connected with gradient-based optimization methods. Recently, these methods have been studied using a variational perspective (Betancourt et al., 2018). This has opened up the possibility of introducing variational and symplectic methods using geometric integration. 

In particular, in this paper, we introduce variational integrators (Marsden and West, 2001) which allow us to derive different methods for optimization. Using both Hamilton’s and Lagrange-d’Alembert’s principle, we derive two families of optimization methods in one-to-one correspondence that generalize Polyak’s heavy ball (Polyak, 1964) and Nesterov’s accelerated gradient (Nesterov, 1983), the second of which mimics the behavior of the latter reducing the oscillations of classical momentum methods. 

However, since the systems considered are explicitly time-dependent, the preservation of symplecticity of autonomous systems occurs here solely on the fibers. Several experiments exemplify the result.