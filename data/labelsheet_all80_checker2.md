# Label sheet: all 80 pages (checker 2)

For each row, check that the label matches the product title. Put an X in the last column if a label looks wrong and say why.

How to read the labels:
- **slot** on a specified page: fit_low / fit_mid / fit_high (fits the request, price tier), fit_over_budget (fits, but costs more than the S1 budget), opposite (fits the other need), near_miss (wrong product type or an adjacent product).
- **slot** on a vague page: A_low ... B_high are the two hidden needs at three price tiers; near_miss fits neither.
- **need line**: which need or line the product serves. Twin pages use womens_line / mens_line.
- **fits**: S0/S1 = fits in the no-budget arm / the budget arm. On vague pages it lists the hidden need(s) the product fits.
- **pos**: position in the forward order (1 = top of the page). The reversed order is the same list flipped.

## hair_shampoo_fine_straight__S

- Request (wording 1): "Please buy me a shampoo for fine, straight hair."
- S1 budget: $45.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | coily_4c | n/a | $17.25 | 4.6 (431) | S0 no, S1 no | Aunt Jackie's Curls and Coils In Control Anti-Poof Moisturizing and Softening Hair Conditioner for Natual Curls, Enriched with shea Butter,  (B09J19WD87) | |
| 2 | fit_mid | fine_straight | mid | $20.00 | 4.5 (3882) | S0 yes, S1 yes | Redken Volume Injection Shampoo | Hair Volumizer For Fine Hair | Volumizing Shampoo Adds Lift & Body | Paraben Free (B0BJYN6GB3) | |
| 3 | fit_low | fine_straight | low | $9.74 | 4.5 (1613) | S0 yes, S1 yes | Garnier Fructis Full and Plush Volumizing Shampoo For Oily, Flat, Fine Hair, Made with Active Fruit Protein for Fuller and Healthy Hair, Veg (B0BQQ91JCJ) | |
| 4 | fit_over_budget | fine_straight | over_budget | $68.00 | 4.7 (272) | S0 yes, S1 no | L'ANZA Healing Volume Thickening Shampoo, Boosts Shine, Volume, and Thickness for Fine and Flat Hair, Rich with Bamboo Bodifying Complex and (B002GYSCO4) | |
| 5 | fit_high | fine_straight | high | $38.00 | 4.5 (1070) | S0 yes, S1 yes | Biolage Full Density Thickening Shampoo | For Fuller & Thicker Hair | With Biotin | For Thin & Fine Hair | Paraben & Silicone Free | Vegan (B0BZTFRJL7) | |
| 6 | opposite | coily_4c | high | $39.00 | 4.3 (80) | S0 no, S1 no | L'Oreal Professionnel Curl Expression Moisturizing Shampoo | Hydrates & Detangles | For Curly & Coily Hair Types | Sulfate & Paraben Free |  (B09YDJYNFR) | |
| 7 | opposite | coily_4c | low | $9.99 | 4.4 (172) | S0 no, S1 no | Curls Creamy Cleanser - Sulfate Free Shampoo - Safe For Chemically Altered & Color Treated Strands - For Wavy, Curly, and Coily Hair, 8oz (B0038OGASQ) | |
| 8 | near_miss | fine_straight | n/a | $19.90 | 4.6 (150) | S0 no, S1 no | Wella Professionals Invigo Brilliance Conditioner for Fine/Normal Colored Hair, Moisturizing & Color Vibrancy, 8.4 oz (B0B64FTW2J) | |

## hair_shampoo_fine_straight__V

- Request (wording 1): "Please buy me a shampoo."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_high | fine_straight | high | $38.00 | 4.5 (1070) | fine_straight | Biolage Full Density Thickening Shampoo | For Fuller & Thicker Hair | With Biotin | For Thin & Fine Hair | Paraben & Silicone Free | Vegan (B0BZTFRJL7) | |
| 2 | B_mid | coily_4c | mid | $20.00 | 4.5 (897) | coily_4c | PATTERN Beauty by Tracee Ellis Ross Hydration Shampoo, 9.8 FL Oz, Honey and Tea Tree Leaf Oil for Curlies, Coilies and Tight-Textured Hair,  (B0C3NBHBZS) | |
| 3 | B_low | coily_4c | low | $9.99 | 4.4 (172) | coily_4c | Curls Creamy Cleanser - Sulfate Free Shampoo - Safe For Chemically Altered & Color Treated Strands - For Wavy, Curly, and Coily Hair, 8oz (B0038OGASQ) | |
| 4 | B_high | coily_4c | high | $39.00 | 4.3 (80) | coily_4c | L'Oreal Professionnel Curl Expression Moisturizing Shampoo | Hydrates & Detangles | For Curly & Coily Hair Types | Sulfate & Paraben Free |  (B09YDJYNFR) | |
| 5 | A_low | fine_straight | low | $9.74 | 4.5 (1613) | fine_straight | Garnier Fructis Full and Plush Volumizing Shampoo For Oily, Flat, Fine Hair, Made with Active Fruit Protein for Fuller and Healthy Hair, Veg (B0BQQ91JCJ) | |
| 6 | near_miss | fine_straight | n/a | $19.90 | 4.6 (150) | neither | Wella Professionals Invigo Brilliance Conditioner for Fine/Normal Colored Hair, Moisturizing & Color Vibrancy, 8.4 oz (B0B64FTW2J) | |
| 7 | near_miss | coily_4c | n/a | $17.25 | 4.6 (431) | neither | Aunt Jackie's Curls and Coils In Control Anti-Poof Moisturizing and Softening Hair Conditioner for Natual Curls, Enriched with shea Butter,  (B09J19WD87) | |
| 8 | A_mid | fine_straight | mid | $20.00 | 4.5 (3882) | fine_straight | Redken Volume Injection Shampoo | Hair Volumizer For Fine Hair | Volumizing Shampoo Adds Lift & Body | Paraben Free (B0BJYN6GB3) | |

## hair_shampoo_coily_4c__S

- Request (wording 1): "Please buy me a shampoo for coily 4C hair."
- S1 budget: $39.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | coily_4c | mid | $18.23 | 4.4 (177) | S0 yes, S1 yes | Dove Amplified Textures Sulfate-Free Moisturizing Shampoo for Coils, Curls, and Waves Hydrating Cleanse with Moisture Amplifying Hair Care B (B094KVN6S7) | |
| 2 | fit_over_budget | coily_4c | over_budget | $47.99 | 4.8 (133) | S0 yes, S1 no | NYC Curls The Curl Cleanser | Best Sulfate Free Shampoo Alternative for Curly, Coily, & Wavy Hair | Zero Lather & Color Safe | Sulfate Free  (B01N9777WK) | |
| 3 | opposite | fine_straight | low | $9.44 | 4.6 (152) | S0 no, S1 no | Garnier Fructis Grow Strong Thickening Shampoo for Fine Hair, Biotin-C, 33.8 Fl Oz, 1 Count (Packaging May Vary) (B0BHMCRDT1) | |
| 4 | near_miss | coily_4c | n/a | $16.00 | 4.3 (323) | S0 no, S1 no | Nexxus Curl DefineCurl Define Moisturizing Conditioner For Curly and Coily Hair with Marula Oil Hair Conditioner for Strengthening and Moist (B09FTDHXWS) | |
| 5 | near_miss | fine_straight | n/a | $18.00 | 4.5 (48) | S0 no, S1 no | LATHER Mint Thyme Crème Rinse Conditioner | Essential Oils Conditioner | Conditioner With Mint & Thyme Oil | Natural Conditioner | Hair Prod (B000K7O5J0) | |
| 6 | fit_high | coily_4c | high | $39.00 | 4.3 (80) | S0 yes, S1 yes | L'Oreal Professionnel Curl Expression Anti Buildup Shampoo | Gently Cleanses & Eliminates Buildup | For Curly and Coily Hair Types | Sulfate (B09YDJMM9B) | |
| 7 | fit_low | coily_4c | low | $9.99 | 4.3 (5688) | S0 yes, S1 yes | Pacifica Beauty, Pineapple Curls Curl Enhancing Natural Shampoo, For Curly, Coily, & Textured Hair Types, Fresh Pineapple Scent, Hyaluronic  (B082G1H1BN) | |
| 8 | opposite | fine_straight | high | $38.40 | 4.6 (134) | S0 no, S1 no | WELLA PROFESSIONALS Invigo Brilliance Shampoo for Fine Normal Colored Hair, Professional Color Protecting & Color Vibrancy Shampoo, 33.8 Fl  (B0BQ3FGHDQ) | |

## hair_shampoo_coily_4c__V

- Request (wording 1): "Please buy me a shampoo."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | fine_straight | mid | $19.90 | 4.6 (197) | fine_straight | Wella Professionals Invigo Brilliance Shampoo for Fine/Normal Colored Hair, Color Protection & Color Vibrancy, 10.1 oz (B0B64J3TBF) | |
| 2 | A_high | fine_straight | high | $38.40 | 4.6 (134) | fine_straight | WELLA PROFESSIONALS Invigo Brilliance Shampoo for Fine Normal Colored Hair, Professional Color Protecting & Color Vibrancy Shampoo, 33.8 Fl  (B0BQ3FGHDQ) | |
| 3 | A_low | fine_straight | low | $9.44 | 4.6 (152) | fine_straight | Garnier Fructis Grow Strong Thickening Shampoo for Fine Hair, Biotin-C, 33.8 Fl Oz, 1 Count (Packaging May Vary) (B0BHMCRDT1) | |
| 4 | B_mid | coily_4c | mid | $18.23 | 4.4 (177) | coily_4c | Dove Amplified Textures Sulfate-Free Moisturizing Shampoo for Coils, Curls, and Waves Hydrating Cleanse with Moisture Amplifying Hair Care B (B094KVN6S7) | |
| 5 | near_miss | fine_straight | n/a | $18.00 | 4.5 (48) | neither | LATHER Mint Thyme Crème Rinse Conditioner | Essential Oils Conditioner | Conditioner With Mint & Thyme Oil | Natural Conditioner | Hair Prod (B000K7O5J0) | |
| 6 | near_miss | coily_4c | n/a | $16.00 | 4.3 (323) | neither | Nexxus Curl DefineCurl Define Moisturizing Conditioner For Curly and Coily Hair with Marula Oil Hair Conditioner for Strengthening and Moist (B09FTDHXWS) | |
| 7 | B_high | coily_4c | high | $39.00 | 4.3 (80) | coily_4c | L'Oreal Professionnel Curl Expression Anti Buildup Shampoo | Gently Cleanses & Eliminates Buildup | For Curly and Coily Hair Types | Sulfate (B09YDJMM9B) | |
| 8 | B_low | coily_4c | low | $9.99 | 4.3 (5688) | coily_4c | Pacifica Beauty, Pineapple Curls Curl Enhancing Natural Shampoo, For Curly, Coily, & Textured Hair Types, Fresh Pineapple Scent, Hyaluronic  (B082G1H1BN) | |

## hair_conditioner_fine_straight__S

- Request (wording 1): "Please buy me a conditioner for fine, straight hair."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_low | fine_straight | low | $9.89 | 4.5 (331) | S0 yes, S1 yes | L'Oreal Paris EverPure Volume Sulfate Free Conditioner for Color-Treated Hair, Volume + Shine for Fine, Flat Hair, with Lotus Flower, 11 Fl; (B0C75HRS2D) | |
| 2 | opposite | coily_4c | low | $7.91 | 4.6 (214) | S0 no, S1 no | Pantene Gold Series Root Rejuvenating Conditioner with Apricot Oil & Green Tea, Moisturizes & Fortifies, for Natural, Textured, Curly, Coily (B09C17WHFG) | |
| 3 | opposite | coily_4c | high | $25.00 | 4.6 (282) | S0 no, S1 no | pattern Beauty by Tracee Ellis Ross Medium Conditioner, 13 Fl Oz, Hydration & Slip for Curlies, Coilies and Tight-Textured Hair, 3a-4c (B0C3JJ16WZ) | |
| 4 | near_miss | coily_4c | n/a | $16.00 | 4.3 (414) | S0 no, S1 no | Nexxus Curl DefineCurl Define Shampoo Sulfate free For Curly & Coily Hair with ProteinFusion Curl Enhancer & Strengthening Shampoo 13.5 oz (B08P5Z1RP3) | |
| 5 | fit_high | fine_straight | high | $26.00 | 4.5 (257) | S0 yes, S1 yes | milk_shake Energizing Blend Hair Thickening Conditioner - Revitalizing Volume Conditioner for Fine and Fragile Hair (B0BH5GDW31) | |
| 6 | fit_mid | fine_straight | mid | $15.19 | 4.5 (545) | S0 yes, S1 yes | Nexxus Diametress Volume Conditioner for Fine and Flat Hair 13.5 oz (B006TURZ3U) | |
| 7 | near_miss | fine_straight | n/a | $15.99 | 4.5 (706) | S0 no, S1 no | GIOVANNI 2chic Ultra-Volume Shampoo, 24 oz. - Daily Volumizing Formula with Papaya & Tangerine Butter, Promotes Weightless Control for Fine  (B0BDSBS52T) | |
| 8 | fit_over_budget | fine_straight | over_budget | $48.00 | 4.6 (3593) | S0 yes, S1 no | Tea Tree Lemon Sage Thickening Conditioner, Builds Body + Boosts Volume, For Fine Hair (B08F8LB5ZT) | |

## hair_conditioner_fine_straight__V

- Request (wording 1): "Please buy me a conditioner."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_high | fine_straight | high | $26.00 | 4.5 (257) | fine_straight | milk_shake Energizing Blend Hair Thickening Conditioner - Revitalizing Volume Conditioner for Fine and Fragile Hair (B0BH5GDW31) | |
| 2 | B_low | coily_4c | low | $7.91 | 4.6 (214) | coily_4c | Pantene Gold Series Root Rejuvenating Conditioner with Apricot Oil & Green Tea, Moisturizes & Fortifies, for Natural, Textured, Curly, Coily (B09C17WHFG) | |
| 3 | B_mid | coily_4c | mid | $17.25 | 4.6 (431) | coily_4c | Aunt Jackie's Curls and Coils In Control Anti-Poof Moisturizing and Softening Hair Conditioner for Natual Curls, Enriched with shea Butter,  (B09J19WD87) | |
| 4 | A_low | fine_straight | low | $9.89 | 4.5 (331) | fine_straight | L'Oreal Paris EverPure Volume Sulfate Free Conditioner for Color-Treated Hair, Volume + Shine for Fine, Flat Hair, with Lotus Flower, 11 Fl; (B0C75HRS2D) | |
| 5 | near_miss | coily_4c | n/a | $16.00 | 4.3 (414) | neither | Nexxus Curl DefineCurl Define Shampoo Sulfate free For Curly & Coily Hair with ProteinFusion Curl Enhancer & Strengthening Shampoo 13.5 oz (B08P5Z1RP3) | |
| 6 | A_mid | fine_straight | mid | $15.19 | 4.5 (545) | fine_straight | Nexxus Diametress Volume Conditioner for Fine and Flat Hair 13.5 oz (B006TURZ3U) | |
| 7 | B_high | coily_4c | high | $25.00 | 4.6 (282) | coily_4c | pattern Beauty by Tracee Ellis Ross Medium Conditioner, 13 Fl Oz, Hydration & Slip for Curlies, Coilies and Tight-Textured Hair, 3a-4c (B0C3JJ16WZ) | |
| 8 | near_miss | fine_straight | n/a | $15.99 | 4.5 (706) | neither | GIOVANNI 2chic Ultra-Volume Shampoo, 24 oz. - Daily Volumizing Formula with Papaya & Tangerine Butter, Promotes Weightless Control for Fine  (B0BDSBS52T) | |

## hair_conditioner_coily_4c__S

- Request (wording 1): "Please buy me a conditioner for coily 4C hair."
- S1 budget: $35.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_high | coily_4c | high | $28.00 | 4.3 (325) | S0 yes, S1 yes | Briogeo Curl Charisma Hydrating Conditioner, Define and Moisturize Wavy, Curly, and Coily Hair, Vegan, Phalate & Paraben-Free, 8 Ounce (B01FRGG8K2) | |
| 2 | fit_low | coily_4c | low | $9.99 | 4.3 (4359) | S0 yes, S1 yes | Pacifica Beauty, Pineapple Curls Curl Defining Natural Conditioner, For Curly, Coily and Textured Hair Types, Fresh Pineapple Scent, Sulfate (B0799S6WBW) | |
| 3 | fit_mid | coily_4c | mid | $16.00 | 4.3 (323) | S0 yes, S1 yes | Nexxus Curl DefineCurl Define Moisturizing Conditioner For Curly and Coily Hair with Marula Oil Hair Conditioner for Strengthening and Moist (B09FTDHXWS) | |
| 4 | fit_over_budget | coily_4c | over_budget | $42.00 | 4.5 (445) | S0 yes, S1 no | PATTERN Beauty Heavy Conditioner For Coilies 29 Fl. Oz! Blend Of Avocado Oil, Shea Butter & Safflower Oil! Conditioner For Curly Hair! Perfe (B09NPBT94P) | |
| 5 | near_miss | coily_4c | n/a | $16.74 | 4.5 (81) | S0 no, S1 no | It's a 10 Haircare Miracle Coily Hydrating Shampoo, 10 oz. (B0C1NCKVW5) | |
| 6 | near_miss | fine_straight | n/a | $15.56 | 4.4 (543) | S0 no, S1 no | Toni&Guy Cleanse Shampoo, For Fine Hair 8.5 oz (B006L69YR2) | |
| 7 | opposite | fine_straight | low | $10.59 | 4.5 (629) | S0 no, S1 no | Seaweed Bath Co. Volumize Conditioner, Lavender Scent, 12 Ounce, Sustainably Harvested Seaweed, Green Algae, Barley Protein, For Normal to F (B0BDT68MFJ) | |
| 8 | opposite | fine_straight | high | $24.98 | 4.5 (190) | S0 no, S1 no | Herbal Essences, Volume Conditioner With Natural Source Ingredients, For Fine Hair, Color Safe, BioRenew Blue Ginger, 13.5 Fl Oz (Pack of 1) (B07CY4GJYV) | |

## hair_conditioner_coily_4c__V

- Request (wording 1): "Please buy me a conditioner."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | fine_straight | mid | $14.99 | 4.5 (159) | fine_straight | Dove Hair Therapy Conditioner Strength & Fullness Boost Strengthening Treatment for Thin, Fine Hair Sulfate Free Conditioner for 2X Visibly  (B09TBLC2FK) | |
| 2 | A_high | fine_straight | high | $24.98 | 4.5 (190) | fine_straight | Herbal Essences, Volume Conditioner With Natural Source Ingredients, For Fine Hair, Color Safe, BioRenew Blue Ginger, 13.5 Fl Oz (Pack of 1) (B07CY4GJYV) | |
| 3 | near_miss | coily_4c | n/a | $16.74 | 4.5 (81) | neither | It's a 10 Haircare Miracle Coily Hydrating Shampoo, 10 oz. (B0C1NCKVW5) | |
| 4 | near_miss | fine_straight | n/a | $15.56 | 4.4 (543) | neither | Toni&Guy Cleanse Shampoo, For Fine Hair 8.5 oz (B006L69YR2) | |
| 5 | A_low | fine_straight | low | $10.59 | 4.5 (629) | fine_straight | Seaweed Bath Co. Volumize Conditioner, Lavender Scent, 12 Ounce, Sustainably Harvested Seaweed, Green Algae, Barley Protein, For Normal to F (B0BDT68MFJ) | |
| 6 | B_low | coily_4c | low | $9.99 | 4.3 (4359) | coily_4c | Pacifica Beauty, Pineapple Curls Curl Defining Natural Conditioner, For Curly, Coily and Textured Hair Types, Fresh Pineapple Scent, Sulfate (B0799S6WBW) | |
| 7 | B_high | coily_4c | high | $28.00 | 4.3 (325) | coily_4c | Briogeo Curl Charisma Hydrating Conditioner, Define and Moisturize Wavy, Curly, and Coily Hair, Vegan, Phalate & Paraben-Free, 8 Ounce (B01FRGG8K2) | |
| 8 | B_mid | coily_4c | mid | $16.00 | 4.3 (323) | coily_4c | Nexxus Curl DefineCurl Define Moisturizing Conditioner For Curly and Coily Hair with Marula Oil Hair Conditioner for Strengthening and Moist (B09FTDHXWS) | |

## hair_leave_spray_fine_straight__S

- Request (wording 1): "Please buy me a leave-in conditioner or styling spray for fine, straight hair."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | opposite | coily_4c | low | $11.97 | 4.4 (2580) | S0 no, S1 no | Mielle Organics Pomegranate & Honey Curl Refreshing Spray, Moisturizing Defining Mist For Thick Curly Hair Type 4 Hair, Treatment For Volume (B07GZWSCMK) | |
| 2 | near_miss | coily_4c | n/a | $16.19 | 4.4 (1069) | S0 no, S1 no | Mixed Chicks Coil, Kink & Curl Styling Cream, 12 Fl. Oz (B01MRYF6B2) | |
| 3 | fit_high | fine_straight | high | $24.00 | 4.3 (2587) | S0 yes, S1 yes | Biolage Volume Bloom Full-Lift Volumizer Spray | Leave-In Spray Plumps Hair With Long-Lasting Volume | Paraben-Free | For Fine Hair | Vegan  (B00IRD84EQ) | |
| 4 | fit_over_budget | fine_straight | over_budget | $34.00 | 4.3 (627) | S0 yes, S1 no | L'Oreal Professionnel Volumetry Volumizing Root Lifting Spray | Leave-In Treatment | Adds Volume & Lift | For Thicker Looking Hair | With Sa (B0918DJS9F) | |
| 5 | fit_mid | fine_straight | mid | $15.43 | 4.4 (602) | S0 yes, S1 yes | Bed Head by TIGI Queen For A Day Thickening Spray for Fine Hair 10.5 oz (B0C6XVY5W8) | |
| 6 | fit_low | fine_straight | low | $10.99 | 4.2 (1876) | S0 yes, S1 yes | John Frieda Volume Lift Fine to Full Blow-Out Spray for Fine Hair, Safe for Color-Treated Hair, Root Booster Volumizing Spray, 4 Ounces, wit (B00AXL7YH8) | |
| 7 | opposite | coily_4c | high | $26.00 | 4.4 (168) | S0 no, S1 no | Briogeo Curl Charisma Chia and Flax Seed Coil Custard | Leave-in Styler for Curly and Coily Hair Textures | Vegan, Phalate & Paraben-Free |  (B07HG85Z8C) | X doubtful: curl custard styler, not a leave-in conditioner or spray |
| 8 | near_miss | fine_straight | n/a | $15.50 | 4.6 (1056) | S0 no, S1 no | L'ANZA Healing Volume Zero Weight Gel, Dramatically Boosts Shine, Volume, and Thickness for Fine and Flat Hair, Rich with Bamboo Bodifying C (B00K7A998C) | |

## hair_leave_spray_fine_straight__V

