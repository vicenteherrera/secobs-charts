[Go to root documentation](https://vicenteherrera.com/secobs-charts)  
[Go to index of charts evaluation](https://vicenteherrera.com/secobs-charts/docs/generated/charts_levels)

## Artifact Hub's Helm charts evaluation

Source: [Artifact Hub](https://artifacthub.io/)  
Evaluation date: 2022-12-07, 18:31:10

### Pod Security Standards (PSS)

[Pod Security Standards (PSS)](https://kubernetes.io/docs/concepts/security/pod-security-standards/) define three levels of security (restricted, baseline and privileged) that can be enforced for pods in a namespace. Evaluation done with [psa-checker](https://vicenteherrera.com/psa-checker/) command line tool, that checks into Kubernetes objects that can create pods.

| Category | Quantity | Percentage |
|------|------|------|
| Total | 9278 | 100.0% |
| Privileged | 779 | 8.4% |
| Baseline | 4806 | 51.8% |
| Restricted | 42 | 0.45% |
| Error_download | 408 | 4.4% |
| Empty_no_object | 187 | 2.02% |
| Error_template | 1006 | 10.84% |
| No_pod_object_but_crd | 1340 | 14.44% |
| No_pod_object | 191 | 2.06% |
| Version_not_evaluable | 519 | 5.59% |

Legend:
 * PSS level:
   * Privileged: Pod specs makes use of privileged settings, the most insecure. Containers are able to access host capabilities.
   * Baseline: Pod specs without extra security or extra privileges. Doesn't account for CRD that may create pods.
   * Restricted: Pod specs follow the best security practices, like requiring containers to not run as root, and drop extra capabilities. Doesn't account for CRDs that may create pods.
 * Error_download: Downloading the template from original source wasn't possible.
 * Error_template: Rendering the template without providing parameters resulted in error.
 * No_pod_object_but_crd: The chart didn't render any object that can create pods, but has CRD that could do so.
 * No_pod_object_no_crd: The chart didn't render any object that can create pods nor CRDs.
 * Version_not_evaluable: The cart includes deployment, daemonset, etc. of v1beta1 that can't be evaluated by the library.

### Operator evaluation with BadRobot score

[BadRobot](https://github.com/controlplaneio/badrobot) evaluates how secure Kubernetes operators are. For each operator included in a chart, a score is calculated with a set of security practices. The closer to zero the score, the better.

| Score | Number of charts |
|------|------|
| Non-evaluable | 1414 |
| Blank score | 167 |
| No workload | 0 |
| Score == 0 | 2538 |
| [0, -50) | 7175 |
| [-50, -100) | 383 |
| [-100, -150) | 85 |
| [-150, -200) | 26 |
| [-200, -250) | 14 |
| [-250, -300) | 7 |
| [-300, -350) | 3 |
| [-350, -400) | 1 |
| [-400, -450) | 1 |
| [-450, -500) | 0 |
| [-500, -550) | 1 |
| [-550, -600) | 0 |
| [-600, -650) | 0 |
| [-650, -700) | 1 |

### Charts list

Alphabetical list of all repositories (number of charts in parenthesis):

[main](./charts_levels)&nbsp; [A(1415)](./charts_levels_a)&nbsp; [B(473)](./charts_levels_b)&nbsp; [C(1009)](./charts_levels_c)&nbsp; [D(424)](./charts_levels_d)&nbsp; [E(233)](./charts_levels_e)&nbsp; [F(273)](./charts_levels_f)&nbsp; [G(552)](./charts_levels_g)&nbsp; [H(240)](./charts_levels_h)&nbsp; [I(228)](./charts_levels_i)&nbsp; [J(181)](./charts_levels_j)&nbsp; [K(440)](./charts_levels_k)&nbsp; [L(235)](./charts_levels_l)&nbsp; [M(400)](./charts_levels_m)&nbsp; [N(203)](./charts_levels_n)&nbsp; [O(481)](./charts_levels_o)&nbsp; [P(468)](./charts_levels_p)&nbsp; [Q(15)](./charts_levels_q)&nbsp; [R(361)](./charts_levels_r)&nbsp; [S(839)](./charts_levels_s)&nbsp; [T(194)](./charts_levels_t)&nbsp; [U(37)](./charts_levels_u)&nbsp; [V(99)](./charts_levels_v)&nbsp; [W(388)](./charts_levels_w)&nbsp; [X(2)](./charts_levels_x)&nbsp; [Y(58)](./charts_levels_y)&nbsp; [Z(30)](./charts_levels_z)&nbsp; 