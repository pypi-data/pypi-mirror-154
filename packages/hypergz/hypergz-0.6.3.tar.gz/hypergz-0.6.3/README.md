# Installation
``` sh
$ pip install hypergz
```

-----------

<h1> Try the algorithm </h1>

To run your own example click [here](http://amitsheer.pythonanywhere.com/)

-----------

<h1> Introuction </h1>
This repository is an implementation of two algorithms:
<h2> 1) Force-Directed Graph Drawing Using Social Gravity and Scaling </h2>
Link for atricle: https://arxiv.org/pdf/1209.0748.pdf

Authors: 
  - Michael J. Bannister
  - David Eppstein
  - Michael T. Goodrich
  - Lowell Trott

This algorithm creates a pleasant drawing of a _graph_ in a shape of a circle using attraction and rejection forces as well as social.

This algorithm offers 3 methods of social gravity:

  - _Centrality by clossness:_ The closer a vertex is to other vertices the more central it will be.
  - _Centrality by betweeness:_ Vertex who is part of more shortest paths will be more central.
  - _Centrality by degree:_ Vertex with higher degree will be more central.
 
 <h3> Example of different centralities in tree graph </h3>

| Networkx | Clossness |
| ------------- | ------------- |
| <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173134761-2e94912a-471b-4ed2-9f76-f09bfb31cff8.png"/></p>  | <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173134856-da240d0e-fa77-4545-bfcb-4d68d932e88a.png"/></p>  |

| Betweeness | Degree |
| ------------- | ------------- |
| <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173134909-6a92e31e-6ca3-4c01-9c58-264f64ee2077.png"/></p>  | <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173134954-3b4820a2-ac2d-4a7d-94c2-e7febfa6cbeb.png"/></p>  |

<h2> 2) Hypergraph Drawing by Force-Directed Placement </h2>
Link for atricle: https://www.researchgate.net/publication/318823299_Hypergraph_Drawing_by_Force-Directed_Placement

Authors: 
  - Naheed Anjum Arafat
  - Stephane Bressan

This algorithm creates a pleasant drawing of a _hyper-graph_ using any force-directed algrithm.
We implemnted with the first algoritm.
This algorithm offers 4 methods of converting hyper-graph to a graph (to apply force-directed algorithm on):
  - _Complete graph_: connecting all vertices with all vertices.
  - _Cycle graph_: connecting each vertex to the next vertex.
  - _Star graph_: connecting all vertices to their center of Mass.
  - _Wheel graph_: union of the _Cycle_ and the _Star_ graphs.
  
 <h3> Example of different graphs </h3>

| Complete | Cycle | Betweeness | Degree |
| ------------- | ------------- | ------------- | ------------- |
| <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173139564-b3678721-5bb2-4911-b5ef-8a12c33e3fb2.png"/></p>  | <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173139724-585d2cd5-f741-48b5-81b7-c5f1ea90fa48.png"/></p>  | <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173139829-92926912-673a-4ae7-981a-e8abd29a1db8.png"/></p>  | <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173139911-ff300e17-5590-4117-b510-8d540b4fea7b.png"/></p>  |

 <h3> Example of hyper-graph with 10 vertices and 8 hyper-edges </h3>

| Complete | Cycle |
| ------------- | ------------- |
| <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173141603-a3d4c2c8-a055-46da-81f5-7fe2a4c96b91.png"/></p>  | <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173141670-b385241a-e319-4690-baf2-f2585df90115.png"/></p>  |

| Betweeness | Degree |
| ------------- | ------------- |
| <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173141748-caf4f22a-163d-42e0-b75e-551a23d72c7b.png"/></p>  | <p align="center"><img src="https://user-images.githubusercontent.com/69470263/173141799-cdeeb944-b37b-48ab-ab18-1bfb9d4954d7.png"/></p>  |

-----------
The team:
  - [Amit Sheer Cohen](https://github.com/AmitSheer)
  - [Neta Roth](https://github.com/neta-r)