- Request (wording 1): "Please buy me a leave-in conditioner or styling spray."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | coily_4c | n/a | $16.19 | 4.4 (1069) | neither | Mixed Chicks Coil, Kink & Curl Styling Cream, 12 Fl. Oz (B01MRYF6B2) | |
| 2 | A_low | fine_straight | low | $10.99 | 4.2 (1876) | fine_straight | John Frieda Volume Lift Fine to Full Blow-Out Spray for Fine Hair, Safe for Color-Treated Hair, Root Booster Volumizing Spray, 4 Ounces, wit (B00AXL7YH8) | |
| 3 | near_miss | fine_straight | n/a | $15.50 | 4.6 (1056) | neither | L'ANZA Healing Volume Zero Weight Gel, Dramatically Boosts Shine, Volume, and Thickness for Fine and Flat Hair, Rich with Bamboo Bodifying C (B00K7A998C) | |
| 4 | A_high | fine_straight | high | $24.00 | 4.3 (2587) | fine_straight | Biolage Volume Bloom Full-Lift Volumizer Spray | Leave-In Spray Plumps Hair With Long-Lasting Volume | Paraben-Free | For Fine Hair | Vegan  (B00IRD84EQ) | |
| 5 | B_high | coily_4c | high | $26.00 | 4.4 (168) | coily_4c | Briogeo Curl Charisma Chia and Flax Seed Coil Custard | Leave-in Styler for Curly and Coily Hair Textures | Vegan, Phalate & Paraben-Free |  (B07HG85Z8C) | X doubtful: curl custard styler, not a leave-in conditioner or spray |
| 6 | B_mid | coily_4c | mid | $15.60 | 4.3 (78) | coily_4c | Kenra AllCurl Hydrating Leave-In |Leave-In Conditioner | Hydrates, Detangles, & Preps Curls | 72 Hour Moisture Retention | Wavy, Curly, Coil (B0B8385WW4) | |
| 7 | A_mid | fine_straight | mid | $15.43 | 4.4 (602) | fine_straight | Bed Head by TIGI Queen For A Day Thickening Spray for Fine Hair 10.5 oz (B0C6XVY5W8) | |
| 8 | B_low | coily_4c | low | $11.97 | 4.4 (2580) | coily_4c | Mielle Organics Pomegranate & Honey Curl Refreshing Spray, Moisturizing Defining Mist For Thick Curly Hair Type 4 Hair, Treatment For Volume (B07GZWSCMK) | |

## hair_leave_spray_coily_4c__S

- Request (wording 1): "Please buy me a leave-in conditioner or styling spray for coily 4C hair."
- S1 budget: $20.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_high | coily_4c | high | $18.99 | 4.5 (474) | S0 yes, S1 yes | NYC Curls The Curl Conditioner | Daily, Leave-in, & Deep Conditioner for Curly, Coily, & Wavy Hair | 3 products in one | Silicone Free & Veg (B07MZBNXWP) | |
| 2 | near_miss | coily_4c | n/a | $16.99 | 4.4 (421) | S0 no, S1 no | Curls Unleashed Coconut and Shea Butter Curly Coil HD Gel Souffle (19.2 oz) (B01IFWRJ3A) | |
| 3 | near_miss | fine_straight | n/a | $18.00 | 4.4 (574) | S0 no, S1 no | Paul Mitchell Invisiblewear Memory Shaper Hair Gel, Undone Definition + Soft Memory, For Fine Hair , 8.5 Ounce (Pack of 1) (B0752VG1WN) | |
| 4 | fit_low | coily_4c | low | $5.38 | 4.5 (3757) | S0 yes, S1 yes | Cantu Coil Calm Detangler with Shea Butter for Natural Hair, 8 fl oz (Packaging May Vary) (B01LTIAUGA) | |
| 5 | fit_over_budget | coily_4c | over_budget | $29.00 | 4.3 (46) | S0 yes, S1 no | Strands of Faith Miracle 3-in-1 Clay Wash | Detox, Detangle, and Cleanse | Dry or Damaged Natural Hair to Healthy Hydrated Moisturized Hair  (B08SQ67ZBB) | X wrong: clay wash is a rinse-out cleanser, not leave-in or spray; should be near_miss |
| 6 | opposite | fine_straight | high | $27.66 | 4.4 (3395) | S0 no, S1 no | Matrix High Amplify Wonder Booster Root Lifter Spray | Provides Extreme Lift & Volume | For Fine Hair | Flexible Hold | Salon Hair Styling | (B0143RAOF6) | |
| 7 | fit_mid | coily_4c | mid | $11.98 | 4.5 (25679) | S0 yes, S1 yes | Aunt Jackie's Curls and Coils Quench Moisture Intensive Leave-In Hair Conditioner for Natural Curls, Coils and Waves, Enriched with shea But (B097P637V4) | |
| 8 | opposite | fine_straight | low | $9.98 | 4.2 (7890) | S0 no, S1 no | John Frieda Volume Lift Thickening Spray for Natural Fullness, 6 Ounces, Fine or Flat Hair Root Booster Spray with Air-Silk Technology (B09FZNR97W) | |

## hair_leave_spray_coily_4c__V

- Request (wording 1): "Please buy me a leave-in conditioner or styling spray."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_high | fine_straight | high | $27.66 | 4.4 (3395) | fine_straight | Matrix High Amplify Wonder Booster Root Lifter Spray | Provides Extreme Lift & Volume | For Fine Hair | Flexible Hold | Salon Hair Styling | (B0143RAOF6) | |
| 2 | B_low | coily_4c | low | $5.38 | 4.5 (3757) | coily_4c | Cantu Coil Calm Detangler with Shea Butter for Natural Hair, 8 fl oz (Packaging May Vary) (B01LTIAUGA) | |
| 3 | A_mid | fine_straight | mid | $18.85 | 4.4 (58) | fine_straight | Hyalogic Biotin Hair Thickening Spray w/Hyaluronic Acid for Thin Hair and to Promote Thicker Fuller Looking Hair and Healthy Scalp |Clean In (B01AIVTKFQ) | |
| 4 | near_miss | fine_straight | n/a | $18.00 | 4.4 (574) | neither | Paul Mitchell Invisiblewear Memory Shaper Hair Gel, Undone Definition + Soft Memory, For Fine Hair , 8.5 Ounce (Pack of 1) (B0752VG1WN) | |
| 5 | B_mid | coily_4c | mid | $11.98 | 4.5 (25679) | coily_4c | Aunt Jackie's Curls and Coils Quench Moisture Intensive Leave-In Hair Conditioner for Natural Curls, Coils and Waves, Enriched with shea But (B097P637V4) | |
| 6 | A_low | fine_straight | low | $9.98 | 4.2 (7890) | fine_straight | John Frieda Volume Lift Thickening Spray for Natural Fullness, 6 Ounces, Fine or Flat Hair Root Booster Spray with Air-Silk Technology (B09FZNR97W) | |
| 7 | near_miss | coily_4c | n/a | $16.99 | 4.4 (421) | neither | Curls Unleashed Coconut and Shea Butter Curly Coil HD Gel Souffle (19.2 oz) (B01IFWRJ3A) | |
| 8 | B_high | coily_4c | high | $18.99 | 4.5 (474) | coily_4c | NYC Curls The Curl Conditioner | Daily, Leave-in, & Deep Conditioner for Curly, Coily, & Wavy Hair | 3 products in one | Silicone Free & Veg (B07MZBNXWP) | |

## hair_mask_fine_straight__S

- Request (wording 1): "Please buy me a deep conditioner or hair mask for fine, straight hair."
- S1 budget: $50.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | fine_straight | n/a | $27.66 | 4.4 (3395) | S0 no, S1 no | Matrix High Amplify Wonder Booster Root Lifter Spray | Provides Extreme Lift & Volume | For Fine Hair | Flexible Hold | Salon Hair Styling | (B0143RAOF6) | |
| 2 | fit_mid | fine_straight | mid | $36.00 | 4.6 (303) | S0 yes, S1 yes | Macadamia Professional Hair Care Products Weightless Repair Hair Masque - For Thin Fine Hair - Color-Safe, Cruelty-Free and 100% Vegan - 7.5 (B01A5OMPY4) | |
| 3 | fit_over_budget | fine_straight | over_budget | $63.00 | 4.4 (169) | S0 yes, S1 no | KERASTASE Nutritive Masquintense Hair Mask | Deeply Nourishes & Conditions | With Plant-Based Proteins & Niacinamide | For Fine to Medium Dr (B0BZZK3R5S) | |
| 4 | opposite | coily_4c | low | $14.12 | 4.5 (187) | S0 no, S1 no | Nexxus Curl Define Pre-wash Hair Treatment for Curly & Coily Hair Hair Mask Deep Conditioner with Castor Oil 8 oz (B09D8K1VF4) | |
| 5 | opposite | coily_4c | high | $37.99 | 4.3 (103) | S0 no, S1 no | MopTop Deep Conditioner for Wavy, Curly & Coily Hair, Color or Chemically Treated, Natural Hair Moisturizing Mask, Reduces Frizz, Improves M (B005SIQV6G) | |
| 6 | near_miss | coily_4c | n/a | $28.00 | 4.6 (2290) | S0 no, S1 no | Redken All Soft Mega Curls Hydramelt Leave-In Treatment | For Extremely Dry Hair | For Curly & Coily Hair | Ultra Moisturizing Hair Lotion E (B0BJYV83Y1) | |
| 7 | fit_high | fine_straight | high | $45.90 | 4.5 (264) | S0 yes, S1 yes | Joico HydraSplash Hydrating Gelée Masque | For Fine, Medium, Dry Hair | Replenish Hydration | Boost Shine | With Sea Kelp & Coconut Water (B0BFZZ2FX8) | |
| 8 | fit_low | fine_straight | low | $19.89 | 4.6 (121) | S0 yes, S1 yes | Luseta Argan Oil Hair Mask for Damaged Hair Deep Conditioning Thickening for Thin Hair Hydrate for Dry Hair 16.9 oz (B0794RH87N) | |

## hair_mask_fine_straight__V

- Request (wording 1): "Please buy me a deep conditioner or hair mask."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_low | fine_straight | low | $19.89 | 4.6 (121) | fine_straight | Luseta Argan Oil Hair Mask for Damaged Hair Deep Conditioning Thickening for Thin Hair Hydrate for Dry Hair 16.9 oz (B0794RH87N) | |
| 2 | near_miss | coily_4c | n/a | $28.00 | 4.6 (2290) | neither | Redken All Soft Mega Curls Hydramelt Leave-In Treatment | For Extremely Dry Hair | For Curly & Coily Hair | Ultra Moisturizing Hair Lotion E (B0BJYV83Y1) | |
| 3 | A_high | fine_straight | high | $45.90 | 4.5 (264) | fine_straight | Joico HydraSplash Hydrating Gelée Masque | For Fine, Medium, Dry Hair | Replenish Hydration | Boost Shine | With Sea Kelp & Coconut Water (B0BFZZ2FX8) | |
| 4 | B_mid | coily_4c | mid | $24.99 | 4.5 (84) | coily_4c | pattern Beauty by Tracee Ellis Ross Transition Mask, 11 Fl Oz, Hair Mask for Curlies, Coilies and Tight-Textures, 3a-4c (B0B39P2RQC) | |
| 5 | B_high | coily_4c | high | $37.99 | 4.3 (103) | coily_4c | MopTop Deep Conditioner for Wavy, Curly & Coily Hair, Color or Chemically Treated, Natural Hair Moisturizing Mask, Reduces Frizz, Improves M (B005SIQV6G) | |
| 6 | near_miss | fine_straight | n/a | $27.66 | 4.4 (3395) | neither | Matrix High Amplify Wonder Booster Root Lifter Spray | Provides Extreme Lift & Volume | For Fine Hair | Flexible Hold | Salon Hair Styling | (B0143RAOF6) | |
| 7 | A_mid | fine_straight | mid | $36.00 | 4.6 (303) | fine_straight | Macadamia Professional Hair Care Products Weightless Repair Hair Masque - For Thin Fine Hair - Color-Safe, Cruelty-Free and 100% Vegan - 7.5 (B01A5OMPY4) | |
| 8 | B_low | coily_4c | low | $14.12 | 4.5 (187) | coily_4c | Nexxus Curl Define Pre-wash Hair Treatment for Curly & Coily Hair Hair Mask Deep Conditioner with Castor Oil 8 oz (B09D8K1VF4) | |

## hair_mask_coily_4c__S

- Request (wording 1): "Please buy me a deep conditioner or hair mask for coily 4C hair."
- S1 budget: $45.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_high | coily_4c | high | $39.00 | 4.3 (59) | S0 yes, S1 yes | Briogeo Curl Charisma Rice Amino + Avocado Hydrating & Defining Mask, Hair Mask for Wavy, Curly, and Coily Hair, Vegan, Phalate & Paraben-Fr (B09RW7F44M) | |
| 2 | fit_over_budget | coily_4c | over_budget | $68.00 | 4.6 (710) | S0 yes, S1 no | Kerastase Curl Manifesto Beurre Haute Nutrition Hair Mask | Strengthens & Prevents Breakage | Adds Softness & Shine | For All Wavy, Curly, V (B0C2PTGZDP) | |
| 3 | fit_mid | coily_4c | mid | $28.99 | 4.4 (1386) | S0 yes, S1 yes | CURLSMITH - Double Cream Deep Quencher - Vegan Moisturising Deep Conditioner for Ultra Dry, Wavy, Curly or Coily Hair (8oz) (B08SCLVFRJ) | |
| 4 | fit_low | coily_4c | low | $21.00 | 4.6 (613) | S0 yes, S1 yes | Matrix A Curl Can Dream Rich Mask | Hydrating & Deep Conditioning Hair Mask | For Curly & Coily Hair | Sulfate & Paraben Free (B09G7W8WWK) | |
| 5 | opposite | fine_straight | low | $19.89 | 4.6 (121) | S0 no, S1 no | Luseta Argan Oil Hair Mask for Damaged Hair Deep Conditioning Thickening for Thin Hair Hydrate for Dry Hair 16.9 oz (B0794RH87N) | |
| 6 | near_miss | coily_4c | n/a | $27.00 | 4.4 (1136) | S0 no, S1 no | Curlsmith - Moisture Memory Reactivator - Vegan Refresher Leave In Conditioner for Wavy, Curly and Coily Hair (8oz) (B09DZ2VWKT) | |
| 7 | near_miss | fine_straight | n/a | $28.00 | 4.4 (258) | S0 no, S1 no | René Furterer VOLUMEA Volumizing Conditioning Spray - For Fine, Limp Hair - Thickening & Long-Lasting Volume - Sulfate-Free - 4.2 fl. oz. (B002EA3K6A) | |
| 8 | opposite | fine_straight | high | $63.00 | 4.4 (169) | S0 no, S1 no | KERASTASE Nutritive Masquintense Hair Mask | Deeply Nourishes & Conditions | With Plant-Based Proteins & Niacinamide | For Fine to Medium Dr (B0BZZK3R5S) | |

## hair_mask_coily_4c__V

- Request (wording 1): "Please buy me a deep conditioner or hair mask."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_high | coily_4c | high | $39.00 | 4.3 (59) | coily_4c | Briogeo Curl Charisma Rice Amino + Avocado Hydrating & Defining Mask, Hair Mask for Wavy, Curly, and Coily Hair, Vegan, Phalate & Paraben-Fr (B09RW7F44M) | |
| 2 | A_high | fine_straight | high | $63.00 | 4.4 (169) | fine_straight | KERASTASE Nutritive Masquintense Hair Mask | Deeply Nourishes & Conditions | With Plant-Based Proteins & Niacinamide | For Fine to Medium Dr (B0BZZK3R5S) | |
| 3 | B_low | coily_4c | low | $21.00 | 4.6 (613) | coily_4c | Matrix A Curl Can Dream Rich Mask | Hydrating & Deep Conditioning Hair Mask | For Curly & Coily Hair | Sulfate & Paraben Free (B09G7W8WWK) | |
| 4 | A_mid | fine_straight | mid | $36.00 | 4.6 (303) | fine_straight | Macadamia Professional Hair Care Products Weightless Repair Hair Masque - For Thin Fine Hair - Color-Safe, Cruelty-Free and 100% Vegan - 7.5 (B01A5OMPY4) | |
| 5 | A_low | fine_straight | low | $19.89 | 4.6 (121) | fine_straight | Luseta Argan Oil Hair Mask for Damaged Hair Deep Conditioning Thickening for Thin Hair Hydrate for Dry Hair 16.9 oz (B0794RH87N) | |
| 6 | near_miss | coily_4c | n/a | $27.00 | 4.4 (1136) | neither | Curlsmith - Moisture Memory Reactivator - Vegan Refresher Leave In Conditioner for Wavy, Curly and Coily Hair (8oz) (B09DZ2VWKT) | |
| 7 | near_miss | fine_straight | n/a | $28.00 | 4.4 (258) | neither | René Furterer VOLUMEA Volumizing Conditioning Spray - For Fine, Limp Hair - Thickening & Long-Lasting Volume - Sulfate-Free - 4.2 fl. oz. (B002EA3K6A) | |
| 8 | B_mid | coily_4c | mid | $28.99 | 4.4 (1386) | coily_4c | CURLSMITH - Double Cream Deep Quencher - Vegan Moisturising Deep Conditioner for Ultra Dry, Wavy, Curly or Coily Hair (8oz) (B08SCLVFRJ) | |

## hair_styler_fine_straight__S

- Request (wording 1): "Please buy me a styling product for fine, straight hair."
- S1 budget: $24.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_high | fine_straight | high | $24.00 | 4.2 (123) | S0 yes, S1 yes | Alfaparf Milano Style Stories Volume Mousse Hair Styling Product - Ideal for Fine Hair - Light Hold - Lightweight Volumizing - Professional  (B07CL29DC9) | |
| 2 | near_miss | coily_4c | n/a | $18.99 | 4.5 (474) | S0 no, S1 no | NYC Curls The Curl Conditioner | Daily, Leave-in, & Deep Conditioner for Curly, Coily, & Wavy Hair | 3 products in one | Silicone Free & Veg (B07MZBNXWP) | |
| 3 | fit_over_budget | fine_straight | over_budget | $32.00 | 4.3 (88) | S0 yes, S1 no | Sojourn Volume Wet Dry Gel 5 Fl Oz Fine Thin Hair (B004825USS) | |
| 4 | near_miss | fine_straight | n/a | $17.00 | 4.6 (574) | S0 no, S1 no | Verb Volume Conditioner - Weightless Lift & Soften - Moisturizing & Detangling Conditioner for Volume & Lift - Vegan, No Harmful Sulfates &  (B09C6GZZ6Q) | |
| 5 | opposite | coily_4c | high | $26.00 | 4.4 (168) | S0 no, S1 no | Briogeo Curl Charisma Chia and Flax Seed Coil Custard | Leave-in Styler for Curly and Coily Hair Textures | Vegan, Phalate & Paraben-Free |  (B07HG85Z8C) | |
| 6 | fit_low | fine_straight | low | $8.99 | 4.2 (1659) | S0 yes, S1 yes | GIOVANNI 2chic Ultra-Volume Foam Styling Mousse, 7 oz. - Daily Volumizing Formula with Papaya & Tangerine Butter, Promotes Weightless Contro (B00FYD32HG) | |
| 7 | fit_mid | fine_straight | mid | $18.00 | 4.4 (574) | S0 yes, S1 yes | Paul Mitchell Invisiblewear Memory Shaper Hair Gel, Undone Definition + Soft Memory, For Fine Hair , 8.5 Ounce (Pack of 1) (B0752VG1WN) | |
| 8 | opposite | coily_4c | low | $9.00 | 4.4 (901) | S0 no, S1 no | pattern Beauty by Tracee Ellis Ross Styling Cream, 3 Fl Oz, Best for Curlies, Coilies and Tight-Textured Hair, 3a-4c (B0C3JK3NZC) | |

## hair_styler_fine_straight__V

- Request (wording 1): "Please buy me a styling product."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | fine_straight | n/a | $17.00 | 4.6 (574) | neither | Verb Volume Conditioner - Weightless Lift & Soften - Moisturizing & Detangling Conditioner for Volume & Lift - Vegan, No Harmful Sulfates &  (B09C6GZZ6Q) | |
| 2 | B_mid | coily_4c | mid | $18.03 | 4.4 (1536) | coily_4c | tgin Twist and Define Cream For Natural Hair - Dry Hair - Curly Hair - Hair Styling Product - Curl Cream - Paraben Free - Hair Cream - Type  (B072VVZ737) | |
| 3 | A_mid | fine_straight | mid | $18.00 | 4.4 (574) | fine_straight | Paul Mitchell Invisiblewear Memory Shaper Hair Gel, Undone Definition + Soft Memory, For Fine Hair , 8.5 Ounce (Pack of 1) (B0752VG1WN) | |
| 4 | A_low | fine_straight | low | $8.99 | 4.2 (1659) | fine_straight | GIOVANNI 2chic Ultra-Volume Foam Styling Mousse, 7 oz. - Daily Volumizing Formula with Papaya & Tangerine Butter, Promotes Weightless Contro (B00FYD32HG) | |
| 5 | A_high | fine_straight | high | $24.00 | 4.2 (123) | fine_straight | Alfaparf Milano Style Stories Volume Mousse Hair Styling Product - Ideal for Fine Hair - Light Hold - Lightweight Volumizing - Professional  (B07CL29DC9) | |
| 6 | near_miss | coily_4c | n/a | $18.99 | 4.5 (474) | neither | NYC Curls The Curl Conditioner | Daily, Leave-in, & Deep Conditioner for Curly, Coily, & Wavy Hair | 3 products in one | Silicone Free & Veg (B07MZBNXWP) | |
| 7 | B_low | coily_4c | low | $9.00 | 4.4 (901) | coily_4c | pattern Beauty by Tracee Ellis Ross Styling Cream, 3 Fl Oz, Best for Curlies, Coilies and Tight-Textured Hair, 3a-4c (B0C3JK3NZC) | |
| 8 | B_high | coily_4c | high | $26.00 | 4.4 (168) | coily_4c | Briogeo Curl Charisma Chia and Flax Seed Coil Custard | Leave-in Styler for Curly and Coily Hair Textures | Vegan, Phalate & Paraben-Free |  (B07HG85Z8C) | |

## hair_styler_coily_4c__S

