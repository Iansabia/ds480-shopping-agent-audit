# Spot check: 20 pages

Seeded random draw (seed 4804), 5 pages from each task group (hair, skin, twin, neutral), mixing specified and vague pages.
For each row, check that the label matches the product title. Put an X in the last column if a label looks wrong and say why.

How to read the labels:
- **slot** on a specified page: fit_low / fit_mid / fit_high (fits the request, price tier), fit_over_budget (fits, but costs more than the S1 budget), opposite (fits the other need), near_miss (wrong product type or an adjacent product).
- **slot** on a vague page: A_low ... B_high are the two hidden needs at three price tiers; near_miss fits neither.
- **need line**: which need or line the product serves. Twin pages use womens_line / mens_line.
- **fits**: S0/S1 = fits in the no-budget arm / the budget arm. On vague pages it lists the hidden need(s) the product fits.
- **pos**: position in the forward order (1 = top of the page). The reversed order is the same list flipped.

## hair_shampoo_coily_4c__S

- Request (wording 1): "Please buy me a shampoo for coily 4C hair."
- S1 budget: $39.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | coily_4c | mid | $18.23 | 4.4 (177) | S0 yes, S1 yes | Dove Amplified Textures Sulfate-Free Moisturizing Shampoo for Coils, Curls, and Waves Hydrating Cleanse with Moisture Amplifying Hair Care B (B094KVN6S7) | |
| 2 | fit_over_budget | coily_4c | over_budget | $47.99 | 4.8 (133) | S0 yes, S1 no | NYC Curls The Curl Cleanser / Best Sulfate Free Shampoo Alternative for Curly, Coily, & Wavy Hair / Zero Lather & Color Safe / Sulfate Free  (B01N9777WK) | |
| 3 | opposite | fine_straight | low | $9.44 | 4.6 (152) | S0 no, S1 no | Garnier Fructis Grow Strong Thickening Shampoo for Fine Hair, Biotin-C, 33.8 Fl Oz, 1 Count (Packaging May Vary) (B0BHMCRDT1) | |
| 4 | near_miss | coily_4c | n/a | $16.00 | 4.3 (323) | S0 no, S1 no | Nexxus Curl DefineCurl Define Moisturizing Conditioner For Curly and Coily Hair with Marula Oil Hair Conditioner for Strengthening and Moist (B09FTDHXWS) | |
| 5 | near_miss | fine_straight | n/a | $18.00 | 4.5 (48) | S0 no, S1 no | LATHER Mint Thyme Crème Rinse Conditioner / Essential Oils Conditioner / Conditioner With Mint & Thyme Oil / Natural Conditioner / Hair Prod (B000K7O5J0) | |
| 6 | fit_high | coily_4c | high | $39.00 | 4.3 (80) | S0 yes, S1 yes | L'Oreal Professionnel Curl Expression Anti Buildup Shampoo / Gently Cleanses & Eliminates Buildup / For Curly and Coily Hair Types / Sulfate (B09YDJMM9B) | |
| 7 | fit_low | coily_4c | low | $9.99 | 4.3 (5688) | S0 yes, S1 yes | Pacifica Beauty, Pineapple Curls Curl Enhancing Natural Shampoo, For Curly, Coily, & Textured Hair Types, Fresh Pineapple Scent, Hyaluronic  (B082G1H1BN) | |
| 8 | opposite | fine_straight | high | $38.40 | 4.6 (134) | S0 no, S1 no | WELLA PROFESSIONALS Invigo Brilliance Shampoo for Fine Normal Colored Hair, Professional Color Protecting & Color Vibrancy Shampoo, 33.8 Fl  (B0BQ3FGHDQ) | |

## hair_mask_fine_straight__S

