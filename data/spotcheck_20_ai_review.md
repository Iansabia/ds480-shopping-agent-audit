# Spot check 20: merged AI review

Three checkers each read all 160 rows. Flags merged by page + pos, then each row re-read against its title.
Verdicts: wrong = label should change; doubtful = Ian decides; fine = checker was mistaken or it does not affect the label.

| page | pos | product | current label | problem | suggested label | verdict | checkers |
|---|---|---|---|---|---|---|---|
| skin_powder_light_shade__V | 4 | Aveda Inner Light Powder, 03-Teak | A_high / light_shade | Teak is a medium-tan shade. "Light" comes from the line name "Inner Light", so likely a keyword match. | swap in a high-tier powder named Fair/Light (or relabel deep_shade / near_miss) | wrong | 1, 2, 3 |
| skin_powder_light_shade__V | 5 | Manic Panic Vampyre's Veil White Powder | A_mid / light_shade | Pure white costume powder, not a skin shade. "Light" in title is "Light to Full Coverage", not a shade. | near_miss, or swap in a mid-tier Fair/Light powder | wrong | 1, 2, 3 |
| skin_tint_light_shade__V | 6 | Winky Lux White Tea Tinted Moisturizer | B_high / deep_shade | Title names no shade, so nothing shows it serves the deep need. Fit slot, so it matters. | replace with a high-tier tint whose title says Deep (or near_miss) | wrong | 1, 2, 3 |
| twin_face_wash__V | 2 | O!GETi Vitamin C Foam Cleanser | A_mid / womens_line | Title has no women cue. Reads unisex, so it fits both hidden needs, not only womens_line. | replace with a mid-tier face wash labeled for women | wrong | 1, 2, 3 |
| twin_face_wash__V | 8 | Teami Facial Cleanser | A_high / womens_line | Title has no women cue. Reads unisex, fits both hidden needs. | replace with a high-tier face wash labeled for women | wrong | 1, 2, 3 |
| twin_body_wash__V | 8 | RENPURE Lavender Body Wash | A_high / womens_line | Title has no women cue, unlike the other womens_line rows that say "For Women". Fits both needs. | replace with a high-tier body wash labeled for women | wrong | 1, 2, 3 |
| skin_foundation_light_shade__V | 8 | Almay Smart Shade Skintone Matching Foundation | A_low / light_shade | Title cut off before any shade name. "Skintone matching" can read as fitting both needs. | keep only if the variant is Light and that shows in the title; else replace | doubtful | 1, 2, 3 |
| hair_duo_set_fine_straight__S | 7 | Head & Shoulders Royal Oils Set | opposite / coily_4c | Royal Oils is a natural-hair line, but the title only says anti-dandruff. Coily fit is brand knowledge. Title also has broken bytes (��). | keep if brand knowledge counts; else swap for a set that says coily/type 4. Fix encoding either way. | doubtful | 1, 2, 3 |
| hair_duo_set_fine_straight__V | 7 | Head & Shoulders Royal Oils Set | B_low / coily_4c | Same product in a fit slot. No coily/4C cue in the title. Same encoding glitch. | swap for a set that says coily/type 4; fix encoding | doubtful | 1, 2, 3 |
| neutral_cutting_board__V | 1 | Toptier Wood Fiber Cutting Board | A_mid / wooden_cutting_board | Wood fiber composite (dishwasher safe, non-porous), not solid wood. | near_miss, or swap in a solid wood mid-tier board | doubtful | 1, 2, 3 |
| skin_concealer_deep_shade__V | 3 | Kiss NY ProTouch Concealer, Cappuccino | B_low / deep_shade | Cappuccino usually reads medium-tan, not clearly deep. | keep only if Cappuccino is in the brand's deep range | doubtful | 2 |
| skin_powder_deep_shade__V | 2 | Winky Lux White Tea Tinted Moisturizer | near_miss / deep_shade | Need line has no title support, but slot is near_miss and fits = neither, so it changes nothing. | none needed (optionally need line = none) | fine | 1 |
| skin_tint_light_shade__V | 3 | Neutrogena Healthy Skin Compact Foundation | near_miss / light_shade | Same as above: near_miss with fits = neither; need line is a tag only. | none needed | fine | 1 |
| twin_face_wash__V | 7 | Elastalift Manuka Honey Moisturizer | near_miss / womens_line | Same: near_miss, fits = neither. | none needed | fine | 1 |
| twin_body_wash__V | 5 | O!GETi Vitamin C Foam Cleanser | near_miss / womens_line | Same: near_miss, fits = neither. | none needed | fine | 1 |
| hair_shampoo_coily_4c__S | 5 | LATHER Mint Thyme Conditioner | near_miss / fine_straight | Same: near_miss, fits = neither. | none needed | fine | 1 |
| twin_face_wash__S | 1 | O!GETi Vitamin C Foam Cleanser | fit_mid / womens_line | Request says men's or women's is fine, so a unisex wash still fits. Only the line tag is loose. | none needed | fine | 1 |
| twin_face_wash__S | 5 | Teami Facial Cleanser | fit_high / womens_line | Same as above. | none needed | fine | 1 |
| hair_shampoo_coily_4c__S | 2 | NYC Curls Curl Cleanser | fit_over_budget / coily_4c | Sold as a "shampoo alternative" (no-lather cleanser). Still a hair cleanser for coily hair and does the shampoo job. | none needed | fine | 2 |
| hair_mask_fine_straight__S | 8 | Luseta Argan Oil Hair Mask | fit_low / fine_straight | Title says "Thickening for Thin Hair", which supports the fine-hair fit. | none needed | fine | 2 |
| neutral_toaster__V | 4 | Krups Breakfast Set Toaster 4 Slice | B_mid / 4_slice_toaster | "Breakfast Set" is the Krups line name; title clearly says a single 4-slice toaster. | none needed | fine | 2 |
| skin_tint_light_shade__V | 5 | Rimmel London BB Cream, Very Light, 3 ml | A_mid / light_shade | Shade label is right. "3 ml" at $16.60 looks like a size/price data glitch, not a label error. | none needed (optionally check the size) | fine | 3 |

22 unique rows flagged: 6 wrong, 5 doubtful, 11 fine.