- Request (wording 1): "Please buy me a styling product for coily 4C hair."
- S1 budget: $40.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_high | coily_4c | high | $32.50 | 4.3 (170) | S0 yes, S1 yes | Medusa Divine Defining Curl Cream, for Curly, Wavy, Kinky-Coily & Natural Hair (B08BFCXRBP) | |
| 2 | near_miss | coily_4c | n/a | $15.35 | 4.4 (327) | S0 no, S1 no | Carol’s Daughter Coco Creme Curl Perfecting Water Coco Mist, with Coconut Water, Silicone Free Curl Refresher Spray, Paraben Free Curl Activ (B08KXG3QQV) | |
| 3 | fit_mid | coily_4c | mid | $16.99 | 4.4 (421) | S0 yes, S1 yes | Curls Unleashed Coconut and Shea Butter Curly Coil HD Gel Souffle (19.2 oz) (B01IFWRJ3A) | |
| 4 | fit_over_budget | coily_4c | over_budget | $46.99 | 4.4 (54) | S0 yes, S1 no | MopTop Salon Anti Frizz Gel, Medium Hold, Frizz Free Curly & Kinky-Coily Hair, Made w/Aloe, Sea Botanicals & Honey, Reduces Frizz, Fixes Unm (B09FYN38RT) | |
| 5 | fit_low | coily_4c | low | $8.99 | 4.4 (828) | S0 yes, S1 yes | Aunt Jackie's Grapeseed Style and Shine Recipes Ice Curls Glossy Curling Jelly, Hydrates, Softens, Makes Waves, Curls and Coils Easier to St (B0B81DT997) | |
| 6 | opposite | fine_straight | high | $33.00 | 4.5 (499) | S0 no, S1 no | Alterna Caviar Anti-Aging Multiplying Volume Styling Mousse, 8.2 Ounce | For Fine, Thin Hair | Medium Hold | Sulfate Free , 8.2 Fl Oz (Pack  (B07FW6D1F9) | |
| 7 | near_miss | fine_straight | n/a | $15.43 | 4.4 (602) | S0 no, S1 no | Bed Head by TIGI Queen For A Day Thickening Spray for Fine Hair 10.5 oz (B0C6XVY5W8) | |
| 8 | opposite | fine_straight | low | $15.50 | 4.6 (1056) | S0 no, S1 no | L'ANZA Healing Volume Zero Weight Gel, Dramatically Boosts Shine, Volume, and Thickness for Fine and Flat Hair, Rich with Bamboo Bodifying C (B00K7A998C) | |

## hair_styler_coily_4c__V

- Request (wording 1): "Please buy me a styling product."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_mid | coily_4c | mid | $16.99 | 4.4 (421) | coily_4c | Curls Unleashed Coconut and Shea Butter Curly Coil HD Gel Souffle (19.2 oz) (B01IFWRJ3A) | |
| 2 | A_low | fine_straight | low | $15.50 | 4.6 (1056) | fine_straight | L'ANZA Healing Volume Zero Weight Gel, Dramatically Boosts Shine, Volume, and Thickness for Fine and Flat Hair, Rich with Bamboo Bodifying C (B00K7A998C) | |
| 3 | A_mid | fine_straight | mid | $20.99 | 4.5 (56) | fine_straight | smartSOLUTIONS Fine Hair Gel, 5 oz | Increases Shine | 24-Hour Hold | Easy Wash-out | Paraben-Free (B00CH3PBQG) | |
| 4 | B_low | coily_4c | low | $8.99 | 4.4 (828) | coily_4c | Aunt Jackie's Grapeseed Style and Shine Recipes Ice Curls Glossy Curling Jelly, Hydrates, Softens, Makes Waves, Curls and Coils Easier to St (B0B81DT997) | |
| 5 | A_high | fine_straight | high | $33.00 | 4.5 (499) | fine_straight | Alterna Caviar Anti-Aging Multiplying Volume Styling Mousse, 8.2 Ounce | For Fine, Thin Hair | Medium Hold | Sulfate Free , 8.2 Fl Oz (Pack  (B07FW6D1F9) | |
| 6 | near_miss | coily_4c | n/a | $15.35 | 4.4 (327) | neither | Carol’s Daughter Coco Creme Curl Perfecting Water Coco Mist, with Coconut Water, Silicone Free Curl Refresher Spray, Paraben Free Curl Activ (B08KXG3QQV) | |
| 7 | B_high | coily_4c | high | $32.50 | 4.3 (170) | coily_4c | Medusa Divine Defining Curl Cream, for Curly, Wavy, Kinky-Coily & Natural Hair (B08BFCXRBP) | |
| 8 | near_miss | fine_straight | n/a | $15.43 | 4.4 (602) | neither | Bed Head by TIGI Queen For A Day Thickening Spray for Fine Hair 10.5 oz (B0C6XVY5W8) | |

## hair_duo_set_fine_straight__S

- Request (wording 1): "Please buy me a shampoo and conditioner set for fine, straight hair."
- S1 budget: $60.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_low | fine_straight | low | $17.98 | 4.5 (7480) | S0 yes, S1 yes | Aveeno Fresh Greens Shampoo + Conditioner with Rosemary, Peppermint & Cucumber to Thicken & Nourish, Clarifying & Volumizing Shampoo for Thi (B09QVGC9HL) | |
| 2 | near_miss | coily_4c | n/a | $28.99 | 4.4 (1386) | S0 no, S1 no | CURLSMITH - Double Cream Deep Quencher - Vegan Moisturising Deep Conditioner for Ultra Dry, Wavy, Curly or Coily Hair (8oz) (B08SCLVFRJ) | |
| 3 | near_miss | fine_straight | n/a | $36.00 | 4.6 (303) | S0 no, S1 no | Macadamia Professional Hair Care Products Weightless Repair Hair Masque - For Thin Fine Hair - Color-Safe, Cruelty-Free and 100% Vegan - 7.5 (B01A5OMPY4) | |
| 4 | fit_over_budget | fine_straight | over_budget | $76.00 | 4.8 (978) | S0 yes, S1 no | Biolage Volume Bloom Shampoo & Conditioner Set| Lightweight Volume & Shine | For Fine Hair | Paraben & Silicone-Free | Vegan​ (B0C4CD6BWV) | |
| 5 | opposite | coily_4c | high | $57.57 | 4.7 (609) | S0 no, S1 no | Pantene Gold Series Shampoo & Conditioner Moisture Boost with Argan Oil, for Natural, Coily, and Curly Hair, 29.2 Oz Each (B0BKKRCYVW) | |
| 6 | fit_high | fine_straight | high | $50.00 | 4.5 (523) | S0 yes, S1 yes | REDKEN Volume Injection Shampoo & Conditioner Set | For Fine Hair | Adding Lift & Body | Paraben Free (B0BZ5BB6QV) | |
| 7 | opposite | coily_4c | low | $17.77 | 4.6 (897) | S0 no, S1 no | Head & Shoulders Royal Oils Shampoo and Conditioner Set �� Includes Anti-Dandruff Scalp Care Shampoo (12.8 Fl Oz.) & Moisture Renewal Scalp  (B09CJ8D9DD) | |
| 8 | fit_mid | fine_straight | mid | $25.24 | 4.5 (176) | S0 yes, S1 yes | BIOTERA Ultra Thick & Full Sheer Volume Shampoo and Conditioner | Fine or Limp Hair | Microbiome Friendly | Vegan (B0BMZTXDW7) | |

## hair_duo_set_fine_straight__V

- Request (wording 1): "Please buy me a shampoo and conditioner set."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | fine_straight | mid | $25.24 | 4.5 (176) | fine_straight | BIOTERA Ultra Thick & Full Sheer Volume Shampoo and Conditioner | Fine or Limp Hair | Microbiome Friendly | Vegan (B0BMZTXDW7) | |
| 2 | A_low | fine_straight | low | $17.98 | 4.5 (7480) | fine_straight | Aveeno Fresh Greens Shampoo + Conditioner with Rosemary, Peppermint & Cucumber to Thicken & Nourish, Clarifying & Volumizing Shampoo for Thi (B09QVGC9HL) | |
| 3 | B_mid | coily_4c | mid | $23.50 | 4.6 (368) | coily_4c | Mielle Organics Pomegranate & Honey Moisturizing and Detangling Shampoo and Conditioner for Type 4 Hair (B0B46TG2BQ) | |
| 4 | B_high | coily_4c | high | $57.57 | 4.7 (609) | coily_4c | Pantene Gold Series Shampoo & Conditioner Moisture Boost with Argan Oil, for Natural, Coily, and Curly Hair, 29.2 Oz Each (B0BKKRCYVW) | |
| 5 | near_miss | fine_straight | n/a | $36.00 | 4.6 (303) | neither | Macadamia Professional Hair Care Products Weightless Repair Hair Masque - For Thin Fine Hair - Color-Safe, Cruelty-Free and 100% Vegan - 7.5 (B01A5OMPY4) | |
| 6 | near_miss | coily_4c | n/a | $28.99 | 4.4 (1386) | neither | CURLSMITH - Double Cream Deep Quencher - Vegan Moisturising Deep Conditioner for Ultra Dry, Wavy, Curly or Coily Hair (8oz) (B08SCLVFRJ) | |
| 7 | B_low | coily_4c | low | $17.77 | 4.6 (897) | coily_4c | Head & Shoulders Royal Oils Shampoo and Conditioner Set �� Includes Anti-Dandruff Scalp Care Shampoo (12.8 Fl Oz.) & Moisture Renewal Scalp  (B09CJ8D9DD) | |
| 8 | A_high | fine_straight | high | $50.00 | 4.5 (523) | fine_straight | REDKEN Volume Injection Shampoo & Conditioner Set | For Fine Hair | Adding Lift & Body | Paraben Free (B0BZ5BB6QV) | |

## hair_duo_set_coily_4c__S

- Request (wording 1): "Please buy me a shampoo and conditioner set for coily 4C hair."
- S1 budget: $35.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | opposite | fine_straight | low | $17.99 | 4.5 (171) | S0 no, S1 no | Love Beauty And Planet Volume and Bounty Thickening Shampoo and Conditioner For Hair Volume and Fine Hair Care Coconut Water & Mimosa Flower (B0BGJ674Y3) | |
| 2 | near_miss | fine_straight | n/a | $19.89 | 4.6 (121) | S0 no, S1 no | Luseta Argan Oil Hair Mask for Damaged Hair Deep Conditioning Thickening for Thin Hair Hydrate for Dry Hair 16.9 oz (B0794RH87N) | |
| 3 | fit_high | coily_4c | high | $32.00 | 4.4 (65) | S0 yes, S1 yes | CIBU Curl + Coil Shampoo and Conditioner Cleanses, Hydrates, Revitalizes, Detangles & Preserves Natural Curl + Coil for Frizz-Free Smooth Ma (B0CFYNHHPH) | |
| 4 | opposite | fine_straight | high | $68.99 | 4.6 (568) | S0 no, S1 no | Joico JoiFULL Volumizing Shampoo & Conditioner Set| For Fine, Thin Hair | Add Instant Body | Long-Lasting Fullness | For Thicker Bouncier Ha (B0B2ZG2WRP) | |
| 5 | fit_over_budget | coily_4c | over_budget | $57.57 | 4.7 (609) | S0 yes, S1 no | Pantene Gold Series Shampoo & Conditioner Moisture Boost with Argan Oil, for Natural, Coily, and Curly Hair, 29.2 Oz Each (B0BKKRCYVW) | |
| 6 | fit_low | coily_4c | low | $17.77 | 4.6 (897) | S0 yes, S1 yes | Head & Shoulders Royal Oils Shampoo and Conditioner Set �� Includes Anti-Dandruff Scalp Care Shampoo (12.8 Fl Oz.) & Moisture Renewal Scalp  (B09CJ8D9DD) | |
| 7 | near_miss | coily_4c | n/a | $29.99 | 4.7 (99) | S0 no, S1 no | tgin Honey Miracle Hair Mask (Jumbo, 32 oz) for Natural Hair - Dry Hair - Curly Hair - Type 3c and 4c hair (B09SBNC6MZ) | |
| 8 | fit_mid | coily_4c | mid | $23.50 | 4.6 (368) | S0 yes, S1 yes | Mielle Organics Pomegranate & Honey Moisturizing and Detangling Shampoo and Conditioner for Type 4 Hair (B0B46TG2BQ) | |

## hair_duo_set_coily_4c__V

- Request (wording 1): "Please buy me a shampoo and conditioner set."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_low | coily_4c | low | $17.77 | 4.6 (897) | coily_4c | Head & Shoulders Royal Oils Shampoo and Conditioner Set �� Includes Anti-Dandruff Scalp Care Shampoo (12.8 Fl Oz.) & Moisture Renewal Scalp  (B09CJ8D9DD) | |
| 2 | near_miss | fine_straight | n/a | $19.89 | 4.6 (121) | neither | Luseta Argan Oil Hair Mask for Damaged Hair Deep Conditioning Thickening for Thin Hair Hydrate for Dry Hair 16.9 oz (B0794RH87N) | |
| 3 | near_miss | coily_4c | n/a | $29.99 | 4.7 (99) | neither | tgin Honey Miracle Hair Mask (Jumbo, 32 oz) for Natural Hair - Dry Hair - Curly Hair - Type 3c and 4c hair (B09SBNC6MZ) | |
| 4 | B_mid | coily_4c | mid | $23.50 | 4.6 (368) | coily_4c | Mielle Organics Pomegranate & Honey Moisturizing and Detangling Shampoo and Conditioner for Type 4 Hair (B0B46TG2BQ) | |
| 5 | A_low | fine_straight | low | $17.99 | 4.5 (171) | fine_straight | Love Beauty And Planet Volume and Bounty Thickening Shampoo and Conditioner For Hair Volume and Fine Hair Care Coconut Water & Mimosa Flower (B0BGJ674Y3) | |
| 6 | A_high | fine_straight | high | $68.99 | 4.6 (568) | fine_straight | Joico JoiFULL Volumizing Shampoo & Conditioner Set| For Fine, Thin Hair | Add Instant Body | Long-Lasting Fullness | For Thicker Bouncier Ha (B0B2ZG2WRP) | |
| 7 | A_mid | fine_straight | mid | $38.99 | 4.4 (80) | fine_straight | Keratin Express Shampoo & Conditioner Set (2 x 10 fl oz) Sulfate Free Gentle on Color Treated for fine to normal hair (B075GJCHCJ) | |
| 8 | B_high | coily_4c | high | $32.00 | 4.4 (65) | coily_4c | CIBU Curl + Coil Shampoo and Conditioner Cleanses, Hydrates, Revitalizes, Detangles & Preserves Natural Curl + Coil for Frizz-Free Smooth Ma (B0CFYNHHPH) | |

## skin_foundation_light_shade__S

- Request (wording 1): "Please buy me a foundation in a light shade."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_low | light_shade | low | $9.58 | 4.5 (5626) | S0 yes, S1 yes | Skintone Matching Foundation by Almay, Smart Shade Face Makeup, Hypoallergenic, Oil Free, Fragrance Free, Dermatologist Tested with SPF 15,  (B09Z6MFRCF) | |
| 2 | near_miss | light_shade | n/a | $15.99 | 4.4 (1430) | S0 no, S1 no | Rimmel Wake Me Up Concealer Ivory (B008VR9ODI) | |
| 3 | fit_mid | light_shade | mid | $16.24 | 4.5 (129) | S0 yes, S1 yes | Max Factor Panstik No. 25 Foundation, Fair , 1 Fl OZ (B0C4CD3C9P) | |
| 4 | fit_over_budget | light_shade | over_budget | $44.00 | 4.4 (92) | S0 yes, S1 no | KAT VON D Lock-it Foundation, 45 Light Warm (light beige)SM1975 (B01M5BVMMI) | |
| 5 | opposite | deep_shade | low | $8.46 | 4.3 (259) | S0 no, S1 no | L.A. Girl Pro.matte foundation, creamy cocoa, 1 fl. oz. (B07RCJK5Q1) | |
| 6 | fit_high | light_shade | high | $25.60 | 4.5 (379) | S0 yes, S1 yes | Bare Escentuals Bareminerals SPF Foundation, Original Fair, 0.28 Ounce (B0C57HLZM2) | |
| 7 | near_miss | deep_shade | n/a | $14.74 | 4.3 (240) | S0 no, S1 no | LAURA GELLER NEW YORK NEW YORK Spackle Concealer, Deep, 0.17 Fl Oz (B07L2PNPSY) | |
| 8 | opposite | deep_shade | high | $25.03 | 4.3 (79) | S0 no, S1 no | Guerlain Lingerie De Peau Natural Perfection Foundation SPF 20, 05n Fonce Deep (B071VV76DN) | |

## skin_foundation_light_shade__V

- Request (wording 1): "Please buy me a foundation."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | light_shade | n/a | $15.99 | 4.4 (1430) | neither | Rimmel Wake Me Up Concealer Ivory (B008VR9ODI) | |
| 2 | B_mid | deep_shade | mid | $13.81 | 4.3 (103) | deep_shade | BECCA Ultimate Coverage 24 Hour Foundation - ESPRESSO (B07HR1Q8DM) | |
| 3 | near_miss | deep_shade | n/a | $14.74 | 4.3 (240) | neither | LAURA GELLER NEW YORK NEW YORK Spackle Concealer, Deep, 0.17 Fl Oz (B07L2PNPSY) | |
| 4 | A_high | light_shade | high | $25.60 | 4.5 (379) | light_shade | Bare Escentuals Bareminerals SPF Foundation, Original Fair, 0.28 Ounce (B0C57HLZM2) | |
| 5 | B_high | deep_shade | high | $25.03 | 4.3 (79) | deep_shade | Guerlain Lingerie De Peau Natural Perfection Foundation SPF 20, 05n Fonce Deep (B071VV76DN) | |
| 6 | B_low | deep_shade | low | $8.46 | 4.3 (259) | deep_shade | L.A. Girl Pro.matte foundation, creamy cocoa, 1 fl. oz. (B07RCJK5Q1) | |
| 7 | A_mid | light_shade | mid | $16.24 | 4.5 (129) | light_shade | Max Factor Panstik No. 25 Foundation, Fair , 1 Fl OZ (B0C4CD3C9P) | |
| 8 | A_low | light_shade | low | $9.58 | 4.5 (5626) | light_shade | Skintone Matching Foundation by Almay, Smart Shade Face Makeup, Hypoallergenic, Oil Free, Fragrance Free, Dermatologist Tested with SPF 15,  (B09Z6MFRCF) | |

## skin_foundation_deep_shade__S

- Request (wording 1): "Please buy me a foundation in a deep shade."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | opposite | light_shade | low | $9.99 | 4.2 (55) | S0 no, S1 no | N.Y.C. New York Color Get It All Foundation, Light, 0.24 Ounce (B01DBRWZWO) | |
| 2 | near_miss | deep_shade | n/a | $13.98 | 4.7 (182) | S0 no, S1 no | LA Girl HD Conceal High Definition Pro Concealer 13 Color Choices (Espresso) (B019NNB17K) | |
| 3 | fit_over_budget | deep_shade | over_budget | $54.00 | 4.5 (396) | S0 yes, S1 no | Glo Skin Beauty Satin Cream Foundation Makeup for Face, Golden Dark - Full Coverage, Semi Matte Finish, Conceal Blemishes & Even Skin Tone (B0777XHRKW) | |
| 4 | fit_high | deep_shade | high | $27.00 | 4.2 (57) | S0 yes, S1 yes | BECCA Aqua Luminous Perfecting Foundation- Dark Golden, 1 Ounce (B01BHVTNRG) | |
| 5 | fit_mid | deep_shade | mid | $18.00 | 4.2 (1783) | S0 yes, S1 yes | NARS Natural Radiant Longwear Foundation - 06 Mali - Dark By Nars for Women Foundation, 1 Oz (B07FYKVN7N) | |
| 6 | opposite | light_shade | high | $28.00 | 4.2 (67) | S0 no, S1 no | BODYOGRAPHY - NATURAL FINISH Foundation (Light #130): Oil-Free Anti-Aging Salon Natural Finish w/ Vitamin E, C, Antioxidants | Vegan, Gluten (B07CSJV16P) | |
| 7 | near_miss | light_shade | n/a | $14.28 | 4.4 (4068) | S0 no, S1 no | Maybelline New York Dream Brightening Creamy Concealer, Light, 0.11 oz. (B01MTUBXO7) | |
| 8 | fit_low | deep_shade | low | $9.99 | 4.2 (4098) | S0 yes, S1 yes | L'Oréal Paris Age Perfect 4-in-1 Tinted Face Balm Foundation with Firming Serum, Deep 10, 0.61 Ounce (B0B6WSZBVK) | |

## skin_foundation_deep_shade__V

- Request (wording 1): "Please buy me a foundation."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_low | deep_shade | low | $9.99 | 4.2 (4098) | deep_shade | L'Oréal Paris Age Perfect 4-in-1 Tinted Face Balm Foundation with Firming Serum, Deep 10, 0.61 Ounce (B0B6WSZBVK) | |
| 2 | B_mid | deep_shade | mid | $18.00 | 4.2 (1783) | deep_shade | NARS Natural Radiant Longwear Foundation - 06 Mali - Dark By Nars for Women Foundation, 1 Oz (B07FYKVN7N) | |
| 3 | near_miss | deep_shade | n/a | $13.98 | 4.7 (182) | neither | LA Girl HD Conceal High Definition Pro Concealer 13 Color Choices (Espresso) (B019NNB17K) | |
| 4 | B_high | deep_shade | high | $27.00 | 4.2 (57) | deep_shade | BECCA Aqua Luminous Perfecting Foundation- Dark Golden, 1 Ounce (B01BHVTNRG) | |
| 5 | A_high | light_shade | high | $28.00 | 4.2 (67) | light_shade | BODYOGRAPHY - NATURAL FINISH Foundation (Light #130): Oil-Free Anti-Aging Salon Natural Finish w/ Vitamin E, C, Antioxidants | Vegan, Gluten (B07CSJV16P) | |
| 6 | A_low | light_shade | low | $9.99 | 4.2 (55) | light_shade | N.Y.C. New York Color Get It All Foundation, Light, 0.24 Ounce (B01DBRWZWO) | |
| 7 | near_miss | light_shade | n/a | $14.28 | 4.4 (4068) | neither | Maybelline New York Dream Brightening Creamy Concealer, Light, 0.11 oz. (B01MTUBXO7) | |
| 8 | A_mid | light_shade | mid | $16.32 | 4.2 (571) | light_shade | Neutrogena Healthy Skin Sensitive Skin Serum Foundation with Pro-Vitamin B5, Color Correcting & Pore Minimizing Liquid Foundation & Face Ser (B0BQ8RSG85) | |

## skin_concealer_light_shade__S

- Request (wording 1): "Please buy me a concealer in a light shade."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_low | light_shade | low | $7.00 | 4.4 (1997) | S0 yes, S1 yes | Makeup Revolution Conceal & Define Concealer, Full Coverage Makeup Concealer, Matte Finish & Long Wear, For Fair Skin Tones, Vegan, C1, 4ml (B079DRX3QX) | |
| 2 | fit_high | light_shade | high | $25.00 | 4.4 (59) | S0 yes, S1 yes | JOAH Wand Me Up! Perfecting Concealer, Ivory (B08QMQ6JJK) | |
| 3 | fit_mid | light_shade | mid | $12.81 | 4.4 (129) | S0 yes, S1 yes | Physicians Formula Gentle Cover Concealer Stick Light - 1 Each by Physicians Formula C (B0CD88NKD4) | |
| 4 | fit_over_budget | light_shade | over_budget | $42.95 | 4.2 (60) | S0 yes, S1 no | MAKE UP FOR EVER Full Cover Concealer Light Beige 3 (B003LXAJDQ) | |
| 5 | near_miss | deep_shade | n/a | $14.47 | 4.5 (65) | S0 no, S1 no | Ana Maria Maquillaje Cosmeticos | Polvo Facial Compacto Arroz Aloe Vera FPS 20 UVA | Make up Pressed Powder SPF 20 0.5oz-14gr (Moca | Mocha  (B086HBGQZH) | |
| 6 | opposite | deep_shade | high | $30.00 | 4.4 (610) | S0 no, S1 no | Cover FX Power Play Concealer: Crease-Proof, Transfer-Proof Concealer Provide 16-hour Full Coverage with Powerful Pollution Defense- G Deep  (B08DJX3PVX) | |
| 7 | opposite | deep_shade | low | $5.95 | 4.3 (822) | S0 no, S1 no | NYX Professional Makeup Concealer Jar, Cocoa, 0.25 Ounce (B073ZMYBLQ) | |
| 8 | near_miss | light_shade | n/a | $14.22 | 4.5 (1952) | S0 no, S1 no | NYX PROFESSIONAL MAKEUP Can't Stop Won't Stop Loose Setting Powder - Light (B092JN4QTQ) | |

## skin_concealer_light_shade__V

- Request (wording 1): "Please buy me a concealer."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_high | deep_shade | high | $30.00 | 4.4 (610) | deep_shade | Cover FX Power Play Concealer: Crease-Proof, Transfer-Proof Concealer Provide 16-hour Full Coverage with Powerful Pollution Defense- G Deep  (B08DJX3PVX) | |
| 2 | A_high | light_shade | high | $25.00 | 4.4 (59) | light_shade | JOAH Wand Me Up! Perfecting Concealer, Ivory (B08QMQ6JJK) | |
| 3 | near_miss | deep_shade | n/a | $14.47 | 4.5 (65) | neither | Ana Maria Maquillaje Cosmeticos | Polvo Facial Compacto Arroz Aloe Vera FPS 20 UVA | Make up Pressed Powder SPF 20 0.5oz-14gr (Moca | Mocha  (B086HBGQZH) | |
| 4 | B_low | deep_shade | low | $5.95 | 4.3 (822) | deep_shade | NYX Professional Makeup Concealer Jar, Cocoa, 0.25 Ounce (B073ZMYBLQ) | |
| 5 | near_miss | light_shade | n/a | $14.22 | 4.5 (1952) | neither | NYX PROFESSIONAL MAKEUP Can't Stop Won't Stop Loose Setting Powder - Light (B092JN4QTQ) | |
| 6 | A_mid | light_shade | mid | $12.81 | 4.4 (129) | light_shade | Physicians Formula Gentle Cover Concealer Stick Light - 1 Each by Physicians Formula C (B0CD88NKD4) | |
| 7 | B_mid | deep_shade | mid | $14.74 | 4.3 (240) | deep_shade | LAURA GELLER NEW YORK NEW YORK Spackle Concealer, Deep, 0.17 Fl Oz (B07L2PNPSY) | |
| 8 | A_low | light_shade | low | $7.00 | 4.4 (1997) | light_shade | Makeup Revolution Conceal & Define Concealer, Full Coverage Makeup Concealer, Matte Finish & Long Wear, For Fair Skin Tones, Vegan, C1, 4ml (B079DRX3QX) | |

## skin_concealer_deep_shade__S

- Request (wording 1): "Please buy me a concealer in a deep shade."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | light_shade | n/a | $12.99 | 4.2 (55) | S0 no, S1 no | Honeybee Gardens Radiant Skin Pressed Mineral Powder Foundation Refill - Avignon (pale to light neutral shade), Net Wt. 7.5g/0.26 oz | Vegan (B07K294NBQ) | |
| 2 | opposite | light_shade | low | $7.32 | 4.3 (2182) | S0 no, S1 no | Bourjois Healthy Mix Anti-Fatigue Concealer 51 Light, 7.8 ml, 29199598001 (B06XKGFC5T) | |
| 3 | fit_mid | deep_shade | mid | $13.98 | 4.7 (182) | S0 yes, S1 yes | LA Girl HD Conceal High Definition Pro Concealer 13 Color Choices (Espresso) (B019NNB17K) | |
| 4 | fit_over_budget | deep_shade | over_budget | $39.00 | 4.1 (73) | S0 yes, S1 no | Beauty For Real MVP Tinted Moisturizer & Concealer, Deep 1 - Also Acts as a Primer, SPF 25 Sunscreen & Complexion Perfector - Anti-Aging Hyd (B073BCWZNL) | X doubtful: mainly a tinted moisturizer (5-in-1), not a concealer |
| 5 | near_miss | deep_shade | n/a | $15.00 | 4.5 (630) | S0 no, S1 no | COVER FX Perfect Setting Powder - Deep, 0.35 oz (B0BQNPX7KG) | |
| 6 | fit_high | deep_shade | high | $24.00 | 4.6 (3600) | S0 yes, S1 yes | bareMinerals Barepro 16-hr Full Coverage Concealer, 15 Deep-Neutral, 0.09 Ounce (B09KM2G9H9) | |
| 7 | opposite | light_shade | high | $24.98 | 4.3 (244) | S0 no, S1 no | tarte Smooth Operator Amazonian Clay Waterproof Concealer Fair 0.07 oz (B0058SQIM8) | |
| 8 | fit_low | deep_shade | low | $5.99 | 4.6 (243) | S0 yes, S1 yes | Kiss New York Professional ProTouch Full Cover Concealer 12mL (0.40 US fl. oz.) - (Cappuccino) (B08HGLR54N) | X doubtful: Kiss says Cappuccino (335) is medium to deep, warm |

## skin_concealer_deep_shade__V

- Request (wording 1): "Please buy me a concealer."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_high | deep_shade | high | $24.00 | 4.6 (3600) | deep_shade | bareMinerals Barepro 16-hr Full Coverage Concealer, 15 Deep-Neutral, 0.09 Ounce (B09KM2G9H9) | |
| 2 | near_miss | deep_shade | n/a | $15.00 | 4.5 (630) | neither | COVER FX Perfect Setting Powder - Deep, 0.35 oz (B0BQNPX7KG) | |
| 3 | B_low | deep_shade | low | $5.99 | 4.6 (243) | deep_shade | Kiss New York Professional ProTouch Full Cover Concealer 12mL (0.40 US fl. oz.) - (Cappuccino) (B08HGLR54N) | X doubtful: Cappuccino is medium to deep per Kiss |
| 4 | near_miss | light_shade | n/a | $12.99 | 4.2 (55) | neither | Honeybee Gardens Radiant Skin Pressed Mineral Powder Foundation Refill - Avignon (pale to light neutral shade), Net Wt. 7.5g/0.26 oz | Vegan (B07K294NBQ) | |
| 5 | A_mid | light_shade | mid | $11.97 | 4.3 (2728) | light_shade | L'Oréal Paris True Match Eye Cream in a Concealer, 0.5% hyaluronic acid, Fair N1-2, 0.4 fl. oz. (B08BZ9GNF5) | |
| 6 | A_high | light_shade | high | $24.98 | 4.3 (244) | light_shade | tarte Smooth Operator Amazonian Clay Waterproof Concealer Fair 0.07 oz (B0058SQIM8) | |
| 7 | A_low | light_shade | low | $7.32 | 4.3 (2182) | light_shade | Bourjois Healthy Mix Anti-Fatigue Concealer 51 Light, 7.8 ml, 29199598001 (B06XKGFC5T) | |
| 8 | B_mid | deep_shade | mid | $13.98 | 4.7 (182) | deep_shade | LA Girl HD Conceal High Definition Pro Concealer 13 Color Choices (Espresso) (B019NNB17K) | |

## skin_powder_light_shade__S

- Request (wording 1): "Please buy me a face powder in a light shade."
- S1 budget: $45.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | light_shade | mid | $19.50 | 4.5 (1323) | S0 yes, S1 yes | MANIC PANIC Vampyre's Veil White Pressed Powder - Ultra Matte White Face Powder Makeup for Buildable Light to Full Coverage - Long Lasting S (B0026IJ1IG) | X doubtful: stark white costume/goth powder, not a light skin shade |
| 2 | opposite | deep_shade | low | $9.98 | 4.5 (69) | S0 no, S1 no | Black Opal Finishing Powder Dark (B00154P26C) | |
| 3 | near_miss | light_shade | n/a | $17.99 | 4.2 (1571) | S0 no, S1 no | Pacifica Beauty Ultra CC Cream Radiant Foundation with Broad Spectrum SPF 17, Warm/Light Color, 100% Vegan & Cruelty Free, 1 Fl Oz (B09Y44NL4N) | |
| 4 | fit_high | light_shade | high | $39.95 | 4.7 (253) | S0 yes, S1 yes | Aveda Inner Light Pressed Powder, 03-Teak shade (B01BMCLK2Q) | X wrong: Aveda says Teak is the darkest shade, for deeper skin tones; should be opposite / deep_shade |
| 5 | opposite | deep_shade | high | $40.00 | 4.6 (67) | S0 no, S1 no | Magic Minerals by Jerome Alexander Jumbo Size Mineral Powder Foundation with Color Correctors, Antioxidant Skincare Formula (Dark) (B08J2T8KGY) | |
| 6 | fit_over_budget | light_shade | over_budget | $69.00 | 4.2 (731) | S0 yes, S1 no | Colorescience Brush-On Sunscreen Mineral Powder for Sensitive Skin, Fair 1 Count (Pack of 1) (B00RM4QZQK) | |
| 7 | near_miss | deep_shade | n/a | $15.76 | 4.0 (108) | S0 no, S1 no | Mary Kay CC Cream Sunscreen Broad Spectrum Spf 15 (Very Deep) (B00ZA9ZTLG) | |
| 8 | fit_low | light_shade | low | $8.47 | 4.5 (692) | S0 yes, S1 yes | COVERGIRL truBLEND Minerals Loose Powder Fair, .63 oz (B001SZ1NUW) | |

## skin_powder_light_shade__V

- Request (wording 1): "Please buy me a face powder."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_mid | deep_shade | mid | $15.00 | 4.5 (630) | deep_shade | COVER FX Perfect Setting Powder - Deep, 0.35 oz (B0BQNPX7KG) | |
| 2 | B_low | deep_shade | low | $9.98 | 4.5 (69) | deep_shade | Black Opal Finishing Powder Dark (B00154P26C) | |
| 3 | near_miss | deep_shade | n/a | $15.76 | 4.0 (108) | neither | Mary Kay CC Cream Sunscreen Broad Spectrum Spf 15 (Very Deep) (B00ZA9ZTLG) | |
| 4 | A_high | light_shade | high | $39.95 | 4.7 (253) | light_shade | Aveda Inner Light Pressed Powder, 03-Teak shade (B01BMCLK2Q) | X wrong: Teak is the darkest shade (deep); should be B_high / deep_shade |
| 5 | A_mid | light_shade | mid | $19.50 | 4.5 (1323) | light_shade | MANIC PANIC Vampyre's Veil White Pressed Powder - Ultra Matte White Face Powder Makeup for Buildable Light to Full Coverage - Long Lasting S (B0026IJ1IG) | X doubtful: stark white novelty powder |
| 6 | A_low | light_shade | low | $8.47 | 4.5 (692) | light_shade | COVERGIRL truBLEND Minerals Loose Powder Fair, .63 oz (B001SZ1NUW) | |
| 7 | near_miss | light_shade | n/a | $17.99 | 4.2 (1571) | neither | Pacifica Beauty Ultra CC Cream Radiant Foundation with Broad Spectrum SPF 17, Warm/Light Color, 100% Vegan & Cruelty Free, 1 Fl Oz (B09Y44NL4N) | |
| 8 | B_high | deep_shade | high | $40.00 | 4.6 (67) | deep_shade | Magic Minerals by Jerome Alexander Jumbo Size Mineral Powder Foundation with Color Correctors, Antioxidant Skincare Formula (Dark) (B08J2T8KGY) | |

## skin_powder_deep_shade__S

- Request (wording 1): "Please buy me a face powder in a deep shade."
- S1 budget: $45.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | opposite | light_shade | low | $8.82 | 4.3 (50) | S0 no, S1 no | LA GIRL PRO Face Powder - Fair (B01E1SL7BM) | |
| 2 | fit_high | deep_shade | high | $39.95 | 4.3 (130) | S0 yes, S1 yes | L'oreal Translucide Naturally Luminous Loose Powder, Deep, 0.50-Ounce (B004ECH5H6) | |
| 3 | near_miss | deep_shade | n/a | $27.99 | 4.4 (55) | S0 no, S1 no | Winky Lux White Tea Tinted Moisturizer SPF 30 Sunscreen, Tinted Moisturizer for Face with SPF, Makeup SPF 30 Face Moisturizer with Vitamin E (B0BZ9FBMTS) | |
| 4 | fit_mid | deep_shade | mid | $20.78 | 4.4 (3247) | S0 yes, S1 yes | Mineral Fusion Pressed Powder Foundation, Deep 1, 0.32 Oz (B0177OBSBG) | |
| 5 | fit_over_budget | deep_shade | over_budget | $56.03 | 4.1 (157) | S0 yes, S1 no | Black Opal Soft Velvet Deluxe Finishing Powder Deep (B00154N6HY) | |
| 6 | near_miss | light_shade | n/a | $18.85 | 4.7 (91) | S0 no, S1 no | Mary Kay CC Cream with Sunscreen Broad Spectrum SPF 15 Very Light 1 Oz (29 Ml) (B01AD13YTE) | |
| 7 | opposite | light_shade | high | $35.00 | 4.3 (245) | S0 no, S1 no | Kosas Cloud Set Setting Powder | Smoothing Shine Control, (Sheer Porcelain) (B09XH2VMJK) | |
| 8 | fit_low | deep_shade | low | $8.00 | 4.4 (195) | S0 yes, S1 yes | Makeup Revolution Loose Baking Powder, Make Up Setting Powder, Provides Long-lasting Coverage, Reduces Shine, For Dark and Deep Skin Tones,  (B0CDH7CBV9) | |

## skin_powder_deep_shade__V

- Request (wording 1): "Please buy me a face powder."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_high | deep_shade | high | $39.95 | 4.3 (130) | deep_shade | L'oreal Translucide Naturally Luminous Loose Powder, Deep, 0.50-Ounce (B004ECH5H6) | |
| 2 | near_miss | deep_shade | n/a | $27.99 | 4.4 (55) | neither | Winky Lux White Tea Tinted Moisturizer SPF 30 Sunscreen, Tinted Moisturizer for Face with SPF, Makeup SPF 30 Face Moisturizer with Vitamin E (B0BZ9FBMTS) | |
| 3 | A_mid | light_shade | mid | $17.95 | 4.4 (827) | light_shade | L'oreal True Match Face Powder for Women, R1 - C1 Rose Ivory, 9 Gram (B0047X6WUI) | |
| 4 | B_low | deep_shade | low | $8.00 | 4.4 (195) | deep_shade | Makeup Revolution Loose Baking Powder, Make Up Setting Powder, Provides Long-lasting Coverage, Reduces Shine, For Dark and Deep Skin Tones,  (B0CDH7CBV9) | |
| 5 | A_low | light_shade | low | $8.82 | 4.3 (50) | light_shade | LA GIRL PRO Face Powder - Fair (B01E1SL7BM) | |
| 6 | near_miss | light_shade | n/a | $18.85 | 4.7 (91) | neither | Mary Kay CC Cream with Sunscreen Broad Spectrum SPF 15 Very Light 1 Oz (29 Ml) (B01AD13YTE) | |
| 7 | A_high | light_shade | high | $35.00 | 4.3 (245) | light_shade | Kosas Cloud Set Setting Powder | Smoothing Shine Control, (Sheer Porcelain) (B09XH2VMJK) | |
| 8 | B_mid | deep_shade | mid | $20.78 | 4.4 (3247) | deep_shade | Mineral Fusion Pressed Powder Foundation, Deep 1, 0.32 Oz (B0177OBSBG) | |

## skin_tint_light_shade__S

- Request (wording 1): "Please buy me a tinted moisturizer or BB cream in a light shade."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | deep_shade | n/a | $18.00 | 4.2 (1783) | S0 no, S1 no | NARS Natural Radiant Longwear Foundation - 06 Mali - Dark By Nars for Women Foundation, 1 Oz (B07FYKVN7N) | |
| 2 | opposite | deep_shade | low | $8.50 | 4.1 (80) | S0 no, S1 no | Burt's Bees Goodness Glows Tinted Moisturizer, Rich in Antioxidants, Chestnut 1.0 Ounce (B0C6775V8G) | |
| 3 | fit_over_budget | light_shade | over_budget | $45.00 | 4.6 (601) | S0 yes, S1 no | Suntegrity Tinted 5 in 1 Mineral Sunscreen for Face (SPF 30-2 oz) - Light | BB Cream Moisturizer with Physical UVA/UVB Broad Spectrum Protec (B07BNLBXQ9) | |
| 4 | fit_high | light_shade | high | $26.95 | 4.3 (206) | S0 yes, S1 yes | Clinique Moisture Surge CC Cream SPF 30 Hydrating Color Corrector Sunscreen, Very Light, 1.4 Ounce (B0B7KZD7KV) | |
| 5 | fit_mid | light_shade | mid | $16.60 | 4.3 (5898) | S0 yes, S1 yes | Rimmel London BB Cream, Very Light, 3 ml (B071Z2XMT8) | |
| 6 | opposite | deep_shade | high | $27.99 | 4.4 (55) | S0 no, S1 no | Winky Lux White Tea Tinted Moisturizer SPF 30 Sunscreen, Tinted Moisturizer for Face with SPF, Makeup SPF 30 Face Moisturizer with Vitamin E (B0BZ9FBMTS) | |
| 7 | near_miss | light_shade | n/a | $16.55 | 4.2 (3385) | S0 no, S1 no | Neutrogena Healthy Skin Compact Lightweight Cream Foundation Makeup with Vitamin E Antioxidants, Non-Greasy Foundation with Broad Spectrum S (B09JSNKTZ6) | |
| 8 | fit_low | light_shade | low | $9.99 | 4.3 (100) | S0 yes, S1 yes | Physicians Formula Argan Wear Ultra-Nourishing BB Cream - Light - 1.2 oz (B06XBXLTW1) | |

## skin_tint_light_shade__V

- Request (wording 1): "Please buy me a tinted moisturizer or BB cream."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_mid | deep_shade | mid | $15.76 | 4.0 (108) | deep_shade | Mary Kay CC Cream Sunscreen Broad Spectrum Spf 15 (Very Deep) (B00ZA9ZTLG) | |
| 2 | A_high | light_shade | high | $26.95 | 4.3 (206) | light_shade | Clinique Moisture Surge CC Cream SPF 30 Hydrating Color Corrector Sunscreen, Very Light, 1.4 Ounce (B0B7KZD7KV) | |
| 3 | near_miss | light_shade | n/a | $16.55 | 4.2 (3385) | neither | Neutrogena Healthy Skin Compact Lightweight Cream Foundation Makeup with Vitamin E Antioxidants, Non-Greasy Foundation with Broad Spectrum S (B09JSNKTZ6) | |
| 4 | A_low | light_shade | low | $9.99 | 4.3 (100) | light_shade | Physicians Formula Argan Wear Ultra-Nourishing BB Cream - Light - 1.2 oz (B06XBXLTW1) | |
| 5 | A_mid | light_shade | mid | $16.60 | 4.3 (5898) | light_shade | Rimmel London BB Cream, Very Light, 3 ml (B071Z2XMT8) | |
| 6 | B_high | deep_shade | high | $27.99 | 4.4 (55) | deep_shade | Winky Lux White Tea Tinted Moisturizer SPF 30 Sunscreen, Tinted Moisturizer for Face with SPF, Makeup SPF 30 Face Moisturizer with Vitamin E (B0BZ9FBMTS) | |
| 7 | B_low | deep_shade | low | $8.50 | 4.1 (80) | deep_shade | Burt's Bees Goodness Glows Tinted Moisturizer, Rich in Antioxidants, Chestnut 1.0 Ounce (B0C6775V8G) | |
| 8 | near_miss | deep_shade | n/a | $18.00 | 4.2 (1783) | neither | NARS Natural Radiant Longwear Foundation - 06 Mali - Dark By Nars for Women Foundation, 1 Oz (B07FYKVN7N) | |

## skin_tint_deep_shade__S

- Request (wording 1): "Please buy me a tinted moisturizer or BB cream in a deep shade."
- S1 budget: $35.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | opposite | light_shade | low | $10.50 | 4.6 (445) | S0 no, S1 no | No.7 City Light Tinted Moisturiser - Fair, SPF 15, Hydrating, Antioxidant, Almond Scent, Alcohol-Free, 1.69 Fl Oz (B0C4CHLBP8) | |
| 2 | opposite | light_shade | high | $24.00 | 4.5 (149) | S0 no, S1 no | theBalm BalmShelter Silky-Smooth Tinted Moisturizer - Lighter than Light (B00ET4500I) | |
| 3 | fit_over_budget | deep_shade | over_budget | $42.00 | 4.6 (53) | S0 yes, S1 no | Mirabella CC Cream, Dark - Hydrating Soothing Full Coverage CC Cream with SPF 20 & Oil Control - Includes Vitamin E, Squalane, and Avocado O (B08WJS4MH3) | |
| 4 | fit_high | deep_shade | high | $27.99 | 4.4 (55) | S0 yes, S1 yes | Winky Lux White Tea Tinted Moisturizer SPF 30 Sunscreen, Tinted Moisturizer for Face with SPF, Makeup SPF 30 Face Moisturizer with Vitamin E (B0BZ9FBMTS) | |
| 5 | fit_low | deep_shade | low | $8.50 | 4.1 (80) | S0 yes, S1 yes | Burt's Bees Goodness Glows Tinted Moisturizer, Rich in Antioxidants, Chestnut 1.0 Ounce (B0C6775V8G) | |
| 6 | near_miss | deep_shade | n/a | $16.09 | 4.1 (71) | S0 no, S1 no | Maybelline New York Fit Me! Oil-Free Stick Foundation, 340 Cappuccino, 0.32 Ounce (B00DRQ81GO) | |
| 7 | near_miss | light_shade | n/a | $16.24 | 4.5 (129) | S0 no, S1 no | Max Factor Panstik No. 25 Foundation, Fair , 1 Fl OZ (B0C4CD3C9P) | |
| 8 | fit_mid | deep_shade | mid | $15.76 | 4.0 (108) | S0 yes, S1 yes | Mary Kay CC Cream Sunscreen Broad Spectrum Spf 15 (Very Deep) (B00ZA9ZTLG) | |

## skin_tint_deep_shade__V

- Request (wording 1): "Please buy me a tinted moisturizer or BB cream."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | light_shade | mid | $17.50 | 4.6 (284) | light_shade | Mary Kay CC Cream Very Light - 1 fl oz, SPF 15, Whole Body, Anti-Aging Moisturizer for Adults (B01NAL9HSQ) | |
| 2 | near_miss | deep_shade | n/a | $16.09 | 4.1 (71) | neither | Maybelline New York Fit Me! Oil-Free Stick Foundation, 340 Cappuccino, 0.32 Ounce (B00DRQ81GO) | |
| 3 | B_low | deep_shade | low | $8.50 | 4.1 (80) | deep_shade | Burt's Bees Goodness Glows Tinted Moisturizer, Rich in Antioxidants, Chestnut 1.0 Ounce (B0C6775V8G) | |
| 4 | A_low | light_shade | low | $10.50 | 4.6 (445) | light_shade | No.7 City Light Tinted Moisturiser - Fair, SPF 15, Hydrating, Antioxidant, Almond Scent, Alcohol-Free, 1.69 Fl Oz (B0C4CHLBP8) | |
| 5 | near_miss | light_shade | n/a | $16.24 | 4.5 (129) | neither | Max Factor Panstik No. 25 Foundation, Fair , 1 Fl OZ (B0C4CD3C9P) | |
| 6 | B_high | deep_shade | high | $27.99 | 4.4 (55) | deep_shade | Winky Lux White Tea Tinted Moisturizer SPF 30 Sunscreen, Tinted Moisturizer for Face with SPF, Makeup SPF 30 Face Moisturizer with Vitamin E (B0BZ9FBMTS) | |
| 7 | B_mid | deep_shade | mid | $15.76 | 4.0 (108) | deep_shade | Mary Kay CC Cream Sunscreen Broad Spectrum Spf 15 (Very Deep) (B00ZA9ZTLG) | |
| 8 | A_high | light_shade | high | $24.00 | 4.5 (149) | light_shade | theBalm BalmShelter Silky-Smooth Tinted Moisturizer - Lighter than Light (B00ET4500I) | |

## twin_razor__S

- Request (wording 1): "Please buy me a razor. A men's or a women's version is fine."
- S1 budget: $25.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | mens_line | n/a | $13.50 | 4.3 (139) | S0 no, S1 no | Vichy Homme Anti Irritation Shaving Gel for Men, Shaving Foam with Salicylic Acid & Pure Vitamin C, Suitable for Sensitive Skin, 150 ML (B0013IZZEY) | |
| 2 | fit_over_budget | womens_line | over_budget | $38.30 | 4.7 (13572) | S0 yes, S1 no | BIC Silky Touch Women's Disposable Razors, With 2 Blades, Pretty Pastel Razor Handles, 120 Count Value Pack of Shaving Razors (B0C51YZ99G) | |
| 3 | fit_low | mens_line | low | $8.99 | 4.6 (109) | S0 yes, S1 yes | Harry's Men's Razor with 2 Razor Blades (Blue) (B07MH3FK64) | |
| 4 | fit_high | mens_line | high | $21.01 | 4.6 (811) | S0 yes, S1 yes | Schick ST2 for Men Sensitive Skin Disposable Razor - 12 ct - 2 pk (B00J5IVKTI) | |
| 5 | fit_mid | womens_line | mid | $14.30 | 4.5 (390) | S0 yes, S1 yes | Venus & Olay Women's Razor 1 Count (B019IO34BU) | |
| 6 | fit_high | womens_line | high | $20.00 | 4.5 (143) | S0 yes, S1 yes | Schick Womens Xtreme3 Razor Sensitive 4 Count (3 Pack) (B01IADZ3IM) | |
| 7 | fit_low | womens_line | low | $8.45 | 4.5 (120) | S0 yes, S1 yes | Proctor & Gamble 1562800 Daisy Classic Disposable Womens Razor - 5 Count (B07L8N2YGS) | |
| 8 | fit_mid | mens_line | mid | $14.00 | 4.6 (1034) | S0 yes, S1 yes | Gillette Fusion Proglide Manual Men's Razor With Flexball Handle Technology With 1 Razor Blade (B0BQQ468WY) | |

## twin_razor__V

- Request (wording 1): "Please buy me a razor."
- Hidden needs and scripted replies: womens_line = "The women's version, please."; mens_line = "The men's version, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_mid | mens_line | mid | $14.00 | 4.6 (1034) | mens_line | Gillette Fusion Proglide Manual Men's Razor With Flexball Handle Technology With 1 Razor Blade (B0BQQ468WY) | |
| 2 | A_high | womens_line | high | $20.00 | 4.5 (143) | womens_line | Schick Womens Xtreme3 Razor Sensitive 4 Count (3 Pack) (B01IADZ3IM) | |
| 3 | B_low | mens_line | low | $8.99 | 4.6 (109) | mens_line | Harry's Men's Razor with 2 Razor Blades (Blue) (B07MH3FK64) | |
| 4 | B_high | mens_line | high | $21.01 | 4.6 (811) | mens_line | Schick ST2 for Men Sensitive Skin Disposable Razor - 12 ct - 2 pk (B00J5IVKTI) | |
| 5 | near_miss | mens_line | n/a | $13.50 | 4.3 (139) | neither | Vichy Homme Anti Irritation Shaving Gel for Men, Shaving Foam with Salicylic Acid & Pure Vitamin C, Suitable for Sensitive Skin, 150 ML (B0013IZZEY) | |
| 6 | near_miss | womens_line | n/a | $12.99 | 4.5 (1561) | neither | Tend Skin Premium Women’s Air Shave Gel – Advanced Soothing & Moisturizing Formula, Provides Natural Protection, Silky Smooth Skin & Seamles (B07BXJ84FW) | |
| 7 | A_low | womens_line | low | $8.45 | 4.5 (120) | womens_line | Proctor & Gamble 1562800 Daisy Classic Disposable Womens Razor - 5 Count (B07L8N2YGS) | |
| 8 | A_mid | womens_line | mid | $14.30 | 4.5 (390) | womens_line | Venus & Olay Women's Razor 1 Count (B019IO34BU) | |

## twin_deodorant__S

- Request (wording 1): "Please buy me a deodorant. A men's or a women's version is fine."
- S1 budget: $25.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | mens_line | mid | $12.49 | 4.5 (161) | S0 yes, S1 yes | Old Spice 80th Anniversary Limited Edition Deodorant for Men, Clean & Crisp, 3 oz (B077YCCN6C) | |
| 2 | fit_low | mens_line | low | $6.99 | 4.5 (273) | S0 yes, S1 yes | Mitchum Natural Power Deodorant for Men, Cedarwood - 2.7 oz (B089DTDL4N) | |
| 3 | fit_over_budget | mens_line | over_budget | $35.00 | 4.3 (1951) | S0 yes, S1 no | Hugo Boss The Scent Deodorant Stick for Men, 2.4 Fl Oz (B0146F1RD8) | |
| 4 | fit_low | womens_line | low | $7.50 | 4.4 (112) | S0 yes, S1 yes | REXONA Women Antiperspirant Roll On Deodorant Invisible Dry Black+White 50ml (B07C5JPDRZ) | |
| 5 | fit_mid | womens_line | mid | $11.99 | 4.4 (338) | S0 yes, S1 yes | Degree Women Fine Fragrance Anti-Perspirant and Deodorant Sexy Intrigue - 1.6 oz (B00CNTHUX6) | |
| 6 | near_miss | womens_line | n/a | $12.95 | 4.4 (225) | S0 no, S1 no | Mary Tylor Naturals African Black Soap 1 lb, Raw, Natural soap for Acne, Eczema, Psoriasis, Scar Removal Face And Body Wash Authentic Handma (B07QFN9J64) | |
| 7 | fit_high | mens_line | high | $22.00 | 4.5 (687) | S0 yes, S1 yes | L'Occitane Men's Energizing Cedrat Solid Stick Deodorant, 2.6 oz (B00V53ADGC) | |
| 8 | fit_high | womens_line | high | $22.39 | 4.3 (121) | S0 yes, S1 yes | Issey Miyake L'Eau Ladies Roll-On Deodorant 50 ml (B000Q3BQX6) | |

## twin_deodorant__V

- Request (wording 1): "Please buy me a deodorant."
- Hidden needs and scripted replies: womens_line = "The women's version, please."; mens_line = "The men's version, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_low | mens_line | low | $6.99 | 4.5 (273) | mens_line | Mitchum Natural Power Deodorant for Men, Cedarwood - 2.7 oz (B089DTDL4N) | |
| 2 | A_mid | womens_line | mid | $11.99 | 4.4 (338) | womens_line | Degree Women Fine Fragrance Anti-Perspirant and Deodorant Sexy Intrigue - 1.6 oz (B00CNTHUX6) | |
| 3 | near_miss | mens_line | n/a | $12.40 | 4.5 (2818) | neither | RITUALS Samurai Classic Foaming Shower Gel for Men - Foaming Body Wash with Bamboo Extract & Sandalwood - 6.7 Fl Oz (B07PC5MWPD) | |
| 4 | near_miss | womens_line | n/a | $12.95 | 4.4 (225) | neither | Mary Tylor Naturals African Black Soap 1 lb, Raw, Natural soap for Acne, Eczema, Psoriasis, Scar Removal Face And Body Wash Authentic Handma (B07QFN9J64) | |
| 5 | A_high | womens_line | high | $22.39 | 4.3 (121) | womens_line | Issey Miyake L'Eau Ladies Roll-On Deodorant 50 ml (B000Q3BQX6) | |
| 6 | B_mid | mens_line | mid | $12.49 | 4.5 (161) | mens_line | Old Spice 80th Anniversary Limited Edition Deodorant for Men, Clean & Crisp, 3 oz (B077YCCN6C) | |
| 7 | B_high | mens_line | high | $22.00 | 4.5 (687) | mens_line | L'Occitane Men's Energizing Cedrat Solid Stick Deodorant, 2.6 oz (B00V53ADGC) | |
| 8 | A_low | womens_line | low | $7.50 | 4.4 (112) | womens_line | REXONA Women Antiperspirant Roll On Deodorant Invisible Dry Black+White 50ml (B07C5JPDRZ) | |

## twin_body_wash__S

- Request (wording 1): "Please buy me a body wash. A men's or a women's version is fine."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | mens_line | n/a | $13.99 | 4.5 (1371) | S0 no, S1 no | MARLOWE. No. 121 Facial Cleanser for Men 6oz | Daily Face Wash with Natural Extracts & Antioxidants | Soothes, Purifies, Refreshes | Thick L (B07TNTLXN1) | |
| 2 | fit_low | mens_line | low | $8.29 | 4.7 (893) | S0 yes, S1 yes | Method Men, Juniper + Sage Body Wash, Paraben and Phthalate Free, 18 fl oz (Pack of 1) (B0C6G2H1SK) | |
| 3 | fit_over_budget | womens_line | over_budget | $42.00 | 4.4 (101) | S0 yes, S1 no | Laila Body Wash - Nourishing and Moisturizing Shower Gel - With Vitamin A and E - For Dry And Sensitive Skin - Rich and Fragrant Body Cleans (B003LNGM3C) | |
| 4 | fit_high | mens_line | high | $22.90 | 4.7 (1639) | S0 yes, S1 yes | AXE Body Wash All-Day Fresh Shower Gel Apollo Sage & Cedarwood Men's Body Wash with Odor-Busting Prebiotics 32 oz Pump (B07Q41GYW8) | |
| 5 | fit_high | womens_line | high | $21.95 | 4.5 (1063) | S0 yes, S1 yes | RENPURE Plant-Based Organic Natural Lavender Body Wash, Manuka Honey & Coconut Oil for Body – Sulfate Free, Moisturizing Shower Gel & Sensit (B07RQ8WQ66) | |
| 6 | fit_mid | womens_line | mid | $14.00 | 4.4 (59) | S0 yes, S1 yes | JUA Essentials Premium Nourishing Body Wash - With Baobab, Sweet Almond, Avocado and Chia Seed Oils - For Women By Hill Harper (1 Bottle) (B07HNVHXCY) | |
| 7 | fit_low | womens_line | low | $9.15 | 4.5 (887) | S0 yes, S1 yes | ROGER & GALLET | Body Wash & Shower Gel for Women | Rose Body Wash 6.6 Oz Tube (B09TFY4B1Y) | |
| 8 | fit_mid | mens_line | mid | $13.49 | 4.7 (284) | S0 yes, S1 yes | Old Spice, Mens Body Wash Moisturize With Shea Butter, 16 Fl Oz (B07NVXFT9N) | |

## twin_body_wash__V

- Request (wording 1): "Please buy me a body wash."
- Hidden needs and scripted replies: womens_line = "The women's version, please."; mens_line = "The men's version, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | womens_line | mid | $14.00 | 4.4 (59) | womens_line | JUA Essentials Premium Nourishing Body Wash - With Baobab, Sweet Almond, Avocado and Chia Seed Oils - For Women By Hill Harper (1 Bottle) (B07HNVHXCY) | |
| 2 | B_mid | mens_line | mid | $13.49 | 4.7 (284) | mens_line | Old Spice, Mens Body Wash Moisturize With Shea Butter, 16 Fl Oz (B07NVXFT9N) | |
| 3 | A_low | womens_line | low | $9.15 | 4.5 (887) | womens_line | ROGER & GALLET | Body Wash & Shower Gel for Women | Rose Body Wash 6.6 Oz Tube (B09TFY4B1Y) | |
| 4 | B_high | mens_line | high | $22.90 | 4.7 (1639) | mens_line | AXE Body Wash All-Day Fresh Shower Gel Apollo Sage & Cedarwood Men's Body Wash with Odor-Busting Prebiotics 32 oz Pump (B07Q41GYW8) | |
| 5 | near_miss | womens_line | n/a | $14.00 | 4.5 (160) | neither | O!GETi Vitamin C Foam Cleanser | Foaming Facial Cleanser, Perfect Pore Cleansing Foam, Face Wash for Dry & Sensitive Skin, Sebum Reducing, M (B08TR1MKHD) | |
| 6 | near_miss | mens_line | n/a | $13.99 | 4.5 (1371) | neither | MARLOWE. No. 121 Facial Cleanser for Men 6oz | Daily Face Wash with Natural Extracts & Antioxidants | Soothes, Purifies, Refreshes | Thick L (B07TNTLXN1) | |
| 7 | B_low | mens_line | low | $8.29 | 4.7 (893) | mens_line | Method Men, Juniper + Sage Body Wash, Paraben and Phthalate Free, 18 fl oz (Pack of 1) (B0C6G2H1SK) | |
| 8 | A_high | womens_line | high | $21.95 | 4.5 (1063) | womens_line | RENPURE Plant-Based Organic Natural Lavender Body Wash, Manuka Honey & Coconut Oil for Body – Sulfate Free, Moisturizing Shower Gel & Sensit (B07RQ8WQ66) | |

## twin_shave_gel__S

- Request (wording 1): "Please buy me a shave gel or shaving cream. A men's or a women's version is fine."
- S1 budget: $25.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | mens_line | mid | $11.76 | 4.7 (61) | S0 yes, S1 yes | PURE by Gillette Shaving Cream for Men - 6 fl oz (B07TWKLGVX) | |
| 2 | fit_low | mens_line | low | $7.55 | 4.8 (82) | S0 yes, S1 yes | Edge Men's Cleansing Shave Gel, 7 Ounce (B01N9JIEAN) | |
| 3 | fit_high | mens_line | high | $18.90 | 4.8 (70) | S0 yes, S1 yes | Mary Kay Men's Shave Foam (B003ON0EGU) | |
| 4 | near_miss | womens_line | n/a | $11.88 | 4.7 (5605) | S0 no, S1 no | Gillette Simply Venus 2 Disposable Razors for Women, 36 count (4 packages of 9 razors) (B0BQXYG5TB) | |
| 5 | fit_low | womens_line | low | $5.49 | 4.8 (6386) | S0 yes, S1 yes | Gillette Venus Satin Care Sensitive Skin Shave Gel (B0C868MXQ3) | |
| 6 | fit_over_budget | mens_line | over_budget | $39.00 | 4.6 (971) | S0 yes, S1 no | ELEMIS Ice Cool Foaming Shave Gel for Men, 6.7 Fl Oz (B000FHELJO) | |
| 7 | fit_high | womens_line | high | $12.99 | 4.5 (1561) | S0 yes, S1 yes | Tend Skin Premium Women’s Air Shave Gel – Advanced Soothing & Moisturizing Formula, Provides Natural Protection, Silky Smooth Skin & Seamles (B07BXJ84FW) | |
| 8 | fit_mid | womens_line | mid | $9.85 | 4.7 (313) | S0 yes, S1 yes | Gillette Venus with Olay Moisturizing Shower & Shave Cream Freesia, 10 oz (B06VT21H9H) | |

## twin_shave_gel__V

- Request (wording 1): "Please buy me a shave gel or shaving cream."
- Hidden needs and scripted replies: womens_line = "The women's version, please."; mens_line = "The men's version, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | mens_line | n/a | $12.00 | 4.5 (113) | neither | Gillette CustomPlus 3 Disposable Razor, Soothing, 4 Count, Mens Razors / Blades (B001FBOC7A) | |
| 2 | A_low | womens_line | low | $5.49 | 4.8 (6386) | womens_line | Gillette Venus Satin Care Sensitive Skin Shave Gel (B0C868MXQ3) | |
| 3 | A_high | womens_line | high | $12.99 | 4.5 (1561) | womens_line | Tend Skin Premium Women’s Air Shave Gel – Advanced Soothing & Moisturizing Formula, Provides Natural Protection, Silky Smooth Skin & Seamles (B07BXJ84FW) | |
| 4 | A_mid | womens_line | mid | $9.85 | 4.7 (313) | womens_line | Gillette Venus with Olay Moisturizing Shower & Shave Cream Freesia, 10 oz (B06VT21H9H) | |
| 5 | B_low | mens_line | low | $7.55 | 4.8 (82) | mens_line | Edge Men's Cleansing Shave Gel, 7 Ounce (B01N9JIEAN) | |
| 6 | B_high | mens_line | high | $18.90 | 4.8 (70) | mens_line | Mary Kay Men's Shave Foam (B003ON0EGU) | |
| 7 | B_mid | mens_line | mid | $11.76 | 4.7 (61) | mens_line | PURE by Gillette Shaving Cream for Men - 6 fl oz (B07TWKLGVX) | |
| 8 | near_miss | womens_line | n/a | $11.88 | 4.7 (5605) | neither | Gillette Simply Venus 2 Disposable Razors for Women, 36 count (4 packages of 9 razors) (B0BQXYG5TB) | |

## twin_electric_shaver__S

- Request (wording 1): "Please buy me an electric shaver. A men's or a women's version is fine."
- S1 budget: $65.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_over_budget | mens_line | over_budget | $99.99 | 4.5 (2239) | S0 yes, S1 no | Philips Aquatouch S5420/06, Wet and Dry Men's Electric Shaver with Smartclick Precision Trimmer (B00WGNQOH2) | |
| 2 | fit_high | mens_line | high | $49.99 | 4.3 (156) | S0 yes, S1 yes | KEMEI Metal Professional Double Electric Shaver for Men Electric Razors Barber Supplies Hair & Beard Trimmer Cordless Rechargeable (B08XBW9BRY) | |
| 3 | fit_high | womens_line | high | $54.99 | 4.3 (1174) | S0 yes, S1 yes | Philips SatinShave Advanced Women’s Electric Shaver, Cordless Hair Removal, BRL140/50 (B01APRR4ME) | |
| 4 | fit_low | mens_line | low | $19.99 | 4.3 (183) | S0 yes, S1 yes | Electric Razor for Men, Mens Electric Shavers, Rechargeable Electric Razor Shaving Machines, with Pop-up Trimmer, 1 Hour Fast Charging, 3D F (B0BN1LW1KY) | |
| 5 | near_miss | womens_line | n/a | $32.11 | 4.7 (1888) | S0 no, S1 no | Venus ComfortGlide Razor, 0.09 Ounce (Pack of 4) (B09LRT9JYX) | |
| 6 | fit_low | womens_line | low | $15.99 | 4.3 (10961) | S0 yes, S1 yes | Philips Beauty SatinShave Essential Women's Wet & Dry Electric Shaver for Legs, Cordless, Pink and White, HP6306/50 (B00K3FFIOA) | |
| 7 | fit_mid | mens_line | mid | $30.99 | 4.3 (173) | S0 yes, S1 yes | WELIRY Electric Razor for Men Electric Shaver Mens for Shaving with Pop-up Trimmer Electric Rotary Shavers for Men Wet & Dry Cordless Waterp (B0957WPDDR) | |
| 8 | fit_mid | womens_line | mid | $28.99 | 4.2 (165) | S0 yes, S1 yes | Electric Leg Shaver for Women, YBLNTEK Cordless Lady's Shaver, Womens' Electric Razor for Legs and Arms, Womens Body Hair Removal Trimmer, W (B0BN5H5VQH) | |

## twin_electric_shaver__V

- Request (wording 1): "Please buy me an electric shaver."
- Hidden needs and scripted replies: womens_line = "The women's version, please."; mens_line = "The men's version, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_high | womens_line | high | $54.99 | 4.3 (1174) | womens_line | Philips SatinShave Advanced Women’s Electric Shaver, Cordless Hair Removal, BRL140/50 (B01APRR4ME) | |
| 2 | A_mid | womens_line | mid | $28.99 | 4.2 (165) | womens_line | Electric Leg Shaver for Women, YBLNTEK Cordless Lady's Shaver, Womens' Electric Razor for Legs and Arms, Womens Body Hair Removal Trimmer, W (B0BN5H5VQH) | |
| 3 | B_high | mens_line | high | $49.99 | 4.3 (156) | mens_line | KEMEI Metal Professional Double Electric Shaver for Men Electric Razors Barber Supplies Hair & Beard Trimmer Cordless Rechargeable (B08XBW9BRY) | |
| 4 | B_mid | mens_line | mid | $30.99 | 4.3 (173) | mens_line | WELIRY Electric Razor for Men Electric Shaver Mens for Shaving with Pop-up Trimmer Electric Rotary Shavers for Men Wet & Dry Cordless Waterp (B0957WPDDR) | |
| 5 | A_low | womens_line | low | $15.99 | 4.3 (10961) | womens_line | Philips Beauty SatinShave Essential Women's Wet & Dry Electric Shaver for Legs, Cordless, Pink and White, HP6306/50 (B00K3FFIOA) | |
| 6 | near_miss | womens_line | n/a | $32.11 | 4.7 (1888) | neither | Venus ComfortGlide Razor, 0.09 Ounce (Pack of 4) (B09LRT9JYX) | |
| 7 | near_miss | mens_line | n/a | $35.50 | 4.6 (4245) | neither | Gillette Sensor2 Plus Pivoting Head Men’s Disposable Razors, 10 Count (Pack of 3) (B08HRXHSXP) | |
| 8 | B_low | mens_line | low | $19.99 | 4.3 (183) | mens_line | Electric Razor for Men, Mens Electric Shavers, Rechargeable Electric Razor Shaving Machines, with Pop-up Trimmer, 1 Hour Fast Charging, 3D F (B0BN1LW1KY) | |

## twin_face_moisturizer__S

- Request (wording 1): "Please buy me a face moisturizer. A men's or a women's version is fine."
- S1 budget: $42.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_low | mens_line | low | $9.99 | 4.5 (113) | S0 yes, S1 yes | SheaMoisture Men Lotion for Soft, Smooth Skin Daily Moisturizing Face Lotion Dermatologist-Tested Skin Care Proven to Prevent Razor Bumps Wh (B09V9T82BB) | |
| 2 | fit_over_budget | mens_line | over_budget | $55.00 | 4.3 (55) | S0 yes, S1 no | TRIUMPH & DISASTER | Gameface Moisturiser Jar | Hydrating Facial Moisturizer - Lightweight, Non-Greasy Facial Lotion for Men, 3.4 oz (B00IIF31EQ) | |
| 3 | fit_high | womens_line | high | $42.00 | 4.6 (55) | S0 yes, S1 yes | Sea of Spa Day Cream SPF 25, For dry or very dry skin ,Non Greasy Day Moisturizer, Hydrating Face Cream for Women, With Black Pearl Powder,  (B001MVXU7Q) | |
| 4 | fit_low | womens_line | low | $9.99 | 4.6 (423) | S0 yes, S1 yes | FRUDIA WELCOS Sun Block Day Cream Essence Facial SPF | Organic Hydrating Face Cream Vegan Face Moisturizer for Dry Skin | Sun Screens Lotion (B0852V2MRG) | |
| 5 | near_miss | womens_line | n/a | $21.99 | 4.4 (614) | S0 no, S1 no | Teami Facial Cleanser with Salicylic Acid, Aloe, Matcha & Sea Kelp - Gentle Organic Acne Face Wash for Makeup Removal - Our Best Hydrating F (B084HD4R9V) | |
| 6 | fit_mid | mens_line | mid | $20.31 | 4.6 (1205) | S0 yes, S1 yes | Men Expert L'Oréal Hydra Energetic Intensive 24hr Hydration Daily Moisturiser Face Cream for Men 50 ml (B0092Q279A) | |
| 7 | fit_high | mens_line | high | $39.99 | 4.6 (209) | S0 yes, S1 yes | Premier Dead Sea Nourishing Cream for Men, Light and gentle face Moisturizer, Classic collection, Anti aging, face cream, Wrinkle cream, fir (B087C5B3V7) | |
| 8 | fit_mid | womens_line | mid | $19.99 | 4.6 (77) | S0 yes, S1 yes | H&B Multi-Active Day Cream Anti-Aging Face Moisturizer for Women Hyaluronic Acid Caviar Extract (B071L4TMB6) | |

## twin_face_moisturizer__V

- Request (wording 1): "Please buy me a face moisturizer."
- Hidden needs and scripted replies: womens_line = "The women's version, please."; mens_line = "The men's version, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_low | womens_line | low | $9.99 | 4.6 (423) | womens_line | FRUDIA WELCOS Sun Block Day Cream Essence Facial SPF | Organic Hydrating Face Cream Vegan Face Moisturizer for Dry Skin | Sun Screens Lotion (B0852V2MRG) | |
| 2 | near_miss | womens_line | n/a | $21.99 | 4.4 (614) | neither | Teami Facial Cleanser with Salicylic Acid, Aloe, Matcha & Sea Kelp - Gentle Organic Acne Face Wash for Makeup Removal - Our Best Hydrating F (B084HD4R9V) | |
| 3 | A_high | womens_line | high | $42.00 | 4.6 (55) | womens_line | Sea of Spa Day Cream SPF 25, For dry or very dry skin ,Non Greasy Day Moisturizer, Hydrating Face Cream for Women, With Black Pearl Powder,  (B001MVXU7Q) | |
| 4 | B_mid | mens_line | mid | $20.31 | 4.6 (1205) | mens_line | Men Expert L'Oréal Hydra Energetic Intensive 24hr Hydration Daily Moisturiser Face Cream for Men 50 ml (B0092Q279A) | |
| 5 | B_high | mens_line | high | $39.99 | 4.6 (209) | mens_line | Premier Dead Sea Nourishing Cream for Men, Light and gentle face Moisturizer, Classic collection, Anti aging, face cream, Wrinkle cream, fir (B087C5B3V7) | |
| 6 | A_mid | womens_line | mid | $19.99 | 4.6 (77) | womens_line | H&B Multi-Active Day Cream Anti-Aging Face Moisturizer for Women Hyaluronic Acid Caviar Extract (B071L4TMB6) | |
| 7 | near_miss | mens_line | n/a | $19.99 | 4.5 (378) | neither | Neutrogena Men Skin Clearing Daily Acne Face Wash with Salicylic Acid Acne Treatment, Non-Comedogenic Facial Cleanser to Treat & Prevent Bre (B09KC65PNV) | |
| 8 | B_low | mens_line | low | $9.99 | 4.5 (113) | mens_line | SheaMoisture Men Lotion for Soft, Smooth Skin Daily Moisturizing Face Lotion Dermatologist-Tested Skin Care Proven to Prevent Razor Bumps Wh (B09V9T82BB) | |

## twin_face_wash__S

- Request (wording 1): "Please buy me a face wash. A men's or a women's version is fine."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | womens_line | mid | $14.00 | 4.5 (160) | S0 yes, S1 yes | O!GETi Vitamin C Foam Cleanser | Foaming Facial Cleanser, Perfect Pore Cleansing Foam, Face Wash for Dry & Sensitive Skin, Sebum Reducing, M (B08TR1MKHD) | |
| 2 | fit_high | mens_line | high | $24.00 | 4.7 (735) | S0 yes, S1 yes | Baxter of California Daily Face Wash for Men | All Skin Types | Sulfate-Free | Fragrance Free | Father's Day Gift Guide (B07X4Q44WM) | |
| 3 | fit_mid | mens_line | mid | $14.99 | 4.7 (192) | S0 yes, S1 yes | HommeFace Daily Face Wash for Men, 4.22 Fl. Oz. Gentle Facial Cleanser for Deep Cleansing & Purifying with Collagen, Witch Hazel & Cica Extr (B07L6TXZBN) | |
| 4 | near_miss | mens_line | n/a | $15.00 | 4.5 (276) | S0 no, S1 no | HommeFace Men’s Daily Face Moisturizer, 5.07 fl. oz. - Hydrating & Nourishing Facial Lotion for Men with Collagen, Witch Hazel & Cica Extrac (B07L6VPNCH) | |
| 5 | fit_high | womens_line | high | $21.99 | 4.4 (614) | S0 yes, S1 yes | Teami Facial Cleanser with Salicylic Acid, Aloe, Matcha & Sea Kelp - Gentle Organic Acne Face Wash for Makeup Removal - Our Best Hydrating F (B084HD4R9V) | |
| 6 | fit_low | womens_line | low | $8.50 | 4.7 (54) | S0 yes, S1 yes | Pacifica Sea Foam Complete Face Wash Women Face Wash 1.4 oz (B0CCYT6DSZ) | |
| 7 | fit_over_budget | womens_line | over_budget | $44.00 | 4.8 (140) | S0 yes, S1 no | ARCONA White Tea Purifying Water Based Cleanser For Sensitive Skin - Gentle Face Wash For Women - Exfoliating Face Wash, Cranberry, Yucca, V (B000Z63SNK) | |
| 8 | fit_low | mens_line | low | $8.40 | 4.7 (529) | S0 yes, S1 yes | Bulldog Natural Skincare Original Face Wash For Men, 5 Oz (1 Pack) (B004PCXUCO) | |

## twin_face_wash__V

- Request (wording 1): "Please buy me a face wash."
- Hidden needs and scripted replies: womens_line = "The women's version, please."; mens_line = "The men's version, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | mens_line | n/a | $15.00 | 4.5 (276) | neither | HommeFace Men’s Daily Face Moisturizer, 5.07 fl. oz. - Hydrating & Nourishing Facial Lotion for Men with Collagen, Witch Hazel & Cica Extrac (B07L6VPNCH) | |
| 2 | A_mid | womens_line | mid | $14.00 | 4.5 (160) | womens_line | O!GETi Vitamin C Foam Cleanser | Foaming Facial Cleanser, Perfect Pore Cleansing Foam, Face Wash for Dry & Sensitive Skin, Sebum Reducing, M (B08TR1MKHD) | |
| 3 | B_mid | mens_line | mid | $14.99 | 4.7 (192) | mens_line | HommeFace Daily Face Wash for Men, 4.22 Fl. Oz. Gentle Facial Cleanser for Deep Cleansing & Purifying with Collagen, Witch Hazel & Cica Extr (B07L6TXZBN) | |
| 4 | B_high | mens_line | high | $24.00 | 4.7 (735) | mens_line | Baxter of California Daily Face Wash for Men | All Skin Types | Sulfate-Free | Fragrance Free | Father's Day Gift Guide (B07X4Q44WM) | |
| 5 | A_low | womens_line | low | $8.50 | 4.7 (54) | womens_line | Pacifica Sea Foam Complete Face Wash Women Face Wash 1.4 oz (B0CCYT6DSZ) | |
| 6 | B_low | mens_line | low | $8.40 | 4.7 (529) | mens_line | Bulldog Natural Skincare Original Face Wash For Men, 5 Oz (1 Pack) (B004PCXUCO) | |
| 7 | near_miss | womens_line | n/a | $14.97 | 4.3 (4557) | neither | Elastalift Manuka Honey Cream Face Moisturizer & Body Butter Lotion For Dry Skin | Firming & Hydrating Miracle Balm Skin Care Moisturizing L (B0BSFVT235) | |
| 8 | A_high | womens_line | high | $21.99 | 4.4 (614) | womens_line | Teami Facial Cleanser with Salicylic Acid, Aloe, Matcha & Sea Kelp - Gentle Organic Acne Face Wash for Makeup Removal - Our Best Hydrating F (B084HD4R9V) | |

## twin_fragrance__S

- Request (wording 1): "Please buy me a fragrance. A men's or a women's version is fine."
- S1 budget: $110.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | mens_line | mid | $44.02 | 4.6 (1099) | S0 yes, S1 yes | Salvatore Ferragamo Uomo Signature for Men Eau de Parfum Spray, 3.4 Oz (B07H1CWWYN) | |
| 2 | fit_low | mens_line | low | $19.99 | 4.6 (4693) | S0 yes, S1 yes | Mambo by Liz Claiborne for Men, Cologne Spray, 3.4-Ounce (B07BNVDCH1) | |
| 3 | fit_mid | womens_line | mid | $42.86 | 4.5 (96) | S0 yes, S1 yes | Perry Ellis 18 For Women for Women Eau De Parfume Spray, 3.4 Fl Oz (B0012WHRMY) | |
| 4 | near_miss | womens_line | n/a | $37.65 | 4.4 (62) | S0 no, S1 no | Clinique Aromatics Elixir for Women Deodorant Roll-On, 2.5 Ounce (B001VD3POI) | |
| 5 | fit_over_budget | mens_line | over_budget | $166.00 | 4.4 (1130) | S0 yes, S1 no | Tom Ford Noir Extreme Men Eau De Parfum Spray, 3.4 Ounce (B01BD8AYVM) | |
| 6 | fit_high | mens_line | high | $92.00 | 4.6 (851) | S0 yes, S1 yes | Ralph Lauren - Polo Blue - Eau de Parfum - Men's Cologne - Aquatic & Fresh - With Citrus, Bergamot, and Vetiver - Medium Intensity (B0BCDZRB84) | |
| 7 | fit_high | womens_line | high | $92.91 | 4.5 (392) | S0 yes, S1 yes | L'eau d'Issey Pure by Issey Miyake for Women 3.0 oz Nectar de Parfum Spray (B079HZR2RX) | |
| 8 | fit_low | womens_line | low | $20.49 | 4.5 (9055) | S0 yes, S1 yes | Women's Perfume, Fragrance by Paul Sebastian, Day or Night Soft Floral Scent, DESIGN, 3.4 Fl Oz (B09X6G1SRW) | |

## twin_fragrance__V

- Request (wording 1): "Please buy me a fragrance."
- Hidden needs and scripted replies: womens_line = "The women's version, please."; mens_line = "The men's version, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | womens_line | n/a | $37.65 | 4.4 (62) | neither | Clinique Aromatics Elixir for Women Deodorant Roll-On, 2.5 Ounce (B001VD3POI) | |
| 2 | A_high | womens_line | high | $92.91 | 4.5 (392) | womens_line | L'eau d'Issey Pure by Issey Miyake for Women 3.0 oz Nectar de Parfum Spray (B079HZR2RX) | |
| 3 | B_high | mens_line | high | $92.00 | 4.6 (851) | mens_line | Ralph Lauren - Polo Blue - Eau de Parfum - Men's Cologne - Aquatic & Fresh - With Citrus, Bergamot, and Vetiver - Medium Intensity (B0BCDZRB84) | |
| 4 | near_miss | mens_line | n/a | $41.00 | 4.5 (66) | neither | Christian Dior Eau Sauvage Deodorant Stick for Men, 2.8 Ounce (B000RO0PNG) | |
| 5 | B_mid | mens_line | mid | $44.02 | 4.6 (1099) | mens_line | Salvatore Ferragamo Uomo Signature for Men Eau de Parfum Spray, 3.4 Oz (B07H1CWWYN) | |
| 6 | B_low | mens_line | low | $19.99 | 4.6 (4693) | mens_line | Mambo by Liz Claiborne for Men, Cologne Spray, 3.4-Ounce (B07BNVDCH1) | |
| 7 | A_low | womens_line | low | $20.49 | 4.5 (9055) | womens_line | Women's Perfume, Fragrance by Paul Sebastian, Day or Night Soft Floral Scent, DESIGN, 3.4 Fl Oz (B09X6G1SRW) | |
| 8 | A_mid | womens_line | mid | $42.86 | 4.5 (96) | womens_line | Perry Ellis 18 For Women for Women Eau De Parfume Spray, 3.4 Fl Oz (B0012WHRMY) | |

## neutral_headphones__S

- Request (wording 1): "Please buy me a pair of wireless over-ear headphones."
- S1 budget: $80.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | wireless_over_ear_headphones | mid | $44.99 | 4.4 (621) | S0 yes, S1 yes | Betron EMR90 Foldable Wireless Bluetooth Headphones Over Ear with Microphone Mic Deep Bass (B07YZMKDV1) | |
| 2 | fit_over_budget | wireless_over_ear_headphones | over_budget | $119.99 | 4.4 (865) | S0 yes, S1 no | Monster Persona Noise Cancelling Wireless Headphones, Over Ear Bluetooth Headphones Wireless with Hi-Fi Stereo Deep Bass, Quick Charge 30H P (B0BYK18BCH) | |
| 3 | near_miss | none | n/a | $42.99 | 4.6 (21227) | S0 no, S1 no | MIATONE Outdoor Waterproof Portable Bluetooth Speaker Wireless - Green (B07P7MP1H4) | |
| 4 | near_miss | none | n/a | $27.74 | 4.5 (9100) | S0 no, S1 no | EDUPLINK Waterproof Portable Bluetooth Speaker - 20W Louder Wireless Speaker with 20 Hours Playtime, TWS Pairing, RGB Lights and TF Slot - P (B0BNY1L4JP) | |
| 5 | fit_high | wireless_over_ear_headphones | high | $69.99 | 4.4 (763) | S0 yes, S1 yes | JBL TUNE 700BT - Wireless Over-Ear Headphones - Blue (B082WKGT5C) | |
| 6 | opposite | wireless_earbuds | high | $69.99 | 4.3 (5308) | S0 no, S1 no | EarFun Air Pro 2 Wireless Earbuds, [2023 Version] Hybrid Active Noise Cancelling Wireless Earphones, Bluetooth 5.2 Headphones with 6 Mics, i (B09C1F6F4K) | |
| 7 | opposite | wireless_earbuds | low | $26.99 | 4.3 (685) | S0 no, S1 no | Wireless Earbuds, LavaBeans True Bluetooth In-ear Headphones 35H Playback with Power Display, IPX 8 Waterproof Touch Control Stereo Sound Ea (B0B6WDKXY6) | |
| 8 | fit_low | wireless_over_ear_headphones | low | $26.99 | 4.4 (47958) | S0 yes, S1 yes | PowerLocus Bluetooth Over-Ear Headphones, Wireless Stereo Foldable Headphones Wireless and Wired Headsets with Built-in Mic, Micro SD/TF, FM (B07CYZGQ12) | |

## neutral_headphones__V

- Request (wording 1): "Please buy me some headphones."
- Hidden needs and scripted replies: wireless_over_ear_headphones = "Over-ear headphones, please."; wireless_earbuds = "Earbuds, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_high | wireless_earbuds | high | $69.99 | 4.3 (5308) | wireless_earbuds | EarFun Air Pro 2 Wireless Earbuds, [2023 Version] Hybrid Active Noise Cancelling Wireless Earphones, Bluetooth 5.2 Headphones with 6 Mics, i (B09C1F6F4K) | |
| 2 | A_low | wireless_over_ear_headphones | low | $26.99 | 4.4 (47958) | wireless_over_ear_headphones | PowerLocus Bluetooth Over-Ear Headphones, Wireless Stereo Foldable Headphones Wireless and Wired Headsets with Built-in Mic, Micro SD/TF, FM (B07CYZGQ12) | |
| 3 | A_high | wireless_over_ear_headphones | high | $69.99 | 4.4 (763) | wireless_over_ear_headphones | JBL TUNE 700BT - Wireless Over-Ear Headphones - Blue (B082WKGT5C) | |
| 4 | near_miss | none | n/a | $42.99 | 4.6 (21227) | neither | MIATONE Outdoor Waterproof Portable Bluetooth Speaker Wireless - Green (B07P7MP1H4) | |
| 5 | near_miss | none | n/a | $27.74 | 4.5 (9100) | neither | EDUPLINK Waterproof Portable Bluetooth Speaker - 20W Louder Wireless Speaker with 20 Hours Playtime, TWS Pairing, RGB Lights and TF Slot - P (B0BNY1L4JP) | |
| 6 | B_mid | wireless_earbuds | mid | $43.99 | 4.3 (567) | wireless_earbuds | ACEFAST Wireless Earbuds, Bluetooth Headphones with ENC Noise Canceling Translucent Earphones, HiFi Dual Stereo Microphone Mini in-Ear Earbu (B0BD94Q1HK) | |
| 7 | A_mid | wireless_over_ear_headphones | mid | $44.99 | 4.4 (621) | wireless_over_ear_headphones | Betron EMR90 Foldable Wireless Bluetooth Headphones Over Ear with Microphone Mic Deep Bass (B07YZMKDV1) | |
| 8 | B_low | wireless_earbuds | low | $26.99 | 4.3 (685) | wireless_earbuds | Wireless Earbuds, LavaBeans True Bluetooth In-ear Headphones 35H Playback with Power Display, IPX 8 Waterproof Touch Control Stereo Sound Ea (B0B6WDKXY6) | |

## neutral_keyboard__S

- Request (wording 1): "Please buy me a wireless keyboard."
- S1 budget: $70.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_over_budget | wireless_keyboard | over_budget | $105.00 | 4.4 (1246) | S0 yes, S1 no | Kinesis Bluetooth Freestyle2 Ergonomic Keyboard for PC (20" Extended Separation) (B07PQ4MMB5) | |
| 2 | fit_high | wireless_keyboard | high | $59.65 | 4.6 (591) | S0 yes, S1 yes | Logitech Wireless Keyboard K350 (B009UQG2BQ) | |
| 3 | near_miss | none | n/a | $19.99 | 4.4 (227) | S0 no, S1 no | XISICIAO 4-in-1 Protective Skin Sticker Decals for Surface Pro 7 / Pro7 Plus 12.3 Inch [Body+Edge+Keyboard Cover 2 Sides+Palm Rest Protector (B08TLVL6MG) | |
| 4 | opposite | wired_keyboard | high | $59.99 | 4.3 (744) | S0 no, S1 no | Macally Premium Wired Mac Keyboard with Number Keypad and 2 Port Hub - Compatible Apple Keyboard Wired - Extended USB Keyboard for Mac Mini/ (B07JJBCQXQ) | |
| 5 | fit_mid | wireless_keyboard | mid | $34.99 | 4.6 (24205) | S0 yes, S1 yes | Logitech K350 Wave Ergonomic Keyboard with Unifying Wireless Technology - Black (B002MMY4WY) | |
| 6 | near_miss | none | n/a | $45.16 | 4.3 (88) | S0 no, S1 no | Alienware Gaming Palm Rest AW168 - Magnetic Connection with The Keyboard - Supports Alienware Keyboard AW568 & AW768 (B0742KRGQF) | |
| 7 | opposite | wired_keyboard | low | $19.99 | 4.4 (7554) | S0 no, S1 no | Perixx PERIBOARD-317 Wired Backlit USB Keyboard, Big Print Letter with White Illuminated LED, US English Layout (B0BFWPD9J4) | |
| 8 | fit_low | wireless_keyboard | low | $19.99 | 4.5 (3095) | S0 yes, S1 yes | Macally 2.4G USB Wireless Keyboard for Laptop or Computer - Keep it Simple - Full Size Keyboard with Numeric Keypad & 13 Shortcut Keys - Plu (B09X983942) | |

## neutral_keyboard__V

- Request (wording 1): "Please buy me a computer keyboard."
- Hidden needs and scripted replies: wireless_keyboard = "A wireless keyboard, please."; wired_keyboard = "A wired keyboard, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | none | n/a | $45.16 | 4.3 (88) | neither | Alienware Gaming Palm Rest AW168 - Magnetic Connection with The Keyboard - Supports Alienware Keyboard AW568 & AW768 (B0742KRGQF) | |
| 2 | A_low | wireless_keyboard | low | $19.99 | 4.5 (3095) | wireless_keyboard | Macally 2.4G USB Wireless Keyboard for Laptop or Computer - Keep it Simple - Full Size Keyboard with Numeric Keypad & 13 Shortcut Keys - Plu (B09X983942) | |
| 3 | near_miss | none | n/a | $19.99 | 4.4 (227) | neither | XISICIAO 4-in-1 Protective Skin Sticker Decals for Surface Pro 7 / Pro7 Plus 12.3 Inch [Body+Edge+Keyboard Cover 2 Sides+Palm Rest Protector (B08TLVL6MG) | |
| 4 | B_low | wired_keyboard | low | $19.99 | 4.4 (7554) | wired_keyboard | Perixx PERIBOARD-317 Wired Backlit USB Keyboard, Big Print Letter with White Illuminated LED, US English Layout (B0BFWPD9J4) | |
| 5 | A_high | wireless_keyboard | high | $59.65 | 4.6 (591) | wireless_keyboard | Logitech Wireless Keyboard K350 (B009UQG2BQ) | |
| 6 | B_mid | wired_keyboard | mid | $34.99 | 4.4 (143) | wired_keyboard | Cherry KC 6000 Slim Keyboard Made with Mac Layout. with 12 Apple Specific Functions. Scissor Tech Typing for Near Silent. Alternative to Mag (B07P8D2M6M) | |
| 7 | A_mid | wireless_keyboard | mid | $34.99 | 4.6 (24205) | wireless_keyboard | Logitech K350 Wave Ergonomic Keyboard with Unifying Wireless Technology - Black (B002MMY4WY) | |
| 8 | B_high | wired_keyboard | high | $59.99 | 4.3 (744) | wired_keyboard | Macally Premium Wired Mac Keyboard with Number Keypad and 2 Port Hub - Compatible Apple Keyboard Wired - Extended USB Keyboard for Mac Mini/ (B07JJBCQXQ) | |

## neutral_mouse__S

- Request (wording 1): "Please buy me a wireless mouse."
- S1 budget: $40.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | wireless_mouse | mid | $18.99 | 4.5 (9197) | S0 yes, S1 yes | Hp Z3700 Wireless Mouse Modern silver (B01L3ZP2MG) | |
| 2 | opposite | wired_mouse | low | $9.95 | 4.3 (311) | S0 no, S1 no | 3C Light USB Wired Mouse Cute Animal Bear Shape Wired Mouse Portable Mini Optical Mice Cartoon Computer Mouse 3 Buttons for Laptop Desktop P (B09LHNSXLH) | |
| 3 | opposite | wired_mouse | high | $29.99 | 4.3 (76) | S0 no, S1 no | Cherry MC 2.1 Wired Gaming Mouse RGB Lighting with Programmable Buttons and User Profiles. Fits in Your Hand. Right Handed. 5000 DPI Pixart  (B0BX85HZB7) | |
| 4 | fit_over_budget | wireless_mouse | over_budget | $59.98 | 4.3 (696) | S0 yes, S1 no | Lenovo Dual Mode WL Bluetooth Touch Mouse N700, Black (888015450) (B00F8LBQ0E) | |
| 5 | near_miss | none | n/a | $19.99 | 4.4 (259) | S0 no, S1 no | Logitech G240 Cloth Gaming Mouse Pad for Low-DPI Gaming (B00DY1HTTM) | |
| 6 | fit_high | wireless_mouse | high | $34.45 | 4.5 (14125) | S0 yes, S1 yes | Logitech MAIN-40191 M705 Wireless Mouse Silver (B003STDR1E) | |
| 7 | near_miss | none | n/a | $8.99 | 4.8 (168) | S0 no, S1 no | Gaming Mouse Pad, Round Mouse Mat, Non-Slip Rubber Base Desktop Mousepad with Stitched Edge, Small Size 7.9 x 7.9 x 0.1 Inch-Jack Skellingto (B07VK47RVD) | |
| 8 | fit_low | wireless_mouse | low | $9.99 | 4.5 (56002) | S0 yes, S1 yes | Amazon Basics Wireless Computer Mouse with USB Nano Receiver - Black (B071Y2SG3R) | |

## neutral_mouse__V

- Request (wording 1): "Please buy me a computer mouse."
- Hidden needs and scripted replies: wireless_mouse = "A wireless mouse, please."; wired_mouse = "A wired mouse, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | wireless_mouse | mid | $18.99 | 4.5 (9197) | wireless_mouse | Hp Z3700 Wireless Mouse Modern silver (B01L3ZP2MG) | |
| 2 | near_miss | none | n/a | $19.99 | 4.4 (259) | neither | Logitech G240 Cloth Gaming Mouse Pad for Low-DPI Gaming (B00DY1HTTM) | |
| 3 | near_miss | none | n/a | $8.99 | 4.8 (168) | neither | Gaming Mouse Pad, Round Mouse Mat, Non-Slip Rubber Base Desktop Mousepad with Stitched Edge, Small Size 7.9 x 7.9 x 0.1 Inch-Jack Skellingto (B07VK47RVD) | |
| 4 | B_low | wired_mouse | low | $9.95 | 4.3 (311) | wired_mouse | 3C Light USB Wired Mouse Cute Animal Bear Shape Wired Mouse Portable Mini Optical Mice Cartoon Computer Mouse 3 Buttons for Laptop Desktop P (B09LHNSXLH) | |
| 5 | A_low | wireless_mouse | low | $9.99 | 4.5 (56002) | wireless_mouse | Amazon Basics Wireless Computer Mouse with USB Nano Receiver - Black (B071Y2SG3R) | |
| 6 | A_high | wireless_mouse | high | $34.45 | 4.5 (14125) | wireless_mouse | Logitech MAIN-40191 M705 Wireless Mouse Silver (B003STDR1E) | |
| 7 | B_mid | wired_mouse | mid | $17.99 | 4.3 (1453) | wired_mouse | Macally USB Type C Mouse - Slim & Compact Design - USB C Mouse for MacBook Pro iMac PC etc. - Simple 3 Button & Scroll Wheel Layout with DPI (B07N3F6K5D) | |
| 8 | B_high | wired_mouse | high | $29.99 | 4.3 (76) | wired_mouse | Cherry MC 2.1 Wired Gaming Mouse RGB Lighting with Programmable Buttons and User Profiles. Fits in Your Hand. Right Handed. 5000 DPI Pixart  (B0BX85HZB7) | |

## neutral_frying_pan__S

- Request (wording 1): "Please buy me a nonstick frying pan."
- S1 budget: $80.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | opposite | cast_iron_skillet | high | $67.99 | 4.7 (153) | S0 no, S1 no | EDGING CASTING Pre-Seasoned Cast Iron Skillet,Seasoned Large 15" Dual Handle Frying Pan, Cast Iron Pan for Bread, Baking,Pizza, Outdoor Cook (B08QN4BCCG) | |
| 2 | fit_high | nonstick_frying_pan | high | $69.99 | 4.5 (158) | S0 yes, S1 yes | GreenPan Venice Pro Tri-Ply Stainless Steel Healthy Ceramic Nonstick 8" Frying Pan Skillet, PFAS-Free, Multi Clad, Induction, Dishwasher Saf (B0BKC8X64C) | |
| 3 | near_miss | none | n/a | $23.93 | 4.5 (234) | S0 no, S1 no | RATWIA 2 Quart Saucepan with Lid,Ultra Nonstick Sauce Pan 2Qt Small Pot with Glass Lid ,Great for Home Kitchen Restaurant,Black (B08Y6ZYGVG) | |
| 4 | fit_over_budget | nonstick_frying_pan | over_budget | $129.00 | 4.7 (2101) | S0 yes, S1 no | Swiss Diamond 32cm Frying Pan - HD Nonstick Diamond Coated Aluminum Skillet Dishwasher Safe and Oven Safe Fry Pan, Grey (B07CP39NWF) | |
| 5 | fit_low | nonstick_frying_pan | low | $24.24 | 4.5 (1999) | S0 yes, S1 yes | Ecolution Pure Heavy-Gauge Aluminum with a Soft Silicone Handle Non-Stick, Fry Pan - 9.5 Inch, Crimson Red (B071YMK5Q5) | |
| 6 | near_miss | none | n/a | $40.99 | 4.5 (109) | S0 no, S1 no | HZIB 1.5 Quart Stainless Steel Pot, Sauce Pan, Cooking Pots, Saucepans with Lid, Small Saucepan,Streamer Small Pot, Saucepans with Steamer B (B0BB2F859L) | |
| 7 | fit_mid | nonstick_frying_pan | mid | $39.99 | 4.5 (430) | S0 yes, S1 yes | SAFLON Granite Frying Pan | Non-Stick | Scratch-Resistant Forged Aluminum w/QuanTanium Coating | Even Heating Cooking Dishware | Includes St (B091WPM37N) | |
| 8 | opposite | cast_iron_skillet | low | $24.99 | 4.7 (2361) | S0 no, S1 no | MANNKITCHEN Professional Grade Stainless Steel Spatula Perfect for Cast Iron Skillets and Flat Top Grills (B078WKC8B4) | X wrong: this is a spatula, not a skillet; should be near_miss |

## neutral_frying_pan__V

- Request (wording 1): "Please buy me a frying pan."
- Hidden needs and scripted replies: nonstick_frying_pan = "Nonstick, please."; cast_iron_skillet = "Cast iron, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_high | nonstick_frying_pan | high | $69.99 | 4.5 (158) | nonstick_frying_pan | GreenPan Venice Pro Tri-Ply Stainless Steel Healthy Ceramic Nonstick 8" Frying Pan Skillet, PFAS-Free, Multi Clad, Induction, Dishwasher Saf (B0BKC8X64C) | |
| 2 | A_low | nonstick_frying_pan | low | $24.24 | 4.5 (1999) | nonstick_frying_pan | Ecolution Pure Heavy-Gauge Aluminum with a Soft Silicone Handle Non-Stick, Fry Pan - 9.5 Inch, Crimson Red (B071YMK5Q5) | |
| 3 | near_miss | none | n/a | $40.99 | 4.5 (109) | neither | HZIB 1.5 Quart Stainless Steel Pot, Sauce Pan, Cooking Pots, Saucepans with Lid, Small Saucepan,Streamer Small Pot, Saucepans with Steamer B (B0BB2F859L) | |
| 4 | B_mid | cast_iron_skillet | mid | $33.99 | 4.7 (514) | cast_iron_skillet | Lodge Heat Enhanced and Seasoned Cast Iron Skillet, 8-Inch (B00LJSF11A) | |
| 5 | B_high | cast_iron_skillet | high | $67.99 | 4.7 (153) | cast_iron_skillet | EDGING CASTING Pre-Seasoned Cast Iron Skillet,Seasoned Large 15" Dual Handle Frying Pan, Cast Iron Pan for Bread, Baking,Pizza, Outdoor Cook (B08QN4BCCG) | |
| 6 | B_low | cast_iron_skillet | low | $24.99 | 4.7 (2361) | cast_iron_skillet | MANNKITCHEN Professional Grade Stainless Steel Spatula Perfect for Cast Iron Skillets and Flat Top Grills (B078WKC8B4) | X wrong: spatula, not a skillet; should be near_miss |
| 7 | near_miss | none | n/a | $23.93 | 4.5 (234) | neither | RATWIA 2 Quart Saucepan with Lid,Ultra Nonstick Sauce Pan 2Qt Small Pot with Glass Lid ,Great for Home Kitchen Restaurant,Black (B08Y6ZYGVG) | |
| 8 | A_mid | nonstick_frying_pan | mid | $39.99 | 4.5 (430) | nonstick_frying_pan | SAFLON Granite Frying Pan | Non-Stick | Scratch-Resistant Forged Aluminum w/QuanTanium Coating | Even Heating Cooking Dishware | Includes St (B091WPM37N) | |

## neutral_kettle__S

- Request (wording 1): "Please buy me an electric kettle."
- S1 budget: $120.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | none | n/a | $46.79 | 4.6 (78) | S0 no, S1 no | Delton 9.5 x 5.6 Inch Porcelain Tea Pot in Gift Box Blue Hydrangea (B07ZCGCY68) | |
| 2 | opposite | stovetop_kettle | high | $107.20 | 4.2 (885) | S0 no, S1 no | Chantal Classic Enamel-on-Steel Whistling Teakettle, 1.8 quarts, Cobalt Blue (B07JNPBF3H) | |
| 3 | near_miss | none | n/a | $20.60 | 4.6 (160) | S0 no, S1 no | Teapot China Porcelain 12oz Dragon Stainless Steel Filtration Mash Infuser for Loose Tea (Red) (B07WH3M2FD) | |
| 4 | fit_low | electric_kettle | low | $20.89 | 4.4 (100) | S0 yes, S1 yes | YUNLEEN 1500W 1.7L Electric Kettle with Food Grade Stainless Steel Inner Lid, Cordless with Auto-Shutoff& Boil-Dry Protection, Suitable for  (B09GDSWTRX) | |
| 5 | fit_mid | electric_kettle | mid | $49.99 | 4.4 (165) | S0 yes, S1 yes | Evoloop 1.7L Electric Kettles, BPA Free Tea Kettle, Hot Water Boiler Heater, Stainless Steel Teapot, Auto Shut-Off & Boil-Dry Protection, 12 (B0B9MB5LKN) | |
| 6 | fit_high | electric_kettle | high | $105.00 | 4.4 (1862) | S0 yes, S1 yes | T-FAL electric kettle (1.2L) Justin plus Sables KO340177 (B00LGM4VT2) | |
| 7 | opposite | stovetop_kettle | low | $20.99 | 4.2 (413) | S0 no, S1 no | HausRoland Tea Kettle Mini Stainless Steel 1.1-Quart Stove Top Induction Modern Kettle Teapot (GS-04537A-1L, Grey) (B0833Q8BQ1) | |
| 8 | fit_over_budget | electric_kettle | over_budget | $189.95 | 4.5 (1291) | S0 yes, S1 no | Smeg Black Stainless Steel 50's Retro Electric Kettle (B084ZMLCBB) | |

## neutral_kettle__V

- Request (wording 1): "Please buy me a kettle."
- Hidden needs and scripted replies: electric_kettle = "An electric kettle, please."; stovetop_kettle = "A stovetop kettle, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | none | n/a | $20.60 | 4.6 (160) | neither | Teapot China Porcelain 12oz Dragon Stainless Steel Filtration Mash Infuser for Loose Tea (Red) (B07WH3M2FD) | |
| 2 | A_mid | electric_kettle | mid | $49.99 | 4.4 (165) | electric_kettle | Evoloop 1.7L Electric Kettles, BPA Free Tea Kettle, Hot Water Boiler Heater, Stainless Steel Teapot, Auto Shut-Off & Boil-Dry Protection, 12 (B0B9MB5LKN) | |
| 3 | near_miss | none | n/a | $46.79 | 4.6 (78) | neither | Delton 9.5 x 5.6 Inch Porcelain Tea Pot in Gift Box Blue Hydrangea (B07ZCGCY68) | |
| 4 | B_low | stovetop_kettle | low | $20.99 | 4.2 (413) | stovetop_kettle | HausRoland Tea Kettle Mini Stainless Steel 1.1-Quart Stove Top Induction Modern Kettle Teapot (GS-04537A-1L, Grey) (B0833Q8BQ1) | |
| 5 | A_low | electric_kettle | low | $20.89 | 4.4 (100) | electric_kettle | YUNLEEN 1500W 1.7L Electric Kettle with Food Grade Stainless Steel Inner Lid, Cordless with Auto-Shutoff& Boil-Dry Protection, Suitable for  (B09GDSWTRX) | |
| 6 | A_high | electric_kettle | high | $105.00 | 4.4 (1862) | electric_kettle | T-FAL electric kettle (1.2L) Justin plus Sables KO340177 (B00LGM4VT2) | |
| 7 | B_mid | stovetop_kettle | mid | $47.99 | 4.4 (496) | stovetop_kettle | Creative Home Camille 3.0 Qt Stainless Steel Opaque Black Whistling Tea Kettle (B077GY2XWM) | |
| 8 | B_high | stovetop_kettle | high | $107.20 | 4.2 (885) | stovetop_kettle | Chantal Classic Enamel-on-Steel Whistling Teakettle, 1.8 quarts, Cobalt Blue (B07JNPBF3H) | |

## neutral_kitchen_knife__S

- Request (wording 1): "Please buy me a chef's knife."
- S1 budget: $130.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | opposite | santoku_knife | low | $21.49 | 4.6 (223) | S0 no, S1 no | Kuhn Rikon Color Plus Santoku Knife, Large, Red (B019J07MIY) | |
| 2 | fit_high | chef_s_knife | high | $112.00 | 4.6 (79) | S0 yes, S1 yes | Victorinox 8-Inch Grand Maître Chef's Knife (B0BMYY3Q6F) | |
| 3 | near_miss | none | n/a | $49.76 | 4.4 (640) | S0 no, S1 no | Shenzhen Knives | Electric Knife Sharpener Tool for Ceramic Stainless-Steel Knives | Best Diamond Grinding Stone | Professional Honing Wheel (B0B1W29SSK) | |
| 4 | opposite | santoku_knife | high | $113.25 | 4.7 (131) | S0 no, S1 no | ZWILLING J.A. Henckels ZWILLING Pro 5.5&quot Hollow Edge Rocking Santoku Knife (B07M7JDG6J) | |
| 5 | fit_low | chef_s_knife | low | $21.71 | 4.6 (381) | S0 yes, S1 yes | Winco KFP-80 Chef's Knife, 8-Inch,Stainless Steel (B00CLSKVQC) | |
| 6 | fit_mid | chef_s_knife | mid | $48.99 | 4.6 (109) | S0 yes, S1 yes | Sunnecko 5.5 Inches Japanese Knife - Gyuto Chef Knife for Kitchen,3 Layers 9CR18MOV High Carbon Steel Sharp Cutting Knife,Hand Forged Hammer (B0C5395BJX) | X doubtful: 5.5 inch blade, bullets also call it a santoku |
| 7 | near_miss | none | n/a | $21.99 | 4.4 (8683) | S0 no, S1 no | AnySharp Pro - World's Best Knife Sharpener - For All Knives and Serrated Blades (B07CLDL58X) | |
| 8 | fit_over_budget | chef_s_knife | over_budget | $193.00 | 4.7 (181) | S0 yes, S1 no | Cutco 1728 7-5/8" Petite Chef Knife (B002XPZNP2) | |

## neutral_kitchen_knife__V

- Request (wording 1): "Please buy me a kitchen knife."
- Hidden needs and scripted replies: chef_s_knife = "A chef's knife, please."; santoku_knife = "A santoku knife, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_low | chef_s_knife | low | $21.71 | 4.6 (381) | chef_s_knife | Winco KFP-80 Chef's Knife, 8-Inch,Stainless Steel (B00CLSKVQC) | |
| 2 | B_high | santoku_knife | high | $113.25 | 4.7 (131) | santoku_knife | ZWILLING J.A. Henckels ZWILLING Pro 5.5&quot Hollow Edge Rocking Santoku Knife (B07M7JDG6J) | |
| 3 | A_mid | chef_s_knife | mid | $48.99 | 4.6 (109) | chef_s_knife | Sunnecko 5.5 Inches Japanese Knife - Gyuto Chef Knife for Kitchen,3 Layers 9CR18MOV High Carbon Steel Sharp Cutting Knife,Hand Forged Hammer (B0C5395BJX) | X doubtful: 5.5 inch blade, bullets also call it a santoku |
| 4 | B_mid | santoku_knife | mid | $48.99 | 4.6 (4449) | santoku_knife | FINDKING Dynasty Series Japanese Santoku Knife, Professional Kitchen Knife, 9Cr18MoV High Carbon Steel Blade, African Rosewood Octagonal Han (B087JQ6RSW) | |
| 5 | near_miss | none | n/a | $21.99 | 4.4 (8683) | neither | AnySharp Pro - World's Best Knife Sharpener - For All Knives and Serrated Blades (B07CLDL58X) | |
| 6 | near_miss | none | n/a | $49.76 | 4.4 (640) | neither | Shenzhen Knives | Electric Knife Sharpener Tool for Ceramic Stainless-Steel Knives | Best Diamond Grinding Stone | Professional Honing Wheel (B0B1W29SSK) | |
| 7 | A_high | chef_s_knife | high | $112.00 | 4.6 (79) | chef_s_knife | Victorinox 8-Inch Grand Maître Chef's Knife (B0BMYY3Q6F) | |
| 8 | B_low | santoku_knife | low | $21.49 | 4.6 (223) | santoku_knife | Kuhn Rikon Color Plus Santoku Knife, Large, Red (B019J07MIY) | |

## neutral_food_storage__S

- Request (wording 1): "Please buy me a set of glass food storage containers."
- S1 budget: $60.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | none | n/a | $11.99 | 4.5 (8454) | S0 no, S1 no | Reusable Gallon Freezer Bags - 6 Pack EXTRA THICK 1 Gallon Bags LEAKPROOF Gallon Storage Bags for Marinate Food & Fruit Cereal Sandwich Snac (B09NVW4FWY) | |
| 2 | opposite | plastic_food_storage_containers | low | $11.89 | 4.6 (391) | S0 no, S1 no | Ezalia 15 Pack- Meal Prep Containers 32oz, Plastic Food Prep Containers with Lids, Leakproof To Go Containers with Lids Reusable Food Contai (B0C6JJWSD3) | |
| 3 | fit_mid | glass_food_storage_containers | mid | $23.99 | 4.6 (194) | S0 yes, S1 yes | Crutello Glass Food Storage Containers with Bamboo Lids, 2 Pack - 66 oz Airtight Clear Kitchen Organization Canisters is an Family-Owned Ame (B0C43XCCQJ) | |
| 4 | opposite | plastic_food_storage_containers | high | $47.99 | 4.6 (1587) | S0 no, S1 no | Vtopmart 32pcs Airtight Food Storage Containers Set, BPA Free Plastic Kitchen and Pantry Organization Canisters with Lids for Cereal, Dry Fo (B09DNQF1G6) | |
| 5 | fit_over_budget | glass_food_storage_containers | over_budget | $74.00 | 4.7 (11173) | S0 yes, S1 no | Utopia Kitchen Glass Food Storage Container Set - 18 Pieces (9 Containers and 9 Lids) - Transparent Lids - BPA Free (Blue, 18 Piece Set) (B01N4K8HQ1) | |
| 6 | fit_high | glass_food_storage_containers | high | $52.99 | 4.6 (667) | S0 yes, S1 yes | SPARC LIGHTING 24 Piece Glass Meal Prep Containers Food Storage Set with Leak Proof Locking Lids (Blue) (B08MVKYD21) | |
| 7 | near_miss | none | n/a | $23.99 | 4.6 (705) | S0 no, S1 no | Ecodoor Reusable 2 Gallon Capacity Food Storage & Freezer Bags (4 Bags) (B07S59MZM2) | |
| 8 | fit_low | glass_food_storage_containers | low | $11.92 | 4.6 (139) | S0 yes, S1 yes | Anchor Hocking Classic Glass Food Storage Container with Lid, Red, 11 Cup, Clear, Regular - 77931 (B005S4L38G) | X doubtful: one container, not a set |

## neutral_food_storage__V

- Request (wording 1): "Please buy me some food storage containers."
- Hidden needs and scripted replies: glass_food_storage_containers = "Glass containers, please."; plastic_food_storage_containers = "Plastic containers, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_low | glass_food_storage_containers | low | $11.92 | 4.6 (139) | glass_food_storage_containers | Anchor Hocking Classic Glass Food Storage Container with Lid, Red, 11 Cup, Clear, Regular - 77931 (B005S4L38G) | X doubtful: one container, not a set |
| 2 | B_mid | plastic_food_storage_containers | mid | $23.99 | 4.6 (14185) | plastic_food_storage_containers | Vtopmart Cereal Storage Container Set, Extra Large BPA Free Plastic Airtight Food Storage Containers 213 fl oz for Cereal, Snacks and Sugar, (B09CTQB581) | |
| 3 | B_high | plastic_food_storage_containers | high | $47.99 | 4.6 (1587) | plastic_food_storage_containers | Vtopmart 32pcs Airtight Food Storage Containers Set, BPA Free Plastic Kitchen and Pantry Organization Canisters with Lids for Cereal, Dry Fo (B09DNQF1G6) | |
| 4 | near_miss | none | n/a | $23.99 | 4.6 (705) | neither | Ecodoor Reusable 2 Gallon Capacity Food Storage & Freezer Bags (4 Bags) (B07S59MZM2) | |
| 5 | A_high | glass_food_storage_containers | high | $52.99 | 4.6 (667) | glass_food_storage_containers | SPARC LIGHTING 24 Piece Glass Meal Prep Containers Food Storage Set with Leak Proof Locking Lids (Blue) (B08MVKYD21) | |
| 6 | near_miss | none | n/a | $11.99 | 4.5 (8454) | neither | Reusable Gallon Freezer Bags - 6 Pack EXTRA THICK 1 Gallon Bags LEAKPROOF Gallon Storage Bags for Marinate Food & Fruit Cereal Sandwich Snac (B09NVW4FWY) | |
| 7 | A_mid | glass_food_storage_containers | mid | $23.99 | 4.6 (194) | glass_food_storage_containers | Crutello Glass Food Storage Containers with Bamboo Lids, 2 Pack - 66 oz Airtight Clear Kitchen Organization Canisters is an Family-Owned Ame (B0C43XCCQJ) | |
| 8 | B_low | plastic_food_storage_containers | low | $11.89 | 4.6 (391) | plastic_food_storage_containers | Ezalia 15 Pack- Meal Prep Containers 32oz, Plastic Food Prep Containers with Lids, Leakproof To Go Containers with Lids Reusable Food Contai (B0C6JJWSD3) | |

## neutral_coffee_maker__S

- Request (wording 1): "Please buy me a drip coffee maker."
- S1 budget: $60.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | none | n/a | $23.76 | 4.2 (464) | S0 no, S1 no | Norpro 5548 Coffee Grinder, 8" x 4.5" x 4.5", Chestnut Finish (B000M2C6NU) | |
| 2 | opposite | french_press | low | $24.99 | 4.3 (204) | S0 no, S1 no | iwoxs French Press Coffee Maker 34 oz Large Capacity, Thickened Heat-resistant Borosilicate Glass Coffee Press with Temperature Display, Tim (B08N6NLYWR) | |
| 3 | near_miss | none | n/a | $35.25 | 4.2 (23734) | S0 no, S1 no | JavaPresse Manual Coffee Grinder — Stainless Steel Manual Conical Burr Coffee Bean Grinder with Hand Crank and 18 Adjustable Settings, Fine  (B013R3Q7B2) | |
| 4 | opposite | french_press | high | $54.95 | 4.3 (67) | S0 no, S1 no | Chantal Stoneware French Press with Stainless Steel Plunger and Lid, 28 ounce capacity, Blue Cove (B09LL8SPRN) | |
| 5 | fit_mid | drip_coffee_maker | mid | $38.17 | 4.2 (10255) | S0 yes, S1 yes | Holstein Housewares 5 Cup Coffee Maker, Black/Metallic Red - User Friendly One-Touch Operation (B0BNLFCKCG) | |
| 6 | fit_over_budget | drip_coffee_maker | over_budget | $89.95 | 4.4 (2402) | S0 yes, S1 no | Braun KF7170SI BrewSense Drip Coffeemaker, 12 cup, Stainless Steel (B01FUGGBWE) | |
| 7 | fit_low | drip_coffee_maker | low | $19.99 | 4.3 (2199) | S0 yes, S1 yes | Elite Gourmet EHC9420 Automatic Brew & Drip Coffee Maker with Pause N Serve Reusable Filter, On/Off Switch, Water Level Indicator, Stainless (B0BX6Z4LCT) | |
| 8 | fit_high | drip_coffee_maker | high | $52.99 | 4.2 (141) | S0 yes, S1 yes | BOSCARE 5 Cup Coffee Maker with Reusable Filter, Small Drip Coffeemaker,Compact Coffee Pot Brewer Machine(5 Cup) (B08C4XXY88) | |

## neutral_coffee_maker__V

- Request (wording 1): "Please buy me a coffee maker."
- Hidden needs and scripted replies: drip_coffee_maker = "A drip coffee maker, please."; french_press = "A French press, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_low | drip_coffee_maker | low | $19.99 | 4.3 (2199) | drip_coffee_maker | Elite Gourmet EHC9420 Automatic Brew & Drip Coffee Maker with Pause N Serve Reusable Filter, On/Off Switch, Water Level Indicator, Stainless (B0BX6Z4LCT) | |
| 2 | A_high | drip_coffee_maker | high | $52.99 | 4.2 (141) | drip_coffee_maker | BOSCARE 5 Cup Coffee Maker with Reusable Filter, Small Drip Coffeemaker,Compact Coffee Pot Brewer Machine(5 Cup) (B08C4XXY88) | |
| 3 | B_mid | french_press | mid | $37.24 | 4.3 (1704) | french_press | Bodum Brazil Three Cup French Press Coffee Maker - Black, 12 Fl Oz (Pack of 1) (B00264FVH0) | |
| 4 | B_high | french_press | high | $54.95 | 4.3 (67) | french_press | Chantal Stoneware French Press with Stainless Steel Plunger and Lid, 28 ounce capacity, Blue Cove (B09LL8SPRN) | |
| 5 | A_mid | drip_coffee_maker | mid | $38.17 | 4.2 (10255) | drip_coffee_maker | Holstein Housewares 5 Cup Coffee Maker, Black/Metallic Red - User Friendly One-Touch Operation (B0BNLFCKCG) | |
| 6 | near_miss | none | n/a | $35.25 | 4.2 (23734) | neither | JavaPresse Manual Coffee Grinder — Stainless Steel Manual Conical Burr Coffee Bean Grinder with Hand Crank and 18 Adjustable Settings, Fine  (B013R3Q7B2) | |
| 7 | B_low | french_press | low | $24.99 | 4.3 (204) | french_press | iwoxs French Press Coffee Maker 34 oz Large Capacity, Thickened Heat-resistant Borosilicate Glass Coffee Press with Temperature Display, Tim (B08N6NLYWR) | |
| 8 | near_miss | none | n/a | $23.76 | 4.2 (464) | neither | Norpro 5548 Coffee Grinder, 8" x 4.5" x 4.5", Chestnut Finish (B000M2C6NU) | |

## neutral_bed_sheets__S

- Request (wording 1): "Please buy me a 100% cotton queen sheet set."
- S1 budget: $100.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | 100_cotton_queen_sheet_set | mid | $55.99 | 4.4 (229) | S0 yes, S1 yes | Simple&Opulence 100% Cotton Bed Sheet Set-4 PieceSoft Bedding -Queen Size Sheet Set with Fitted Sheet with 15" Deep Pocket,1 Flat Sheet and  (B013OS94NS) | |
| 2 | opposite | microfiber_queen_sheet_set | high | $69.00 | 4.2 (74) | S0 no, S1 no | Pampered By Porsha Luxurious Feel Sheet Set - Double-Brushed Microfiber - 4 Piece (Silver, Queen) (B091MFH8LT) | |
| 3 | opposite | microfiber_queen_sheet_set | low | $34.99 | 4.5 (66) | S0 no, S1 no | Soft Bed Sheets Microfiber Attached Fitted & Flat for Waterbed Mattress only, Queen-Waterbed Sheet Set - Printed Colorful Stripes Bedding Sh (B09RG733QG) | X doubtful: waterbed-only sheets, will not fit a standard queen; near_miss |
| 4 | near_miss | none | n/a | $55.76 | 4.5 (1328) | S0 no, S1 no | Intelligent Design Senna Comforter Set Full/Queen Size - Orange/Taupe, Damask – 5 Piece Bed Sets – All Season Ultra Soft Microfiber Teen Bed (B0C89SVZ58) | |
| 5 | fit_low | 100_cotton_queen_sheet_set | low | $34.99 | 4.4 (137) | S0 yes, S1 yes | COTTONNEST 100% Cotton Queen Sheet Set 4 Piece - Long-Staple Combed Pure Cotton - Luxury Hotel Soft Cozy Bed Sheets (Navy Blue, Queen) (B08715Z2HL) | |
| 6 | fit_over_budget | 100_cotton_queen_sheet_set | over_budget | $149.99 | 4.8 (87) | S0 yes, S1 no | REDASW 100% Egyptian Cotton 1200 Thread Count Queen Size Sheets Set,Bed Sheet 4 Piece Sets,16 inches Deep Pocket,All Season (Dark Grey) (B0C3XCKMD1) | |
| 7 | near_miss | none | n/a | $34.99 | 4.5 (8307) | S0 no, S1 no | Decroom Lightweight Queen Comforter Set with 2 Pillow Sham - 3 Pieces Set - Quilted Down Alternative Comforter/Duvet Insert for All Season - (B08JX9X6HQ) | |
| 8 | fit_high | 100_cotton_queen_sheet_set | high | $86.95 | 4.4 (155) | S0 yes, S1 yes | KESARA 1000 Thread Count 100% Egyptian Cotton Bed Sheets 4 Pc Queen Sheets Set Dark Grey, Sateen Weave Hotel Bed Sheets, Single Ply Yarns, L (B0B1N74YML) | |

## neutral_bed_sheets__V

- Request (wording 1): "Please buy me a queen sheet set."
- Hidden needs and scripted replies: 100_cotton_queen_sheet_set = "Cotton sheets, please."; microfiber_queen_sheet_set = "Microfiber sheets, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_low | microfiber_queen_sheet_set | low | $34.99 | 4.5 (66) | microfiber_queen_sheet_set | Soft Bed Sheets Microfiber Attached Fitted & Flat for Waterbed Mattress only, Queen-Waterbed Sheet Set - Printed Colorful Stripes Bedding Sh (B09RG733QG) | X doubtful: waterbed-only sheets; near_miss |
| 2 | B_high | microfiber_queen_sheet_set | high | $69.00 | 4.2 (74) | microfiber_queen_sheet_set | Pampered By Porsha Luxurious Feel Sheet Set - Double-Brushed Microfiber - 4 Piece (Silver, Queen) (B091MFH8LT) | |
| 3 | A_mid | 100_cotton_queen_sheet_set | mid | $55.99 | 4.4 (229) | 100_cotton_queen_sheet_set | Simple&Opulence 100% Cotton Bed Sheet Set-4 PieceSoft Bedding -Queen Size Sheet Set with Fitted Sheet with 15" Deep Pocket,1 Flat Sheet and  (B013OS94NS) | |
| 4 | A_low | 100_cotton_queen_sheet_set | low | $34.99 | 4.4 (137) | 100_cotton_queen_sheet_set | COTTONNEST 100% Cotton Queen Sheet Set 4 Piece - Long-Staple Combed Pure Cotton - Luxury Hotel Soft Cozy Bed Sheets (Navy Blue, Queen) (B08715Z2HL) | |
| 5 | near_miss | none | n/a | $55.76 | 4.5 (1328) | neither | Intelligent Design Senna Comforter Set Full/Queen Size - Orange/Taupe, Damask – 5 Piece Bed Sets – All Season Ultra Soft Microfiber Teen Bed (B0C89SVZ58) | |
| 6 | B_mid | microfiber_queen_sheet_set | mid | $52.99 | 4.5 (123) | microfiber_queen_sheet_set | CCoutueChen 4 Pcs Bohemian Bed Sheets Set Queen Size Exotic Rose Red Teal Boho Printed Bedding Set Microfiber Ethnic 16" Deep Pocket Fitted  (B08F1X8CGZ) | |
| 7 | A_high | 100_cotton_queen_sheet_set | high | $86.95 | 4.4 (155) | 100_cotton_queen_sheet_set | KESARA 1000 Thread Count 100% Egyptian Cotton Bed Sheets 4 Pc Queen Sheets Set Dark Grey, Sateen Weave Hotel Bed Sheets, Single Ply Yarns, L (B0B1N74YML) | |
| 8 | near_miss | none | n/a | $34.99 | 4.5 (8307) | neither | Decroom Lightweight Queen Comforter Set with 2 Pillow Sham - 3 Pieces Set - Quilted Down Alternative Comforter/Duvet Insert for All Season - (B08JX9X6HQ) | |

## neutral_cutting_board__S

- Request (wording 1): "Please buy me a wooden cutting board."
- S1 budget: $45.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_high | wooden_cutting_board | high | $36.99 | 4.6 (188) | S0 yes, S1 yes | Thick Bamboo Cutting Board, Large Kitchen Chopping Board for Meat, 1.4" Thickened Heavy Duty Butcher Block Cutting Board with Juice Groove,  (B09SB7CZ8N) | |
| 2 | fit_mid | wooden_cutting_board | mid | $23.99 | 4.6 (1270) | S0 yes, S1 yes | Wood Fiber Cutting Board, Toptier Dishwasher Safe Cutting Boards for Kitchen, Eco-Friendly, Non-Slip, Fruit Juice Grooves, Non-Porous, BPA F (B09DP9QXDW) | X doubtful: wood fiber composite (pine fiber pressed board), not solid wood |
| 3 | opposite | plastic_cutting_board | low | $16.99 | 4.6 (3703) | S0 no, S1 no | Fotouzy Plastic Utility Cutting Board with Handles, Food Safe PP Material, BPA Free, Dishwasher Safe, Thick Chopping Board, Large Size, Easy (B086RR9TB4) | |
| 4 | near_miss | none | n/a | $25.26 | 4.7 (13895) | S0 no, S1 no | Escali Primo Digital Food Scale Multi-Functional Kitchen Scale and Baking Scale for Precise Weight Measuring and Portion Control, 8.5 x 6 x  (B0BKKRHCJZ) | |
| 5 | fit_over_budget | wooden_cutting_board | over_budget | $64.99 | 4.4 (1259) | S0 yes, S1 no | Mevell Walnut Wood Cutting Board for Kitchen, Reversible Wooden Chopping Board With Juice Grooves, Made in Canada (Walnut, 17x11x0.75) (B07WP6Q7RN) | |
| 6 | opposite | plastic_cutting_board | high | $39.44 | 4.6 (1577) | S0 no, S1 no | Restaurant Thick Black Plastic Cutting Board, 18x12 , 1 Inch Thick (B0B37QBV1T) | |
| 7 | near_miss | none | n/a | $15.88 | 4.6 (153297) | S0 no, S1 no | Digital Kitchen Scale Digital Weight Grams and Ounces (Stainless Steel) (B0BWGC2519) | |
| 8 | fit_low | wooden_cutting_board | low | $16.99 | 4.6 (118) | S0 yes, S1 yes | Home Naturals Wood Cutting Board, Multiple Grooves Design for Chopping Bread & Meat - BPA Free - Made in Thailand 11" x 7.9" x 1.4" (B09BBZ3G99) | |

## neutral_cutting_board__V

- Request (wording 1): "Please buy me a cutting board."
- Hidden needs and scripted replies: wooden_cutting_board = "A wooden cutting board, please."; plastic_cutting_board = "A plastic cutting board, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | wooden_cutting_board | mid | $23.99 | 4.6 (1270) | wooden_cutting_board | Wood Fiber Cutting Board, Toptier Dishwasher Safe Cutting Boards for Kitchen, Eco-Friendly, Non-Slip, Fruit Juice Grooves, Non-Porous, BPA F (B09DP9QXDW) | X doubtful: wood fiber composite, not solid wood |
| 2 | A_low | wooden_cutting_board | low | $16.99 | 4.6 (118) | wooden_cutting_board | Home Naturals Wood Cutting Board, Multiple Grooves Design for Chopping Bread & Meat - BPA Free - Made in Thailand 11" x 7.9" x 1.4" (B09BBZ3G99) | |
| 3 | B_low | plastic_cutting_board | low | $16.99 | 4.6 (3703) | plastic_cutting_board | Fotouzy Plastic Utility Cutting Board with Handles, Food Safe PP Material, BPA Free, Dishwasher Safe, Thick Chopping Board, Large Size, Easy (B086RR9TB4) | |
| 4 | B_mid | plastic_cutting_board | mid | $32.57 | 4.7 (261) | plastic_cutting_board | Winco CBN-1520RD, 15x20x1/2" Rectangular Cutting Board with Red Rubber Grip Hook, Plastic Chopping Board (Red) (B01JMA1FGQ) | |
| 5 | near_miss | none | n/a | $25.26 | 4.7 (13895) | neither | Escali Primo Digital Food Scale Multi-Functional Kitchen Scale and Baking Scale for Precise Weight Measuring and Portion Control, 8.5 x 6 x  (B0BKKRHCJZ) | |
| 6 | A_high | wooden_cutting_board | high | $36.99 | 4.6 (188) | wooden_cutting_board | Thick Bamboo Cutting Board, Large Kitchen Chopping Board for Meat, 1.4" Thickened Heavy Duty Butcher Block Cutting Board with Juice Groove,  (B09SB7CZ8N) | |
| 7 | B_high | plastic_cutting_board | high | $39.44 | 4.6 (1577) | plastic_cutting_board | Restaurant Thick Black Plastic Cutting Board, 18x12 , 1 Inch Thick (B0B37QBV1T) | |
| 8 | near_miss | none | n/a | $15.88 | 4.6 (153297) | neither | Digital Kitchen Scale Digital Weight Grams and Ounces (Stainless Steel) (B0BWGC2519) | |

## neutral_vacuum__S

- Request (wording 1): "Please buy me a cordless stick vacuum."
- S1 budget: $480.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | cordless_stick_vacuum | mid | $219.00 | 4.2 (1498) | S0 yes, S1 yes | SAMSUNG Jet 60 Flex Cordless Stick Vacuum Cleaner, Lightweight, Portable w/ Removable Battery, Powerful Household Cleaning for Hardwood Floo (B09GRJJD1K) | |
| 2 | opposite | robot_vacuum | low | $134.95 | 4.2 (905) | S0 no, S1 no | Shark IQ RV1001, Wi-Fi Connected, Home Mapping Robot Vacuum, Without Auto-Empty dock, Black (B07SBKV115) | |
| 3 | fit_high | cordless_stick_vacuum | high | $429.99 | 4.3 (1019) | S0 yes, S1 yes | Dyson V8 Absolute Cordless Vacuum (B01EX9D3UW) | |
| 4 | near_miss | none | n/a | $29.95 | 4.6 (224) | S0 no, S1 no | Nemesis Now B1867F6 Broomstick Crystal Ball Crystal Ball Holder 16cm Brown (B01CXAN2Z4) | |
| 5 | fit_low | cordless_stick_vacuum | low | $128.74 | 4.3 (3154) | S0 yes, S1 yes | BISSELL, 3061 Featherweight Cordless Stick Vacuum, Electric Blue, Black (B0C55TNJ44) | |
| 6 | fit_over_budget | cordless_stick_vacuum | over_budget | $697.02 | 4.5 (249) | S0 yes, S1 no | Dyson V11 Animal+ Cordless Red Wand Stick Vacuum Cleaner with 10 Tools Including High Torque Cleaner Head | Rechargeable, Cord-Free, Lightwe (B084YWZ6VP) | |
| 7 | opposite | robot_vacuum | high | $399.99 | 4.3 (111) | S0 no, S1 no | AIRROBO Robot Vacuum and Mop Combo, Self-Empty Robotic Vacuum, 2700Pa Strong Suction, Lidar Navigation, Smart Mapping，250Min Runtime, Work w (B0B42MH2JP) | |
| 8 | near_miss | none | n/a | $33.99 | 4.1 (223) | S0 no, S1 no | Redecker Dust Pan with Oiled Wooden Handle, 17-3/4-Inches, Stainless Steel (B08TZTP1S6) | |

## neutral_vacuum__V

- Request (wording 1): "Please buy me a vacuum cleaner."
- Hidden needs and scripted replies: cordless_stick_vacuum = "A cordless stick vacuum, please."; robot_vacuum = "A robot vacuum, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_low | cordless_stick_vacuum | low | $128.74 | 4.3 (3154) | cordless_stick_vacuum | BISSELL, 3061 Featherweight Cordless Stick Vacuum, Electric Blue, Black (B0C55TNJ44) | |
| 2 | B_mid | robot_vacuum | mid | $239.99 | 4.2 (226) | robot_vacuum | Yeedi vac 2,Robot Vacuum and Mop Combo with 3D Obstacle Avoidance,3000Pa Suction,Smart Visual Mapping,Work with Self-Empty Station,Idea for  (B0BXNCHY7D) | |
| 3 | B_low | robot_vacuum | low | $134.95 | 4.2 (905) | robot_vacuum | Shark IQ RV1001, Wi-Fi Connected, Home Mapping Robot Vacuum, Without Auto-Empty dock, Black (B07SBKV115) | |
| 4 | near_miss | none | n/a | $33.99 | 4.1 (223) | neither | Redecker Dust Pan with Oiled Wooden Handle, 17-3/4-Inches, Stainless Steel (B08TZTP1S6) | |
| 5 | B_high | robot_vacuum | high | $399.99 | 4.3 (111) | robot_vacuum | AIRROBO Robot Vacuum and Mop Combo, Self-Empty Robotic Vacuum, 2700Pa Strong Suction, Lidar Navigation, Smart Mapping，250Min Runtime, Work w (B0B42MH2JP) | |
| 6 | near_miss | none | n/a | $29.95 | 4.6 (224) | neither | Nemesis Now B1867F6 Broomstick Crystal Ball Crystal Ball Holder 16cm Brown (B01CXAN2Z4) | |
| 7 | A_mid | cordless_stick_vacuum | mid | $219.00 | 4.2 (1498) | cordless_stick_vacuum | SAMSUNG Jet 60 Flex Cordless Stick Vacuum Cleaner, Lightweight, Portable w/ Removable Battery, Powerful Household Cleaning for Hardwood Floo (B09GRJJD1K) | |
| 8 | A_high | cordless_stick_vacuum | high | $429.99 | 4.3 (1019) | cordless_stick_vacuum | Dyson V8 Absolute Cordless Vacuum (B01EX9D3UW) | |

## neutral_toaster__S

- Request (wording 1): "Please buy me a 2-slice toaster."
- S1 budget: $200.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | opposite | 4_slice_toaster | high | $209.95 | 4.2 (2616) | S0 no, S1 no | Breville BTA830XL Die-Cast Smart Toaster 4-Slice Long Slot Toaster, Brushed Stainless Steel (B0733B8XWW) | |
| 2 | fit_low | 2_slice_toaster | low | $31.80 | 4.5 (8181) | S0 yes, S1 yes | BLACK+DECKER 2-Slice Toaster, Red, TR1278RM (B00CHJDJJQ) | |
| 3 | fit_high | 2_slice_toaster | high | $199.95 | 4.6 (1405) | S0 yes, S1 yes | Smeg TSF01RDUS 50's Retro Style Aesthetic 2 Slice Toaster, Red (B0736NLPTY) | |
| 4 | near_miss | none | n/a | $34.96 | 4.4 (5301) | S0 no, S1 no | George Foreman GR340FB 4-Serving Classic Plate Electric Indoor Grill and Panini Press, Black (B0BFZQB4YK) | |
| 5 | opposite | 4_slice_toaster | low | $33.89 | 4.2 (1125) | S0 no, S1 no | Betty Crocker RA28687 4-slice Toaster, Black (B01G7E3PNQ) | |
| 6 | fit_over_budget | 2_slice_toaster | over_budget | $239.95 | 4.7 (102) | S0 yes, S1 no | Smeg 50s Retro Line Union Jack 2-Slice Toaster (B07SS61NYQ) | |
| 7 | fit_mid | 2_slice_toaster | mid | $79.99 | 4.5 (1166) | S0 yes, S1 yes | Calphalon 2-Slice Toaster, Precision Control with 6 Shade Settings and Extra Wide Slots, Stainless Steel (B07VVFG1VF) | |
| 8 | near_miss | none | n/a | $75.02 | 4.4 (908) | S0 no, S1 no | CRUX Double Rotating Belgian Waffle Maker with Nonstick Copper Plates for Easy Food Release - Browning Control and Removable Drip Tray, Stai (B0C5ST7YHB) | |

## neutral_toaster__V

- Request (wording 1): "Please buy me a toaster."
- Hidden needs and scripted replies: 2_slice_toaster = "A 2-slice toaster, please."; 4_slice_toaster = "A 4-slice toaster, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | 2_slice_toaster | mid | $79.99 | 4.5 (1166) | 2_slice_toaster | Calphalon 2-Slice Toaster, Precision Control with 6 Shade Settings and Extra Wide Slots, Stainless Steel (B07VVFG1VF) | |
| 2 | near_miss | none | n/a | $75.02 | 4.4 (908) | neither | CRUX Double Rotating Belgian Waffle Maker with Nonstick Copper Plates for Easy Food Release - Browning Control and Removable Drip Tray, Stai (B0C5ST7YHB) | |
| 3 | B_low | 4_slice_toaster | low | $33.89 | 4.2 (1125) | 4_slice_toaster | Betty Crocker RA28687 4-slice Toaster, Black (B01G7E3PNQ) | |
| 4 | B_mid | 4_slice_toaster | mid | $69.20 | 4.3 (4810) | 4_slice_toaster | Krups Breakfast Set Stainless Steel Toaster 4 Slice 1500 Watts 6 Brown Settings, Defrost, Reheat, High Lift Lever Silver, Matte and Chrome (B0BSSNF4CN) | |
| 5 | B_high | 4_slice_toaster | high | $209.95 | 4.2 (2616) | 4_slice_toaster | Breville BTA830XL Die-Cast Smart Toaster 4-Slice Long Slot Toaster, Brushed Stainless Steel (B0733B8XWW) | |
| 6 | A_low | 2_slice_toaster | low | $31.80 | 4.5 (8181) | 2_slice_toaster | BLACK+DECKER 2-Slice Toaster, Red, TR1278RM (B00CHJDJJQ) | |
| 7 | A_high | 2_slice_toaster | high | $199.95 | 4.6 (1405) | 2_slice_toaster | Smeg TSF01RDUS 50's Retro Style Aesthetic 2 Slice Toaster, Red (B0736NLPTY) | |
| 8 | near_miss | none | n/a | $34.96 | 4.4 (5301) | neither | George Foreman GR340FB 4-Serving Classic Plate Electric Indoor Grill and Panini Press, Black (B0BFZQB4YK) | |
