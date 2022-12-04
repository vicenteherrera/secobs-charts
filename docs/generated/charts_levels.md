[Go to root documentation](https://vicenteherrera.com/secobs-charts)  
[Go to index of charts evaluation](https://vicenteherrera.com/secobs-charts/docs/generated/charts_levels)

## Artifact Hub's Helm charts evaluation

Source: [Artifact Hub](https://artifacthub.io/)  
Evaluation date: 2022-12-04, 09:00:21

### Pod Security Standards (PSS)

[Pod Security Standards (PSS)](https://kubernetes.io/docs/concepts/security/pod-security-standards/) define three levels of security (restricted, baseline and privileged) that can be enforced for pods in a namespace. Evaluation done with [psa-checker](https://vicenteherrera.com/psa-checker/) command line tool, that checks into Kubernetes objects that can create pods.

| Category | Quantity | Percentage |
|------|------|------|
| Total | 10 | 100.0% |
| Privileged | 3 | 30.0% |
| Baseline | 2 | 20.0% |
| Restricted | 0 | 0.0% |
| Error_download | 0 | 0.0% |
| Error_template | 0 | 0.0% |
| Empty_no_object | 3 | 30.0% |
| Version_not_evaluable | 2 | 20.0% |

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
| Non-evaluable | 2 |
| No workload | 1 |
| [0, -50) | 5 |
| [-50, -100) | 1 |
| [-100, -150) | 1 |
| [-150, -200) | 0 |
| [-200, -250) | 0 |
| [-250, -300) | 0 |
| [-300, -350) | 0 |
| [-350, -400) | 0 |
| [-400, -450) | 0 |
| [-450, -500) | 0 |
| [-500, -550) | 0 |
| [-550, -600) | 0 |
| [-600, -650) | 0 |
| [-650, -700) | 0 |

### Charts list

Alphabetical list of all repositories (number of charts in parenthesis):

[main](./charts_levels)&nbsp; [A(2)](./charts_levels_a)&nbsp; [B(0)](./charts_levels_b)&nbsp; [C(1)](./charts_levels_c)&nbsp; [D(0)](./charts_levels_d)&nbsp; [E(0)](./charts_levels_e)&nbsp; [F(1)](./charts_levels_f)&nbsp; [G(1)](./charts_levels_g)&nbsp; [H(0)](./charts_levels_h)&nbsp; [I(0)](./charts_levels_i)&nbsp; [J(0)](./charts_levels_j)&nbsp; [K(0)](./charts_levels_k)&nbsp; [L(0)](./charts_levels_l)&nbsp; [M(0)](./charts_levels_m)&nbsp; [N(0)](./charts_levels_n)&nbsp; [O(2)](./charts_levels_o)&nbsp; [P(0)](./charts_levels_p)&nbsp; [Q(0)](./charts_levels_q)&nbsp; [R(0)](./charts_levels_r)&nbsp; [S(3)](./charts_levels_s)&nbsp; [T(0)](./charts_levels_t)&nbsp; [U(0)](./charts_levels_u)&nbsp; [V(0)](./charts_levels_v)&nbsp; [W(0)](./charts_levels_w)&nbsp; [X(0)](./charts_levels_x)&nbsp; [Y(0)](./charts_levels_y)&nbsp; [Z(0)](./charts_levels_z)&nbsp; 