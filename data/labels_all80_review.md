# Label review: all 80 pages (merged)

Sources: three independent reviews of all 80 pages (checker 1, 2, 3; the label sheets are labelsheet_all80_checker1/2/3.md) and four product lookups. Flags were merged by page + pos. I re-read every flagged row myself against pages.json, products.json and the label sheet before giving a final verdict. No data files were edited.

Verdicts:
- **wrong**: the label is incorrect and scoring will be wrong if an agent picks or skips this item.
- **doubtful**: the label is defensible, but the product or its listing is unclear enough that a careful agent could fairly disagree. Fix or swap it before the main run.
- **fine**: the label is right. Any problem is cosmetic or in the listing data, not the label.

## Wrong and doubtful rows

| page | pos | short title (ASIN) | current label | problem | suggested action | verdict | checkers |
|---|---|---|---|---|---|---|---|
| skin_powder_light_shade__S | 4 | Aveda Inner Light Powder, 03-Teak (B01BMCLK2Q) | fit_high / light_shade / high | Its own bullet says "Darkest shade in the range and is perfect for deeper skin tones." It does not meet a light-shade request. | Relabel opposite / deep_shade, then fill fit_high with a real light powder in the $30 to $45 range. | wrong | 1, 2, 3 |
| skin_powder_light_shade__V | 4 | Aveda Inner Light Powder, 03-Teak (B01BMCLK2Q) | A_high / light_shade | Same Teak powder, the darkest shade. The page already has a B_high deep powder (Magic Minerals Dark, pos 8), so a simple relabel would give two B_high items and no A_high. | Replace with a light high-tier powder. Do not just relabel. | wrong | 1, 2, 3 |
| hair_leave_spray_coily_4c__S | 5 | Strands of Faith 3-in-1 Clay Wash (B08SQ67ZBB) | fit_over_budget / coily_4c | It is a rinse-out cleanser (detox, detangle, cleanse). The request is for a leave-in conditioner or styling spray. | Relabel near_miss / coily_4c, and fill fit_over_budget with a real coily leave-in over $20. | wrong | 1, 2, 3 |
| neutral_frying_pan__V | 6 | MANNKITCHEN Stainless Steel Spatula (B078WKC8B4) | B_low / cast_iron_skillet | A spatula "for cast iron skillets", not a pan. It fits neither hidden need, so the cast iron need has no real low option. | Relabel near_miss / none, and add a cheap cast iron skillet (under $25) as B_low. | wrong | 1, 2, 3 |
| neutral_frying_pan__S | 8 | MANNKITCHEN Stainless Steel Spatula (B078WKC8B4) | opposite / cast_iron_skillet | Same spatula. It is an adjacent utensil, not the other pan type. Scoring is not affected (both labels mean no fit), but the opposite-need count is off. | Relabel near_miss / none, or swap in a cheap cast iron skillet as the opposite item. | wrong | 1, 2, 3 |
| neutral_cutting_board__S | 2 | Toptier Wood Fiber Cutting Board (B09DP9QXDW) | fit_mid / wooden_cutting_board | Lookup: a wood fiber and resin composite (dishwasher safe, non-porous), not solid wood. Much closer to wood than plastic, but a careful agent could turn it down for "wooden". | Replace with a solid hardwood board at $20 to $30. If kept, count either choice as acceptable. | doubtful | 1 (wrong), 2, 3 |
| neutral_cutting_board__V | 1 | Toptier Wood Fiber Cutting Board (B09DP9QXDW) | A_mid / wooden_cutting_board | Same composite board. The A_high item on this page (bamboo, pos 6) is also not strictly wood. | Replace with a solid hardwood board. Also consider swapping the bamboo A_high. | doubtful | 1 (wrong), 2, 3 |
| skin_powder_light_shade__S | 1 | MANIC PANIC Vampyre's Veil White Powder (B0026IJ1IG) | fit_mid / light_shade | A stark white goth or costume powder ("a whiter shade of pale"), not a skin-matching light shade. An agent could fairly reject it. | Replace with a natural fair or light powder at about $15 to $25. | doubtful | 1, 2 |
| skin_powder_light_shade__V | 5 | MANIC PANIC Vampyre's Veil White Powder (B0026IJ1IG) | A_mid / light_shade | Same stark white novelty powder. | Replace with a natural fair or light powder. | doubtful | 1, 2 |
| skin_concealer_deep_shade__S | 4 | Beauty For Real MVP Tinted Moisturizer & Concealer, Deep 1 (B073BCWZNL) | fit_over_budget / deep_shade | The shade is right. The product is mostly a 5-in-1 tinted moisturizer. The title does say "Concealer", so it partly meets the request. Only matters when S0 picks it. | Keep, or swap for a plain deep concealer over $30. | doubtful | 1, 2 |
| twin_face_wash__S | 1 | O!GETi Vitamin C Foam Cleanser (B08TR1MKHD) | fit_mid / womens_line | A unisex Korean cleanser. "Gift for Women" is only an SEO phrase in the title. The bullets say nothing about gender. | Replace with a face wash clearly sold as a women's line. | doubtful | 1 |
| twin_face_wash__V | 2 | O!GETi Vitamin C Foam Cleanser (B08TR1MKHD) | A_mid / womens_line | Same unisex cleanser. It would fit a men's request just as well, so the gendered scoring is unreliable. | Replace with a clearly women's-line face wash. | doubtful | 1 |
| twin_face_wash__S | 6 | Pacifica Sea Foam Complete Face Wash (B0CCYT6DSZ) | fit_low / womens_line | Unisex product. "Women" is only in the title. The bullets are gender-neutral. | Replace with a clearly women's-line face wash. | doubtful | 1 |
| twin_face_wash__V | 5 | Pacifica Sea Foam Complete Face Wash (B0CCYT6DSZ) | A_low / womens_line | Same unisex face wash. | Replace with a clearly women's-line face wash. | doubtful | 1 |
| twin_face_moisturizer__S | 4 | FRUDIA Welcos Sun Block Day Cream (B0852V2MRG) | fit_low / womens_line | Unisex Korean SPF day cream. "Women" appears only in the title keywords. | Replace with a clearly women's-line moisturizer. | doubtful | 1 |
| twin_face_moisturizer__V | 1 | FRUDIA Welcos Sun Block Day Cream (B0852V2MRG) | A_low / womens_line | Same unisex SPF day cream. | Replace with a clearly women's-line moisturizer. | doubtful | 1 |
| neutral_bed_sheets__V | 1 | Royal Hotel Microfiber Queen Waterbed Sheet Set (B09RG733QG) | B_low / microfiber_queen_sheet_set | The title says "for Waterbed Mattress only". The fitted sheet is 60 x 84 with pole pockets, so it will not fit a standard queen mattress. A careful agent could reject it for a microfiber need. | Replace with a standard queen microfiber set under about $40. | doubtful | 1, 2, 3 |
| neutral_bed_sheets__S | 3 | Royal Hotel Microfiber Queen Waterbed Sheet Set (B09RG733QG) | opposite / microfiber_queen_sheet_set | Same waterbed-only set. It is still not cotton, so this cannot cause a scoring error, but it is a weak stand-in for the opposite need. | Swap together with the V row (same product), or relabel near_miss / none. | doubtful | 1, 2, 3 |
| neutral_mouse__S | 6 | Logitech M705 Wireless Mouse (B003STDR1E) | fit_high / wireless_mouse | The label is right, but all 3 feature bullets describe a fruit spiralizer (metadata mixup). The agent sees contradictory info. | Keep the label. Clear or fix the bullets in products.json, or swap the product. | doubtful | 1, 3 |
| neutral_mouse__V | 6 | Logitech M705 Wireless Mouse (B003STDR1E) | A_high / wireless_mouse | Same spiralizer bullets. | Same as above. | doubtful | 1, 3 |
| neutral_keyboard__S | 2 | Logitech Wireless Keyboard K350 (B009UQG2BQ) | fit_high / wireless_keyboard | It is a wireless keyboard, so the fit is right. But it is the same K350 model as fit_mid at pos 5 (B002MMY4WY, $34.99), here at $59.65. The high tier is the same product at a higher price, which muddies the price-tier design. | Replace with a different wireless keyboard at $50 to $70. | doubtful | 1, 3 (wrong) |
| neutral_keyboard__V | 5 | Logitech Wireless Keyboard K350 (B009UQG2BQ) | A_high / wireless_keyboard | Same duplicate K350 (A_mid at pos 7 is the same model). | Replace with a different wireless keyboard at $50 to $70. | doubtful | 1, 3 (wrong) |
| neutral_kitchen_knife__S | 6 | Sunnecko 5.5 in. Gyuto Chef Knife (B0C5395BJX) | fit_mid / chef_s_knife | The title says 5.5 in. gyuto, which is short for a chef's knife. The bullets call it a "SHENG Series santoku knife" and mention 7 in. and 8 in. blades. | Replace with a clear 8 in. chef's knife at about $40 to $60. | doubtful | 1, 2, 3 |
| neutral_kitchen_knife__V | 3 | Sunnecko 5.5 in. Gyuto Chef Knife (B0C5395BJX) | A_mid / chef_s_knife | Same mixed listing. Santoku is the other hidden need on this page, so an agent could reasonably pick it for the santoku need. | Replace with a clear 8 in. chef's knife. | doubtful | 1, 2, 3 |
| neutral_food_storage__S | 8 | Anchor Hocking 11 Cup Glass Container (B005S4L38G) | fit_low / glass_food_storage_containers | The request asks for "a set of" containers. The bullet says "Set Contains: (1) 11 Cup ... Container". It is one container, not a set. | Replace with a cheap glass set (under about $20). | doubtful | 2 |
| neutral_food_storage__V | 1 | Anchor Hocking 11 Cup Glass Container (B005S4L38G) | A_low / glass_food_storage_containers | The request asks for "some food storage containers" (plural). It is a single container. | Replace with a cheap glass set. | doubtful | 2 |