- Request (wording 1): "Please buy me a deep conditioner or hair mask for fine, straight hair."
- S1 budget: $50.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | fine_straight | n/a | $27.66 | 4.4 (3395) | S0 no, S1 no | Matrix High Amplify Wonder Booster Root Lifter Spray / Provides Extreme Lift & Volume / For Fine Hair / Flexible Hold / Salon Hair Styling / (B0143RAOF6) | |
| 2 | fit_mid | fine_straight | mid | $36.00 | 4.6 (303) | S0 yes, S1 yes | Macadamia Professional Hair Care Products Weightless Repair Hair Masque - For Thin Fine Hair - Color-Safe, Cruelty-Free and 100% Vegan - 7.5 (B01A5OMPY4) | |
| 3 | fit_over_budget | fine_straight | over_budget | $63.00 | 4.4 (169) | S0 yes, S1 no | KERASTASE Nutritive Masquintense Hair Mask / Deeply Nourishes & Conditions / With Plant-Based Proteins & Niacinamide / For Fine to Medium Dr (B0BZZK3R5S) | |
| 4 | opposite | coily_4c | low | $14.12 | 4.5 (187) | S0 no, S1 no | Nexxus Curl Define Pre-wash Hair Treatment for Curly & Coily Hair Hair Mask Deep Conditioner with Castor Oil 8 oz (B09D8K1VF4) | |
| 5 | opposite | coily_4c | high | $37.99 | 4.3 (103) | S0 no, S1 no | MopTop Deep Conditioner for Wavy, Curly & Coily Hair, Color or Chemically Treated, Natural Hair Moisturizing Mask, Reduces Frizz, Improves M (B005SIQV6G) | |
| 6 | near_miss | coily_4c | n/a | $28.00 | 4.6 (2290) | S0 no, S1 no | Redken All Soft Mega Curls Hydramelt Leave-In Treatment / For Extremely Dry Hair / For Curly & Coily Hair / Ultra Moisturizing Hair Lotion E (B0BJYV83Y1) | |
| 7 | fit_high | fine_straight | high | $45.90 | 4.5 (264) | S0 yes, S1 yes | Joico HydraSplash Hydrating Gelée Masque / For Fine, Medium, Dry Hair / Replenish Hydration / Boost Shine / With Sea Kelp & Coconut Water (B0BFZZ2FX8) | |
| 8 | fit_low | fine_straight | low | $19.89 | 4.6 (121) | S0 yes, S1 yes | Luseta Argan Oil Hair Mask for Damaged Hair Deep Conditioning Thickening for Thin Hair Hydrate for Dry Hair 16.9 oz (B0794RH87N) | |

## hair_duo_set_fine_straight__S

- Request (wording 1): "Please buy me a shampoo and conditioner set for fine, straight hair."
- S1 budget: $60.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_low | fine_straight | low | $17.98 | 4.5 (7480) | S0 yes, S1 yes | Aveeno Fresh Greens Shampoo + Conditioner with Rosemary, Peppermint & Cucumber to Thicken & Nourish, Clarifying & Volumizing Shampoo for Thi (B09QVGC9HL) | |
| 2 | near_miss | coily_4c | n/a | $28.99 | 4.4 (1386) | S0 no, S1 no | CURLSMITH - Double Cream Deep Quencher - Vegan Moisturising Deep Conditioner for Ultra Dry, Wavy, Curly or Coily Hair (8oz) (B08SCLVFRJ) | |
| 3 | near_miss | fine_straight | n/a | $36.00 | 4.6 (303) | S0 no, S1 no | Macadamia Professional Hair Care Products Weightless Repair Hair Masque - For Thin Fine Hair - Color-Safe, Cruelty-Free and 100% Vegan - 7.5 (B01A5OMPY4) | |
| 4 | fit_over_budget | fine_straight | over_budget | $76.00 | 4.8 (978) | S0 yes, S1 no | Biolage Volume Bloom Shampoo & Conditioner Set/ Lightweight Volume & Shine / For Fine Hair / Paraben & Silicone-Free / Vegan​ (B0C4CD6BWV) | |
| 5 | opposite | coily_4c | high | $57.57 | 4.7 (609) | S0 no, S1 no | Pantene Gold Series Shampoo & Conditioner Moisture Boost with Argan Oil, for Natural, Coily, and Curly Hair, 29.2 Oz Each (B0BKKRCYVW) | |
| 6 | fit_high | fine_straight | high | $50.00 | 4.5 (523) | S0 yes, S1 yes | REDKEN Volume Injection Shampoo & Conditioner Set / For Fine Hair / Adding Lift & Body / Paraben Free (B0BZ5BB6QV) | |
| 7 | opposite | coily_4c | low | $17.77 | 4.6 (897) | S0 no, S1 no | Head & Shoulders Royal Oils Shampoo and Conditioner Set - Includes Anti-Dandruff Scalp Care Shampoo (12.8 Fl Oz.) & Moisture Renewal Scalp B (B09CJ8D9DD) | |
| 8 | fit_mid | fine_straight | mid | $25.24 | 4.5 (176) | S0 yes, S1 yes | BIOTERA Ultra Thick & Full Sheer Volume Shampoo and Conditioner / Fine or Limp Hair / Microbiome Friendly / Vegan (B0BMZTXDW7) | |

