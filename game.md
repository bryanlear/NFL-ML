# Sports Analytics 
## Classic Bradley-Terry Model
    This model assumes each team/player has one scalar ability.

### Probability Model
    This model specifies the data-generating mechanism *before any data is observed

$\text{Schedule} = \{\,\text{opponent}_1,\ \text{opponent}_2,\ \dots,\ \text{opponent}_n \,\}$

**Schedule**: list of opponents a team plays and the order/timing of those games during a season. *Strength and composition of opponents in set of games*

Win percentage then becomes a function of schedule strength - **NOT** just team quality.

When opponent's strength is high then expected $probability * game^{-1}$ decreases (even for a strong team).
A team's win percentage reflects *matchup* - no absolute quality.

Let team strength be $\theta_i$.\
Let opponent strength be $\theta_j$.\
Then expected win probability in **Bradley-Terry** formulation is:

$P(i\succ j) = \frac{e^{\theta_i}}{e^{\theta_i} + e^{\theta_j}}$

*log-odds depend on $\theta_i - \theta_j$*

If strong team (high $\theta_i$) plays mostly high $\theta_j$ teams, then **every** game has lower $P(win)$, therefore *mean* win percentage over the schedule is lower

In log-scale define: 

$\beta_i=log(\theta_i)$

which yields logistic form:

$P(i\succ j) = \frac{e^{\theta_i}}{e^{\theta_i} + e^{\theta_j}} = \sigma(\beta_i-\beta_j)$

where, 
$\sigma(x) = \frac{1}{1+e^{-z}}$ is **logistic function**

Thus pairwise outcomes factpr thrpugh differences in log-abilities.

In other words, the probability model is a statement about the stochastic structure of outcomes. It defines the probability distribution for a *single* comparison outcome, conditional on $\theta$ and $\beta$.
Does NOT depend on observed data, does NOT produce a function of the parameters to be mazimixed.

---

### Likelihood Function in BT 
    This uses the observed data and treats parameters as unknown quantities whose values are to be inferred

Supposse one observes $w_{ij}$ wins $i$ over $j$ and $w_{ji}$ wins of $j$ over $i$

Then log-likelihood is: 

$\ell(\beta)=
\sum_{i<j}
\left[
w_{ij}(\beta_i - \log(e^{\beta_i}+e^{\beta_j}))
+
w_{ji}(\beta_j - \log(e^{\beta_i}+e^{\beta_j}))
\right]$

Function of parameters $\beta=(\beta_1,...,\beta_n)$ and used to estimate parameters by e.g., maximizing likelihood. Lastly, it aggregfates contribution from **all matches**! $L(\beta|data)$