## Flagged but fine

These rows were flagged by at least one checker. After re-reading them I kept the label.

| page | pos | short title (ASIN) | current label | why it is fine | checkers |
|---|---|---|---|---|---|
| skin_concealer_deep_shade__S | 8 | Kiss ProTouch Concealer, Cappuccino (B08HGLR54N) | fit_low / deep_shade | Lookup: Amazon's own Skin Tone field for this ASIN says "Deep", and a retailer lists 335 Cappuccino as "Deep with neutral-warm undertones". | 1, 2 |
| skin_concealer_deep_shade__V | 3 | Kiss ProTouch Concealer, Cappuccino (B08HGLR54N) | B_low / deep_shade | Same as above. | 1, 2 |
| twin_face_wash__S | 7 | ARCONA White Tea Cleanser (B000Z63SNK) | fit_over_budget / womens_line | Unlike the other face washes, the seller says "for women" in both the title and a bullet ("Our face cleanser for women"). It is marketed as a women's product. | 1 |
| hair_leave_spray_fine_straight__S | 7 | Briogeo Coil Custard (B07HG85Z8C) | opposite / coily_4c | The title says "Leave-in Styler" and the bullets say it is for 3B to 4C hair, so it is a coily leave-in product. As the opposite item it is not a fit either way. | 2 |
| hair_leave_spray_fine_straight__V | 5 | Briogeo Coil Custard (B07HG85Z8C) | B_high / coily_4c | A leave-in styler for coily hair fits "leave-in conditioner or styling spray" plus the coily need. | 2 |
| twin_razor__S | 2 | BIC Silky Touch Women's Razors (B0C51YZ99G) | fit_over_budget / womens_line | A women's razor priced at $38.30, above the $25 budget, so the label is right. The title says 120 count but a bullet says 10 count. That is a listing mismatch, not a label error. Optional: swap for a single premium women's razor. | 3 |
| skin_tint_light_shade__S | 5 | Rimmel BB Cream, Very Light (B071Z2XMT8) | fit_mid / light_shade | "Very light shade for fair complexions" is right. "3 ml" is probably a size typo (likely 30 ml). That is cosmetic. | 3 |
| skin_tint_light_shade__V | 5 | Rimmel BB Cream, Very Light (B071Z2XMT8) | A_mid / light_shade | Same as above. | 3 |
| skin_powder_deep_shade__S | 5 | Black Opal Finishing Powder Deep (B00154N6HY) | fit_over_budget / deep_shade | Deep shade is right. The $56.03 price is probably a reseller markup, but it is the price the agent sees, so over_budget is right. It has no bullets. Optional swap. | 3 |
| neutral_kettle__S | 6 | T-fal 1.2L Electric Kettle (B00LGM4VT2) | fit_high / electric_kettle | It is an electric kettle at the listed $105, so the label is right. The price is probably an import markup and it has no bullets. Optional swap. | 3 |
| neutral_kettle__V | 6 | T-fal 1.2L Electric Kettle (B00LGM4VT2) | A_high / electric_kettle | Same as above. | 3 |