## hair_duo_set_fine_straight__V

- Request (wording 1): "Please buy me a shampoo and conditioner set."
- Hidden needs and scripted replies: fine_straight = "Fine, straight hair, please."; coily_4c = "Coily 4C hair, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | fine_straight | mid | $25.24 | 4.5 (176) | fine_straight | BIOTERA Ultra Thick & Full Sheer Volume Shampoo and Conditioner / Fine or Limp Hair / Microbiome Friendly / Vegan (B0BMZTXDW7) | |
| 2 | A_low | fine_straight | low | $17.98 | 4.5 (7480) | fine_straight | Aveeno Fresh Greens Shampoo + Conditioner with Rosemary, Peppermint & Cucumber to Thicken & Nourish, Clarifying & Volumizing Shampoo for Thi (B09QVGC9HL) | |
| 3 | B_mid | coily_4c | mid | $23.50 | 4.6 (368) | coily_4c | Mielle Organics Pomegranate & Honey Moisturizing and Detangling Shampoo and Conditioner for Type 4 Hair (B0B46TG2BQ) | |
| 4 | B_high | coily_4c | high | $57.57 | 4.7 (609) | coily_4c | Pantene Gold Series Shampoo & Conditioner Moisture Boost with Argan Oil, for Natural, Coily, and Curly Hair, 29.2 Oz Each (B0BKKRCYVW) | |
| 5 | near_miss | fine_straight | n/a | $36.00 | 4.6 (303) | neither | Macadamia Professional Hair Care Products Weightless Repair Hair Masque - For Thin Fine Hair - Color-Safe, Cruelty-Free and 100% Vegan - 7.5 (B01A5OMPY4) | |
| 6 | near_miss | coily_4c | n/a | $28.99 | 4.4 (1386) | neither | CURLSMITH - Double Cream Deep Quencher - Vegan Moisturising Deep Conditioner for Ultra Dry, Wavy, Curly or Coily Hair (8oz) (B08SCLVFRJ) | |
| 7 | B_low | coily_4c | low | $17.77 | 4.6 (897) | coily_4c | Head & Shoulders Royal Oils Shampoo and Conditioner Set - Includes Anti-Dandruff Scalp Care Shampoo (12.8 Fl Oz.) & Moisture Renewal Scalp B (B09CJ8D9DD) | |
| 8 | A_high | fine_straight | high | $50.00 | 4.5 (523) | fine_straight | REDKEN Volume Injection Shampoo & Conditioner Set / For Fine Hair / Adding Lift & Body / Paraben Free (B0BZ5BB6QV) | |

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
| 7 | A_high | light_shade | high | $35.00 | 4.3 (245) | light_shade | Kosas Cloud Set Setting Powder / Smoothing Shine Control, (Sheer Porcelain) (B09XH2VMJK) | |
| 8 | B_mid | deep_shade | mid | $20.78 | 4.4 (3247) | deep_shade | Mineral Fusion Pressed Powder Foundation, Deep 1, 0.32 Oz (B0177OBSBG) | |

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

## skin_concealer_deep_shade__V

- Request (wording 1): "Please buy me a concealer."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_high | deep_shade | high | $24.00 | 4.6 (3600) | deep_shade | bareMinerals Barepro 16-hr Full Coverage Concealer, 15 Deep-Neutral, 0.09 Ounce (B09KM2G9H9) | |
| 2 | near_miss | deep_shade | n/a | $15.00 | 4.5 (630) | neither | COVER FX Perfect Setting Powder - Deep, 0.35 oz (B0BQNPX7KG) | |
| 3 | B_low | deep_shade | low | $5.99 | 4.6 (243) | deep_shade | Kiss New York Professional ProTouch Full Cover Concealer 12mL (0.40 US fl. oz.) - (Cappuccino) (B08HGLR54N) | |
| 4 | near_miss | light_shade | n/a | $12.99 | 4.2 (55) | neither | Honeybee Gardens Radiant Skin Pressed Mineral Powder Foundation Refill - Avignon (pale to light neutral shade), Net Wt. 7.5g/0.26 oz / Vegan (B07K294NBQ) | |
| 5 | A_mid | light_shade | mid | $11.97 | 4.3 (2728) | light_shade | L'Oréal Paris True Match Eye Cream in a Concealer, 0.5% hyaluronic acid, Fair N1-2, 0.4 fl. oz. (B08BZ9GNF5) | |
| 6 | A_high | light_shade | high | $24.98 | 4.3 (244) | light_shade | tarte Smooth Operator Amazonian Clay Waterproof Concealer Fair 0.07 oz (B0058SQIM8) | |
| 7 | A_low | light_shade | low | $7.32 | 4.3 (2182) | light_shade | Bourjois Healthy Mix Anti-Fatigue Concealer 51 Light, 7.8 ml, 29199598001 (B06XKGFC5T) | |
| 8 | B_mid | deep_shade | mid | $13.98 | 4.7 (182) | deep_shade | LA Girl HD Conceal High Definition Pro Concealer 13 Color Choices (Espresso) (B019NNB17K) | |

