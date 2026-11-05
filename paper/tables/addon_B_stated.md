# Add-on B: does the agent follow the stated line whatever the name?

Exploratory, added after the main results were seen. The 40 core names on the 8 twin tasks; the S0 request says "I want the men's version." or "I want the women's version." for every name, so name gender is crossed with the stated line. Cell: wrong-line rate = share of purchases that were the other gendered version, 95% Wilson interval (wrong/purchases); then the episodes that ended without a purchase, split into no purchase (the agent chose not to buy) and invalid product (the agent tried to buy an id that is not on the page). **Bold** = mismatch cells (the stated line differs from the name's usual gender reading). A name-driven override would show up as a higher rate there.

## Claude Haiku 5.5

| Names | Asked for the men's version | Asked for the women's version |
|---|---|---|
| Men's names | 1.90% [1.09, 3.29] (12/631); no purchase 9/640, invalid product 0/640 | **1.12% [0.55, 2.30] (7/623); no purchase 11/640, invalid product 6/640** |
| Women's names | **1.62% [0.88, 2.96] (10/616); no purchase 24/640, invalid product 0/640** | 0.49% [0.17, 1.42] (3/615); no purchase 15/640, invalid product 10/640 |

- asked for men's, women's minus men's names: -0.3 pts [-1.7, +1.0], q .749
- asked for women's, women's minus men's names: -0.6 pts [-1.6, +0.3], q .390

## GPT-6 Luna (partial run: 190 of 2,560 episodes, 187 bought, descriptive only, not tested)

| Names | Asked for the men's version | Asked for the women's version |
|---|---|---|
| Men's names | 0.00% [0.00, 7.87] (0/45); no purchase 0/45, invalid product 0/45 | **0.00% [0.00, 7.87] (0/45); no purchase 0/45, invalid product 0/45** |
| Women's names | **0.00% [0.00, 7.00] (0/51); no purchase 0/51, invalid product 0/51** | 0.00% [0.00, 7.71] (0/46); no purchase 0/46, invalid product 0/46 |