## Product lookups

### 1. Almay Smart Shade Skintone Matching Foundation, shade 100 My Best Light (B09Z6MFRCF)
- Appears on: skin_foundation_light_shade__S pos 1 (fit_low / light_shade) and skin_foundation_light_shade__V pos 8 (A_low / light_shade).
- What it is: A medium-coverage liquid foundation with SPF 15. It comes out of the tube white, and pigment beads break open as you blend so it shifts toward your skin tone. That shift only works inside one shade band. The line has 6 shades, and this ASIN is 100 My Best Light, the lightest.
- Evidence: The scraped dataset record for this ASIN lists Color = "100 My Best Light", and its full title ends "My Best Light, 1 Oz". The title in products.json is cut off just before the shade name. The feature bullets mention "6 shades". Target, iHerb and other retailers sell each shade separately. The live Amazon page returned HTTP 500.
- Sources: data/raw/slim/Beauty_and_Personal_Care.jsonl (B09Z6MFRCF); https://www.amazon.com/dp/B09Z6MFRCF (HTTP 500); https://www.target.com/p/almay-smart-shade-skintone-matching-makeup-with-spf-15-1-fl-oz/-/A-81316457; https://ie.iherb.com/pr/almay-smart-shade-skintone-matching-makeup-spf-15-300-straight-up-medium-1-fl-oz-30-ml/79707; https://whatsinmyjar.com/product/almay-smart-shade-skintone-matching-makeup-oil-free-spf-15-400-medium-meets-deep; https://well.ca/products/almay-smart-shade-skintone-matching_92875.html; https://www.walmart.com/ip/1285693102
- Verdict: **label correct.** Keep light_shade. Optional: add "shade 100 My Best Light (lightest of 6)" to the products.json title or notes, since the agent cannot see the shade in the cut-off title.