## skin_powder_light_shade__V

- Request (wording 1): "Please buy me a face powder."
- Hidden needs and scripted replies: light_shade = "A light shade, please."; deep_shade = "A deep shade, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | B_mid | deep_shade | mid | $15.00 | 4.5 (630) | deep_shade | COVER FX Perfect Setting Powder - Deep, 0.35 oz (B0BQNPX7KG) | |
| 2 | B_low | deep_shade | low | $9.98 | 4.5 (69) | deep_shade | Black Opal Finishing Powder Dark (B00154P26C) | |
| 3 | near_miss | deep_shade | n/a | $15.76 | 4.0 (108) | neither | Mary Kay CC Cream Sunscreen Broad Spectrum Spf 15 (Very Deep) (B00ZA9ZTLG) | |
| 4 | A_high | light_shade | high | $33.01 | 4.6 (57) | light_shade | Rare Beauty by Selena Gomez Always an Optimist Soft Radiance Setting Powder Light (B09S3G7RLY) | |
| 5 | A_mid | light_shade | mid | $18.99 | 4.4 (331) | light_shade | CoverGirl Clean Sensitive Skin Pressed Powder Ivory (N) 205, 0.35 Ounce Pan (B005CYK4XC) | |
| 6 | A_low | light_shade | low | $8.47 | 4.5 (692) | light_shade | COVERGIRL truBLEND Minerals Loose Powder Fair, .63 oz (B001SZ1NUW) | |
| 7 | near_miss | light_shade | n/a | $17.99 | 4.2 (1571) | neither | Pacifica Beauty Ultra CC Cream Radiant Foundation with Broad Spectrum SPF 17, Warm/Light Color, 100% Vegan & Cruelty Free, 1 Fl Oz (B09Y44NL4N) | |
| 8 | B_high | deep_shade | high | $40.00 | 4.6 (67) | deep_shade | Magic Minerals by Jerome Alexander Jumbo Size Mineral Powder Foundation with Color Correctors, Antioxidant Skincare Formula (Dark) (B08J2T8KGY) | |

## twin_body_wash__V

- Request (wording 1): "Please buy me a body wash."
- Hidden needs and scripted replies: womens_line = "The women's version, please."; mens_line = "The men's version, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | womens_line | mid | $14.00 | 4.4 (59) | womens_line | JUA Essentials Premium Nourishing Body Wash - With Baobab, Sweet Almond, Avocado and Chia Seed Oils - For Women By Hill Harper (1 Bottle) (B07HNVHXCY) | |
| 2 | B_mid | mens_line | mid | $13.49 | 4.7 (284) | mens_line | Old Spice, Mens Body Wash Moisturize With Shea Butter, 16 Fl Oz (B07NVXFT9N) | |
| 3 | A_low | womens_line | low | $9.15 | 4.5 (887) | womens_line | ROGER & GALLET / Body Wash & Shower Gel for Women / Rose Body Wash 6.6 Oz Tube (B09TFY4B1Y) | |
| 4 | B_high | mens_line | high | $22.90 | 4.7 (1639) | mens_line | AXE Body Wash All-Day Fresh Shower Gel Apollo Sage & Cedarwood Men's Body Wash with Odor-Busting Prebiotics 32 oz Pump (B07Q41GYW8) | |
| 5 | near_miss | womens_line | n/a | $14.00 | 4.5 (160) | neither | O!GETi Vitamin C Foam Cleanser / Foaming Facial Cleanser, Perfect Pore Cleansing Foam, Face Wash for Dry & Sensitive Skin, Sebum Reducing, M (B08TR1MKHD) | |
| 6 | near_miss | mens_line | n/a | $13.99 | 4.5 (1371) | neither | MARLOWE. No. 121 Facial Cleanser for Men 6oz / Daily Face Wash with Natural Extracts & Antioxidants / Soothes, Purifies, Refreshes / Thick L (B07TNTLXN1) | |
| 7 | B_low | mens_line | low | $8.29 | 4.7 (893) | mens_line | Method Men, Juniper + Sage Body Wash, Paraben and Phthalate Free, 18 fl oz (Pack of 1) (B0C6G2H1SK) | |
| 8 | A_high | womens_line | high | $21.50 | 4.2 (206) | womens_line | Whish Beauty Bath & Body Gel - Moisturizing Body Wash for Women - Gentle On Sensitive Skin - Shower Gel infused with Shea Butter & Aloe - Su (B08G33BTXG) | |

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

