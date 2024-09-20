I have been printing some diffrent macropads and wanted to design my own that have the things i would like to use.

I wanted to use hotswap keys and i found the Adafruit neokey breakout boards so i have designed it to fit them so it is easy to sway the keys and only soldering will be wires from the controller to the breakout boards and between the boards.

I am still waiting on the boards but i have tested it using a 3d model of the boards from the eagle files that Adafruit provide, and that seems to be working so far but will not know if everything works until i get the breakout boards.

I am also using a 12 LED Ring to show the layer that is active under the encoder button.

I use KMK for the firmware.

Printables files are here: https://www.printables.com/model/1013606-3x3-macropad

I have uploaded the fusion 360 files here if anyone want to edit it, and i have uploaded a base with the holder for the waveshare rp2040-zero and a version that do not have a holder for a rp2040 if you want to edit it for your own controller.

Photos so far is the rendered photos from Fusion 360 i will add real photos when i get the breakout boards so i can show it together and working. 

What you will need is:

18x M2x8 Selftapping screws. I use the ones from this listing: https://www.aliexpress.com/item/1005003604942716.html?spm=a2g0o.order_detail.order_detail_item.7.4b56f19cb83mOQ

7 M3xL3xOD4.2 heatset inserts. I have been using the ones from this lising:  https://www.aliexpress.com/item/1005006472781064.html?spm=a2g0o.order_list.order_list_main.122.48d71802vvI8wP

7 M3x15 Sockethead screws like the ones here: https://www.aliexpress.com/item/1005001550684837.html?pdp_npi=4%40dis%21EUR%21%E2%82%AC%200%2C74%21%E2%82%AC%200%2C74%21%21%215.69%215.69%21%402103867617268639029098123eebda%2112000031068154498%21sh%21FI%21164993959%21X&spm=a2g0o.store_pc_allItems_or_groupList.new_all_items_2007520972213.1005001550684837

9 Adafruit Neokey Breakout boards:  https://www.adafruit.com/product/4978

9 Cherry MX style keys of your choosing, i am using this ones: https://www.aliexpress.com/item/1005004285423123.html?spm=a2g0o.order_list.order_list_main.41.2ab41802PYQkfl

1 EC11 encoder: https://www.aliexpress.com/item/1005005983134515.html?spm=a2g0o.productlist.main.1.59981cefmhmORP&algo_pvid=cd3384ec-e2a9-4f68-a99a-698f2a878d6a&algo_exp_id=cd3384ec-e2a9-4f68-a99a-698f2a878d6a-0&pdp_npi=4%40dis%21EUR%213.08%213.08%21%21%213.36%213.36%21%40211b8f9717268640178527923ed2ea%2112000035172713577%21sea%21FI%21164993959%21X&curPageLogUid=2XoYaA6pnCOX&utparam-url=scene%3Asearch%7Cquery_from%3A

1 12 LED ring: https://www.aliexpress.com/item/1005007095317230.html?spm=a2g0o.productlist.main.3.380163f7Ggpq0l&algo_pvid=6f95773e-681a-47e8-a4e3-1f025a6296b6&algo_exp_id=6f95773e-681a-47e8-a4e3-1f025a6296b6-1&pdp_npi=4%40dis%21EUR%211.94%211.94%21%21%212.11%212.11%21%4021039e0c17268641627383864eaa02%2112000039385131520%21sea%21FI%21164993959%21X&curPageLogUid=LUV5RAVjJGsH&utparam-url=scene%3Asearch%7Cquery_from%3A

1 waveshare rp2040-zero: https://www.aliexpress.com/item/1005004827855053.html?spm=a2g0o.productlist.main.1.282e4592Heo3Ie&algo_pvid=b6debcd7-831e-4ed4-95ba-c15d01748c32&algo_exp_id=b6debcd7-831e-4ed4-95ba-c15d01748c32-0&pdp_npi=4%40dis%21EUR%215.66%215.66%21%21%216.17%216.17%21%40211b813c17268646064761648ee9c2%2112000030637156072%21sea%21FI%21164993959%21X&curPageLogUid=TM3IuMP4yuKZ&utparam-url=scene%3Asearch%7Cquery_from%3A

Cable of your picking. 

I use the following keys on my waveshare rp2040-zero

keyboard.row_pins = (board.GP0, board.GP1, board.GP2)  # Rows are on GP0, GP1, GP2
keyboard.col_pins = (board.GP3, board.GP4, board.GP5)  # Columns are on GP3, GP4, GP5

The LEDs under the keys are on GP28

The LED ring is on GP29