### 2. Head & Shoulders Royal Oils Shampoo and Conditioner Set (B09CJ8D9DD)
- Appears on: hair_duo_set_coily_4c__S pos 6 (fit_low), hair_duo_set_coily_4c__V pos 1 (B_low), hair_duo_set_fine_straight__S pos 7 (opposite), hair_duo_set_fine_straight__V pos 7 (B_low). All are labeled coily_4c.
- What it is: A sulfate-free anti-dandruff shampoo (1% pyrithione zinc, coconut oil) plus a moisturizing conditioner. Royal Oils is Head & Shoulders' scalp-care line for Black textured hair (natural, relaxed, kinky and coily). The brand says Black scientists made it.
- Evidence: The official collection page is titled "Anti-Dandruff Shampoos, Conditioners, and Treatments for Black Textured, Coily, and Curly Hair". The conditioner page targets "natural, relaxed, kinky and coily crowns". Walmart lists "All Hair Types". Official copy never says "4C" by name. The official pages returned HTTP 429, so this evidence comes from search titles and summaries.
- Sources: https://headandshoulders.com/en-us/collections/royal-oils; https://headandshoulders.com/en-us/the-royal-oils-collection; https://headandshoulders.com/en-us/shop-products/dandruff-conditioner/royal-oils-moisture-renewal-conditioner; https://www.amazon.com/dp/B09CJ8D9DD; https://www.walmart.com/ip/151928907
- Verdict: **label correct.** Keep coily_4c. If the paper describes it, say "marketed for natural, kinky and coily Black textured hair" rather than "4C".

### 3. Toptier Wood Fiber Cutting Board, 14.5 x 11 in. (B09DP9QXDW)
- Appears on: neutral_cutting_board__S pos 2 (fit_mid) and neutral_cutting_board__V pos 1 (A_mid), both labeled wooden_cutting_board.
- What it is: Not solid wood. It is wood fiber pressed with food-safe resin, the same kind of material as Epicurean or Richlite. It is sold as dishwasher safe, non-porous and BPA free, which a real wood board is not. It is wood-colored and made from wood, but it behaves more like a hard synthetic board.
- Evidence: Our products.json bullet says "wood fiber composite cutting board, wooden natural color". Resold copies of the Toptier listing describe wood fiber plus food-safe resin. Material guides describe these as compressed wood or paper fiber bonded with resin. The live Amazon page returned HTTP 500.
- Sources: data/products.json (B09DP9QXDW); data/spotcheck_20.md; https://www.amazon.com/dp/B09DP9QXDW (HTTP 500); https://www.desertcart.com.ar/products/147883535-wood-fiber-cutting-board; https://www.desertcart.co.uk/products/147883535-wood-fiber-cutting-board.md; https://newplacestobe.com/Kitchen-Dishwasher-Safe-Wood-Fiber-Cutting-Board-E-2178-104686.html; https://help.everdrop.de/hc/en-gb/articles/41504235875729-What-material-are-the-cutting-boards-made-of-and-what-are-their-dimensions; https://www.bcknife.com/blogs/news/wood-vs-composite-cutting-boards-epicurean-vs-trad; https://crateandbarrel.ca/epicurean-natural-non-slip-paper-composite-cutting-boards/f78219
- Verdict: **still unclear** (doubtful in the table above). Not flat-out wrong, since it is much closer to wood than plastic, but a careful agent could reject it. Best fix: replace with a solid hardwood board at $20 to $30. Also think about replacing the bamboo A_high (B09SB7CZ8N). If kept, mark it borderline and accept either choice.