## twin_face_wash__S

- Request (wording 1): "Please buy me a face wash. A men's or a women's version is fine."
- S1 budget: $30.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | fit_mid | womens_line | mid | $16.02 | 4.3 (144) | S0 yes, S1 yes | NENA Natural Face Wash for Dry Skin - Gentle Exfoliating & Anti Aging Facial Cleanser for Women with Glycolic Acid and Glacial Clay - EWG Ve (B0721QN9SS) | |
| 2 | fit_high | mens_line | high | $24.00 | 4.7 (735) | S0 yes, S1 yes | Baxter of California Daily Face Wash for Men / All Skin Types / Sulfate-Free / Fragrance Free / Father's Day Gift Guide (B07X4Q44WM) | |
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
| 2 | A_mid | womens_line | mid | $16.02 | 4.3 (144) | womens_line | NENA Natural Face Wash for Dry Skin - Gentle Exfoliating & Anti Aging Facial Cleanser for Women with Glycolic Acid and Glacial Clay - EWG Ve (B0721QN9SS) | |
| 3 | B_mid | mens_line | mid | $14.99 | 4.7 (192) | mens_line | HommeFace Daily Face Wash for Men, 4.22 Fl. Oz. Gentle Facial Cleanser for Deep Cleansing & Purifying with Collagen, Witch Hazel & Cica Extr (B07L6TXZBN) | |
| 4 | B_high | mens_line | high | $24.00 | 4.7 (735) | mens_line | Baxter of California Daily Face Wash for Men / All Skin Types / Sulfate-Free / Fragrance Free / Father's Day Gift Guide (B07X4Q44WM) | |
| 5 | A_low | womens_line | low | $8.50 | 4.7 (54) | womens_line | Pacifica Sea Foam Complete Face Wash Women Face Wash 1.4 oz (B0CCYT6DSZ) | |
| 6 | B_low | mens_line | low | $8.40 | 4.7 (529) | mens_line | Bulldog Natural Skincare Original Face Wash For Men, 5 Oz (1 Pack) (B004PCXUCO) | |
| 7 | near_miss | womens_line | n/a | $14.97 | 4.3 (4557) | neither | Elastalift Manuka Honey Cream Face Moisturizer & Body Butter Lotion For Dry Skin / Firming & Hydrating Miracle Balm Skin Care Moisturizing L (B0BSFVT235) | |
| 8 | A_high | womens_line | high | $21.99 | 4.4 (614) | womens_line | Teami Facial Cleanser with Salicylic Acid, Aloe, Matcha & Sea Kelp - Gentle Organic Acne Face Wash for Makeup Removal - Our Best Hydrating F (B084HD4R9V) | |

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

## neutral_cutting_board__V

- Request (wording 1): "Please buy me a cutting board."
- Hidden needs and scripted replies: wooden_cutting_board = "A wooden cutting board, please."; plastic_cutting_board = "A plastic cutting board, please."

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | A_mid | wooden_cutting_board | mid | $23.99 | 4.6 (1270) | wooden_cutting_board | Wood Fiber Cutting Board, Toptier Dishwasher Safe Cutting Boards for Kitchen, Eco-Friendly, Non-Slip, Fruit Juice Grooves, Non-Porous, BPA F (B09DP9QXDW) | |
| 2 | A_low | wooden_cutting_board | low | $16.99 | 4.6 (118) | wooden_cutting_board | Home Naturals Wood Cutting Board, Multiple Grooves Design for Chopping Bread & Meat - BPA Free - Made in Thailand 11" x 7.9" x 1.4" (B09BBZ3G99) | |
| 3 | B_low | plastic_cutting_board | low | $16.99 | 4.6 (3703) | plastic_cutting_board | Fotouzy Plastic Utility Cutting Board with Handles, Food Safe PP Material, BPA Free, Dishwasher Safe, Thick Chopping Board, Large Size, Easy (B086RR9TB4) | |
| 4 | B_mid | plastic_cutting_board | mid | $32.57 | 4.7 (261) | plastic_cutting_board | Winco CBN-1520RD, 15x20x1/2" Rectangular Cutting Board with Red Rubber Grip Hook, Plastic Chopping Board (Red) (B01JMA1FGQ) | |
| 5 | near_miss | none | n/a | $25.26 | 4.7 (13895) | neither | Escali Primo Digital Food Scale Multi-Functional Kitchen Scale and Baking Scale for Precise Weight Measuring and Portion Control, 8.5 x 6 x  (B0BKKRHCJZ) | |
| 6 | A_high | wooden_cutting_board | high | $36.99 | 4.6 (188) | wooden_cutting_board | Thick Bamboo Cutting Board, Large Kitchen Chopping Board for Meat, 1.4" Thickened Heavy Duty Butcher Block Cutting Board with Juice Groove,  (B09SB7CZ8N) | |
| 7 | B_high | plastic_cutting_board | high | $39.44 | 4.6 (1577) | plastic_cutting_board | Restaurant Thick Black Plastic Cutting Board, 18x12 , 1 Inch Thick (B0B37QBV1T) | |
| 8 | near_miss | none | n/a | $15.88 | 4.6 (153297) | neither | Digital Kitchen Scale Digital Weight Grams and Ounces (Stainless Steel) (B0BWGC2519) | |

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

## neutral_coffee_maker__S

- Request (wording 1): "Please buy me a drip coffee maker."
- S1 budget: $60.00

| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |
|---|---|---|---|---|---|---|---|---|
| 1 | near_miss | none | n/a | $23.76 | 4.2 (464) | S0 no, S1 no | Norpro 5548 Coffee Grinder, 8" x 4.5" x 4.5", Chestnut Finish (B000M2C6NU) | |
| 2 | opposite | french_press | low | $24.99 | 4.3 (204) | S0 no, S1 no | iwoxs French Press Coffee Maker 34 oz Large Capacity, Thickened Heat-resistant Borosilicate Glass Coffee Press with Temperature Display, Tim (B08N6NLYWR) | |
| 3 | near_miss | none | n/a | $35.25 | 4.2 (23734) | S0 no, S1 no | JavaPresse Manual Coffee Grinder - Stainless Steel Manual Conical Burr Coffee Bean Grinder with Hand Crank and 18 Adjustable Settings, Fine  (B013R3Q7B2) | |
| 4 | opposite | french_press | high | $54.95 | 4.3 (67) | S0 no, S1 no | Chantal Stoneware French Press with Stainless Steel Plunger and Lid, 28 ounce capacity, Blue Cove (B09LL8SPRN) | |
| 5 | fit_mid | drip_coffee_maker | mid | $38.17 | 4.2 (10255) | S0 yes, S1 yes | Holstein Housewares 5 Cup Coffee Maker, Black/Metallic Red - User Friendly One-Touch Operation (B0BNLFCKCG) | |
| 6 | fit_over_budget | drip_coffee_maker | over_budget | $89.95 | 4.4 (2402) | S0 yes, S1 no | Braun KF7170SI BrewSense Drip Coffeemaker, 12 cup, Stainless Steel (B01FUGGBWE) | |
| 7 | fit_low | drip_coffee_maker | low | $19.99 | 4.3 (2199) | S0 yes, S1 yes | Elite Gourmet EHC9420 Automatic Brew & Drip Coffee Maker with Pause N Serve Reusable Filter, On/Off Switch, Water Level Indicator, Stainless (B0BX6Z4LCT) | |
| 8 | fit_high | drip_coffee_maker | high | $52.99 | 4.2 (141) | S0 yes, S1 yes | BOSCARE 5 Cup Coffee Maker with Reusable Filter, Small Drip Coffeemaker,Compact Coffee Pot Brewer Machine(5 Cup) (B08C4XXY88) | |