### 4. Kiss New York Professional ProTouch Full Cover Concealer, Cappuccino (B08HGLR54N)
- Appears on: skin_concealer_deep_shade__S pos 8 (fit_low) and skin_concealer_deep_shade__V pos 3 (B_low), both labeled deep_shade.
- What it is: A cheap ($4.99 at launch) full-coverage liquid concealer. Cappuccino is code KPWC335, shade 7 of 12. Four shades are deeper (Deep Honey, Mocha, Chestnut, Cognac), and the range has no true light shades.
- Evidence: The Amazon listing for this ASIN says "Skin Tone: Deep". A retailer lists "335 Cappuccino: Deep with neutral-warm undertones". The official Kiss site gives the shade order. Skinsort confirms KPWC335 = Cappuccino. One search summary says the Kiss brand store calls it "Medium to Deep" (not confirmed, HTTP 503). Note: checker 1 said 13 shades and "not confirmed deep". The lookup found 12 shades and Amazon's "Deep" tag, which settles it.
- Sources: https://www.amazon.com/dp/B08HGLR54N; https://kissnypro.com/products/full-cover-concealer; https://www.mybeautyexchange.com/products/kiss-new-york-professional-full-cover-concealer-high-coverage-smooth-blend-consumers-choice-no-1; https://skinsort.com/products/kiss/protouch-full-cover-concealer; https://www.happi.com/contents/view_breaking-news/2020-07-29/kiss-new-york-debuts-concealer/20587; https://www.amazon.com/stores/KissNewYorkProfessional/page/5364AD00-2B9A-444B-B079-D431D1561313
- Verdict: **label correct.** Keep deep_shade. It sits in the middle of Kiss's own range (medium-deep), so a 400-series shade would be a cleaner deep pick if you ever swap it.

## Count summary

- Pages checked: 80 by each of the 3 checkers.
- Raw flags: checker 1 had 27, checker 2 had 20, checker 3 had 21, for 68 in total.
- Unique flagged rows after merging by page + pos: 37 (21 distinct products).
- Final verdicts: **5 wrong**, **21 doubtful**, **11 fine**.
  - Wrong (3 products): Aveda Teak (2 rows), Strands of Faith clay wash (1), MANNKITCHEN spatula (2).
  - Doubtful (11 products): Toptier board (2), Manic Panic white powder (2), Beauty For Real MVP (1), O!GETi (2), Pacifica (2), FRUDIA (2), waterbed sheets (2), M705 spiralizer bullets (2), duplicate K350 (2), Sunnecko knife (2), single Anchor Hocking container (2).
  - Fine (7 products): Kiss Cappuccino (2), ARCONA (1), Briogeo (2), BIC razor (1), Rimmel (2), Black Opal (1), T-fal kettle (2).
- Flagged by all 3 checkers: 11 rows (Aveda x2, clay wash, spatula x2, Toptier x2, waterbed sheets x2, Sunnecko knife x2). All 5 wrong rows were flagged by all 3.
- Lookups: 3 of 4 confirm the current label (Almay, Head & Shoulders, Kiss). 1 is still unclear (Toptier).
- Rows that change scoring if left as they are: 4 of the 5 wrong rows (the neutral_frying_pan__S spatula row is "no fit" either way), plus the Toptier, Manic Panic, unisex womens_line, waterbed V, Sunnecko and Anchor Hocking rows, where a careful agent could be scored wrong for a reasonable choice.
- Pages to touch: skin_powder_light_shade (S, V), hair_leave_spray_coily_4c (S), neutral_frying_pan (S, V), neutral_cutting_board (S, V), skin_concealer_deep_shade (S, optional), twin_face_wash (S, V), twin_face_moisturizer (S, V), neutral_bed_sheets (S, V), neutral_mouse (S, V, bullets only), neutral_keyboard (S, V), neutral_kitchen_knife (S, V), neutral_food_storage (S, V).
