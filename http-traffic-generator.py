# HTTP(S) Traffic Generator (trackthis.link on steroids)
# This script includes a large list of domains borrowed from trackthis.link.
#
# Written by Jaime Escalera (jescalera@sonicwall.com)
#
# The purpose of the script is to generate a high volume of web traffic.
# It can be used by network engineers for stress testing, bandwidth testing, etc.
# It can be used for the same purpose as trackthis.link -- to hide your
# online thumbprint by visiting a bunch of sites in various categories
# to hide your normal web browsing patterns.
#
#
# Requirements: I believe the only module not in the standard library is keyboard.
# Use 'pip3 install keyboard' to install the module.
#
# The script will do the following:
# 1. Minimize all windows (or active command line window used to launch the script)
#	Use the --minimize_all argument set to no to only minimize the command prompt.
#	The windows are minimized to avoid accidentally closing the wrong window
#	or placing focus on another window.
# !! IT IS VERY IMPORTANT THAT YOU REMAIN IDLE WHILE THE SCRIPT IS RUNNING. !!
# !! THIS SCRIPT LEVERAGES KEYBOARD INPUT TO CLOSE THE ACTIVE BROWSER
#	WINDOW AS WELL AS TO MINIMIZE/RESTORE THE COMMAND PROMPT WINDOW.
#	CLICKING ANOTHER WINDOW OR TYPING COULD LEAD TO THE SCRIPT CLOSING
#	OR GIVING FOCUS TO THE WRONG WINDOW. !!
#
# 2. Open a new web browser window and will visit each URL in configurable batches.
#	Each batch opens x number of browser tabs. Configurable using --tabs argument.
#	!! REMAIN PATIENT WHILE WINDOWS AND TABS OPEN/CLOSE. !!
#
# 3. Waits x number of seconds for the sites to load. Configurable using --hold_time argument.
#
# 4. Closes the browser window and launches a new one for the next batch.
#	!! YOU MAY EXPERIENCE A DELAY IN WINDOWS CLOSING/OPENING. THIS BECOMES
#	MORE NOTICEABLE THE MORE TABS YOU OPEN PER BATCH. I BELIEVE THIS BOILS
#	DOWN TO SYSTEM RESOURCES. !!
#
# 5. The process is repeated until all of the URLs are opened in tabs.
#	Use the --max_urls argument to specify a limit instead of processing the full list.
#
# 6. Finally, the remaining browser window should close.
#	The command prompt window will be restored in a few seconds.
#	!! BE PATIENT. THE SCRIPT SLEEPS FOR 5 SECONDS BEFORE ATTEMPTING TO
#	SWITCH THE ACTIVE WINDOW BACK TO THE COMMAND PROMPT. HOPEFULLY IT IS
#	ENOUGH TIME TO ALLOW THE BROWSER WINDOWS TO CLOSE. !!
#
# This script supports providing an input text file with a list of URLs.
# 	Use --input <filename> or <path to file>.
# If no input file is provided, the default list of nearly 800 URLs is used.
#
# The default number of passes is 1. Use --passes <integer> to use a custom
# 	number of passes.
#
# This script supports configuration via config.ini, placed in the same
#	directory as the script file. Launch with --conf argument.
# Configuration items are the same as CLI arguments.
# input = <filename.txt> OR <c:\path\to\file\filename.txt> OR </path/to/file/filename.txt>
#	If input value is blank, use the large built-in list of URLs.
#	If a file is given without a path, assume it is in the script's directory.
#	If input file is not found, script will use the built-in URL list.
#
# -- Configuration example --
# passes = <integer>
# tabs = <integer>
# hold time = <integer>
# shuffle urls = <yes> OR <no>
# minimize all = <yes> OR <no>
# max urls = <integer>
#	If max urls value is empty, set no max. Processes all URLs in file/list.
#
#
# Version 1.0.0:
#	1-16-2020: Calling this newly enhanced version 1.0.
#
# Version 1.0.1:
#	1-17-2020: Added config.ini support, input file path handling, and
#		a number of other enhancements and little extras.
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
version_string = '1.0.1'


# Imports
import webbrowser
import argparse
import keyboard
import time
import random
import os
import configparser


# Input list. FYI: There are many duplicated entries in this list.
input_list = ["https://www.supremenewyork.com/shop","https://stockx.com/","https://www.flightclub.com/","https://www.goat.com/","https://www.stadiumgoods.com/","https://shop.doverstreetmarket.com/us/","https://kith.com/pages/shop-treats","https://www.footlocker.com/","https://us.octobersveryown.com/","https://www.zumiez.com/odd-future-donut-allover-light-blue-crew-socks.html","https://www.canadagoose.com/ca/en/home-page","https://www.a-cold-wall.com/department/all/","https://www.grailed.com/","https://www.kicksonfire.com/","https://kinfolk.com/","https://www.nike.com/us/en_us/c/jordan","https://13month.com/product/collection_list.html?cate_no=103","https://dbtkco.com/","https://have-a-good-time.us/","https://canary---yellow.com/","https://www.youngmoney.com/","https://shop.kanyewest.com/password","https://unhappy.com/","https://travisscott.com/","https://fkatwi.gs/","https://drakeofficial.com/","https://good-music.com/","https://hypebeast.com/music","https://tankmagazine.com/","https://www.meninthistown.com/","https://humanbeing.co/","https://thegentlewoman.co.uk/magazine","https://1granary.com/journal/","http://www.papermag.com/","https://www.sneezemag.com/","https://recenspaper.com/","https://buffalozine.com/","https://www.xxlmag.com/","https://hiphopwired.com/","https://sneakernews.com/","https://footwearnews.com/","https://www.vice.com/en_us","https://www.highsnobiety.com/","https://www.complex.com/","https://www.sneakerfreaker.com/","https://hypebae.com/","https://supercopbot.com/","https://forcecop.com/","http://www.in-n-out.com/","https://www.jonandvinnys.com/","https://www.thrashermagazine.com/","https://store.pizzaslime.com/","https://www.cavempt.com/","https://www.wtaps.com/","https://www.streetwearofficial.com/","https://www.supremelosangeles.com/","https://www.stoneisland.com/us","https://www.crooksncastles.com/","https://thehundreds.com/","https://www.thenorthface.com/""https://www.louisvuitton.com/","https://www.ripndipclothing.com/","https://www.champion.com/","https://santacruzskateboards.com/","https://www.zumiez.com/","https://us.carhartt-wip.com/","https://www.justflip.com/","https://undefeated.com/","https://lacedup.com/","https://vetementswebsite.com/","https://www.hyeinseo.com/","https://www.moncler.com/gb/us/","https://www.antisocialsocialclub.com/","https://www.nike.com/launch/","https://polarskateco.com/","https://www.patta.nl/","https://www.palaceskateboards.com/","https://obeyclothing.com/","https://www.supremenewyork.com/","https://hypebeast.com/","https://www.bbcicecream.com/","https://www.stussy.com/","https://bape.com/index/","https://yeezysupply.com/","https://www.adidas.com/us/yeezy","https://www.balenciaga.com/us","https://www.off---white.com/en/US","https://kith.com/","https://www.heronpreston.com/en/US","https://thehouseofdrew.com/","https://www.vans.com/","https://www.crepprotect.com/","https://hbx.com/","https://www.eastbay.com/","https://www.jdsports.co.uk/","https://www.complexcon.com/","https://sneakercon.com/","https://www.luxurycard.com/goldcard","https://www.americanexpress.com/us/credit-cards/card-application/apply/platinum-charge-card/26129-10-0?pmccode=137&intlink=US-Acq-Shop-Consumer-CardDetails-Platinum-Prospect-Apply-Platinum-Header#/","https://combatgent.com/collections/sale","https://www.dstld.com/shop/womens","https://www.jhilburn.com/catalog/keylooks","https://www.acorns.com/","https://bellagio.mgmresorts.com/en.html","https://www.lurssen.com/en/","https://www.perininavi.it/","https://www.sunseeker.com/en-GB/","https://www.ferragamo.com/shop/us/en","https://www.manoloblahnik.com/us/","https://us.jimmychoo.com/en/home","https://www.patek.com/en/home","https://www.bulgari.com/en-us/","https://www.graff.com/","https://www.zara.com/us/","https://www.bmw.com/en/index.html","https://www.versace.com/us/en-us/home/","https://www.marcjacobs.com/","https://www.elliman.com/hamptons","https://www.germanhorsecenter.com/dressage-horses.html","https://www.christiesrealestate.com/eng/sales/tca/private-island-type","https://www.harneyre.com/features/horse-property/","https://www.danielgale.com/horse-properties","https://www.horseproperties.net/properties/new+york","https://lesliegarfield.com/properties/new-york","https://www.halstead.com/sales/hamptons/properties/tennis/","https://www.sothebysrealty.com/eng/sales/beverly-hills-ca-usa","https://www.corcoran.com/hamptons","https://www.nobleblack.com/properties/sale","https://www.stribling.com/","https://www.bhsusa.com/the-hamptons","https://thepointsguy.com/","https://www.thestreet.com/","https://www.thisismoney.co.uk/money/index.html","https://www.kiplinger.com/","https://money.cnn.com/data/markets/","https://www.stockpile.com/","https://www.betterment.com/","https://www.wealthbase.com/","https://us.etrade.com/home","https://www.coinbase.com/","https://www.ally.com/","https://robinhood.com/","https://www.ml.com/","https://finance.yahoo.com/","https://www.investopedia.com/","https://www.fool.com/","https://hakkasan.com/","https://marqueeny.com/","https://www.kittycatklub.net/","https://mgmgrand.mgmresorts.com/en.html","https://www.caesarscasino.com/","https://www.tomorrowland.com/global/","https://electriczoo.com/","https://www.amnesia.es/allevents/0/en/all-amnesia-tickets.html","https://www.standardhotels.com/new-york/features/biergarten-nyc","https://phdlounge.com/","https://www.bwin.com/","https://www.bet365.com/en/","https://lavony.com/","https://taodowntown.com/","https://www.katerblau.de/","https://www.christensenyachts.com/","https://www.alexandermcqueen.com/us","https://brianatwood.com/","https://www.stuartweitzman.com/home/","https://www.ulysse-nardin.com/","https://www.blancpain.com/en","https://www.girard-perregaux.com/en","https://www.breguet.com/en","https://www.vacheron-constantin.com/en2/home.html","https://www.piaget.com/","https://www.vancleefarpels.com/us/en.html","https://www.harrywinston.com/en","https://www.bugatti.com/","https://www.rolex.com/","https://www.cartier.com/","https://us.burberry.com/","https://www.coach.com/","https://www.dolcegabbana.com/","https://www.armani.com/us/armanicom","https://www.tiffany.com/","https://www.fendi.com/us","https://www.dior.com/en_us","https://www.chanel.com/us/","https://www.hermes.com/us/en/","https://us.louisvuitton.com/eng-us/homepage","https://www.oscardelarenta.com/","https://www.jaguarusa.com/index.html","https://www.lexus.com/","https://www.porsche.com/usa/","https://www.ferrari.com/en-US","https://www.audiusa.com/","https://www.mbusa.com/en/home","https://www.dickssportinggoods.com/p/potable-aqua-water-purification-tablets-16paquptblqxxxxxxcac/16paquptblqxxxxxxcac","https://www.walmart.com/ip/20-PACK-Emergency-Solar-Blanket-Survival-Safety-Insulating-Mylar-Thermal-Heat/749865211","https://www.rticcoolers.com/shop/coolers/softpak/Soft-Pack-30-Grey","https://www.getprepd.com/products/prepd-pack","https://www.tortugabackpacks.com/products/setout-duffle-bag","https://naturalforce.com/","https://www.kuiu.com/hunting-rain-gear/northridge-rain-jacket/14012.html?cgid=rain-gear&dwvar_14012_color=Verde2.0#start=4","https://wpstandard.com/439252/checkouts/28e47c486ce4f5fac99b82eb078e7c98","https://www.battlbox.com/","https://survivalist101.com/tutorials/preppers-guide-prepping-for-beginners/","https://www.amazon.com/Augason-Farms-Emergency-Servings-Calories/dp/B071KPGLBK?ref_=fsclp_pl_dp_12","https://www.amazon.com/Wise-Company-Serving-13x9x10-Inch-11-Pounds/dp/B004JTASAK?ref_=fsclp_pl_dp_11","https://www.amazon.com/Complete-Earthquake-Bag-Earthquakes-Hurricanes/dp/B07C9R2SH6?ref_=fsclp_pl_dp_10","https://www.amazon.com/Backpacking-Cycling-Waterproof-Laminate-Adventures/dp/B01HGSLB6K?ref_=fsclp_pl_dp_9","https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/N-5yc1vZbx5c","https://www.amazon.com/EVERLIT-Earthquake-Emergency-Hurricanes-Hand-Crank/dp/B07BFRV7K5?ref_=fsclp_pl_dp_6","https://www.amazon.com/Hour-Plus-Emergency-Candle-Clear/dp/B007KAX77G?ref_=fsclp_pl_dp_3","https://www.amazon.com/Five-Day-Survival-Pack-Camo/dp/B00I3LYJRI?ref_=fsclp_pl_dp_2","https://www.amazon.com/LifeStraw-Personal-Camping-Emergency-Preparedness/dp/B006QF3TW4/ref=pd_bxgy_2/142-8109673-6143527?_encoding=UTF8&pd_rd_i=B006QF3TW4&pd_rd_r=108b95eb-7cc7-11e9-ad0c-33f6b98a7451&pd_rd_w=X6peP&pd_rd_wg=v8b0j&pf_rd_p=a2006322-0bc0-4db9-a08e-d168c18ce6f0&pf_rd_r=QGCMMQRV8W6ZMAGB7T1J&psc=1&refRID=QGCMMQRV8W6ZMAGB7T1J","https://www.amazon.com/Potable-Aqua-Water-Purification-Treatment/dp/B001949TKS/ref=pd_bxgy_3/142-8109673-6143527?encoding=UTF8&pd_rd_i=B001949TKS&pd_rd_r=108b95eb-7cc7-11e9-ad0c-33f6b98a7451&pd_rd_w=X6peP&pd_rd_wg=v8b0j&pf_rd_p=a2006322-0bc0-4db9-a08e-d168c18ce6f0&pf_rd_r=QGCMMQRV8W6ZMAGB7T1J&psc=1&refRID=QGCMMQRV8W6ZMAGB7T1J","https://www.amazon.com/Emergency-Zone-840-2-Survival-Disaster/dp/B008HHX15Y?ref_=fsclp_pl_dp_1","https://www.bbcamerica.com/anglophenia/2018/03/10-apocalyptic-tv-shows-that-will-make-you-appreciate-life","https://www.spin.com/2017/02/tom-delonge-ufo-researcher-of-the-year-award-video/","https://variety.com/2018/music/news/tom-delonge-blink-182-strange-times-paranormal-1203083329/?fbclid=IwAR1UCFz0NwMDfuEOzO10d3Qzq--BLCqV_ZM-Sp7yjVFszi-HL3HdZ03NHp0","https://bloody-disgusting.com/tv/3546528/rumor-two-alien-franchise-tv-shows-works-one-ridley-scott-hulu/","https://www.syfy.com/aliennewsdesk","https://www.history.com/shows/ancient-aliens","https://pksafety.com/hazmat-suits/","https://slate.com/culture/2012/04/doomsday-preppers-on-national-geographic-is-the-survivalist-reality-show-exploitative.html","https://www.history.com/shows/project-blue-book","https://www.history.com/shows/alone","https://newrepublic.com/article/111393/walking-dead-doomsday-preppers-what-tv-post-apocalypse-fantasies-tell-","https://apartmentprepper.com/what-doomsday-films-and-shows-do-for-preppers/","https://survivalistprepper.net/prepper-movies-you-can-watch-instantly-on-netflix-amazon-or-youtube/","https://www.primalsurvivor.net/doomsday-movies/","https://urbansurvivalsite.com/20-best-prepper-survivalist-shows-netflix/","https://www.trueprepper.com/prepper-tv-shows/","https://www.sapiens.org/culture/preppers/","https://bugoutbagacademy.com/13-survival-kit-list-items/","https://montemlife.com/how-to-make-a-survival-kit/","https://eartheasy.com/off-grid-preparedness/","https://www.nitro-pak.com/black-friday/high-peak-alpinizmo-pilot-0-f-rectangular-sleeping-bag-with-free-stuff-sack-for-adult-camping-travel","https://www.nitro-pak.com/survival-kits/survival-supplies","https://www.selfrelianceoutfitters.com/collections/survival-gear","https://www.cabelas.com/category/Safety-Survival/104774580.uts","https://totalprepare.ca/","https://mypatriotsupply.com/","https://www.survivalistetc.com/category/survival-medicine/","https://prepperbroadcasting.com/medical/doomsday-medicine/","https://geekprepper.com/edc-survival-flashlight-buyers-guide/","https://www.amazon.com/slp/hazmat-suits/yxwaqjv5d5su8hu","https://www.scmp.com/news/world/united-states-canada/article/2124634/look-thing-dude-us-fighter-pilots-track-ufo-new","https://www.scmp.com/news/world/united-states-canada/article/2124872/us-government-admits-it-studies-ufos-so-about-those","https://content.time.com/time/specials/packages/article/0,28804,1860871_1860876_1861006,00.html","https://video.vice.com/en_us/show/motherboard-spaced-out","https://video.vice.com/en_us/video/the-man-who-hunts-spy-satellites/559be69ea8feaf3c462823a0","https://www.worldufoday.com/about-world-ufo-day/whatwherewhywhen/","https://www.vice.com/en_us/article/z43ygx/some-of-the-very-best-alien-conspiracy-theories-world-ufo-day","https://nymag.com/intelligencer/2019/05/los-angeles-fire-season-will-never-end.html","https://nymag.com/intelligencer/2018/03/13-reasons-to-believe-aliens-are-real.html","https://theprepared.com/prepping-basics/guides/survival-disaster-prepper-myths/","https://theweek.com/articles/565576/preppers-meet-paranoid-americans-awaiting-apocalypse","https://www.thehomesecuritysuperstore.com/collections/survival-flashlights","https://www.thebugoutbagguide.com/best-survival-flashlight/","https://survivorsfortress.com/10-best-survival-flashlights/","https://www.walmart.com/cp/4128","https://www.99boulders.com/best-water-purification-tablets","https://www.wisefoodstorage.com/","https://www.wholesalesurvivalkits.com/","https://www.thekeytosurvival.com/","https://www.chemsuits.com/hazmat-suits.html","https://www.sosproducts.com/","https://www.skilledsurvival.com/preppers-checklist/","https://www.skilledsurvival.com/free-bug-out-bag-checklist/","https://www.safetykitstore.com/bulkitems.html","https://www.redcross.org/get-help/how-to-prepare-for-emergencies/survival-kit-supplies.html","https://www.quakekare.com/","https://www.outdoorlife.com/blogs/survivalist/6-doomsday-supplies-youve-understocked","https://www.rei.com/product/407104/space-emergency-blanket","https://www.moreprepared.com/","https://www.galls.com/2017-09-survival-gear-sale","https://www.forgesurvivalsupply.com/","https://www.doomsdayprep.com/shop/bear-grylls-sliding-saw/","https://www.doomsdayprep.com/shop/165pc-first-aid-kit/","https://www.dollardays.com/wholesale-survival-gear.html","https://unchartedsupplyco.com/blogs/news/bug-out-bag-checklist","https://thepreppingguide.com/prepping-on-a-budget/","https://theprepared.com/prepping-basics/guides/emergency-preparedness-checklist-prepping-beginners/","https://prepperworld.org/bug-out-bags-emergency-survival-kits/","https://echo-sigma.com/","https://americansurvivalwholesale.com/","https://www.maydaysupplies.com/","https://www.primalsurvivor.net/mylar-space-blankets/","https://www.rei.com/c/camping-tents","https://www.timberland.com/shop/mens-boots","https://www.lowes.com/","https://www.coleman.com/coleman-sleepingbagsandbeds/","https://www.ramseyoutdoor.com/?SID=7vbjnejkqipdc8blj9n5eecej3","https://www.basspro.com/shop/en/camping","https://www.overstock.com/Sports-Toys/Camping-Hiking/2226/cat.html","https://mpgsport.com/collections/women?sscid=51k3_a95sy&utm_campaign=314743_851401&utm_medium=affiliate&utm_source=shareasale","https://www.welleco.com/","https://www.thirdlove.com/","https://www.sugarbearhair.com/","https://ritual.com/","https://www.chubbiesshorts.com/","https://www.stitchfix.com/","https://www.meundies.com/","https://www.glossier.com/","https://www.garnierusa.com/","https://www.katvondbeauty.com/sale","https://www.marcjacobsbeauty.com/","https://www.anastasiabeverlyhills.com/","https://www.chanel.com/us/makeup/p/172444/rouge-coco-ultra-hydrating-lip-colour/","https://www.makebeauty.com/","https://www.newbeauty.com/blog/skin-care/","https://www.loreal.com/","https://shop.goop.com/shop/collection/beauty/skincare/mask?country=USA","https://shop.goop.com/shop/products/revitalizing-day-moisturizer?taxon_id=622&country=USA","https://www.warbyparker.com/sunglasses/men","https://www.marriott.com/default.mi","https://www.priceline.com/","https://www.tripadvisor.com/","https://www.trivago.com/","https://www.kayak.com/","https://flights.idealo.com/","https://www.themileageclub.com/","https://www.united.com/en/us","https://www.gohawaii.com/islands/maui","https://www.booking.com/","https://visitmaldives.com/","https://www.travelzoo.com/","https://www.visitjamaica.com/plan-your-trip/","https://www.groupon.com/getaways","https://www.caribbeantravel.com/","https://www.expedia.com/Flights","https://www.kiragrace.com/giving-back/","https://www.prana.com/","https://carrotbananapeach.com/","https://www.earthyogaclothing.com/","https://www.greenappleactive.com/","https://teeki.com/","https://shop.lululemon.com/","https://asanarebel.com/","https://www.downdogapp.com/","https://www.glo.com/","https://www.headspace.com/","https://www.tenpercent.com/mindfulness-meditation-the-basics/","https://style.fabletics.com/dms25640/?bp=0&ccode=10078&clabel=Skimbit%20Ltd.&clickid=TvxSIqzSjxyJU210EWQ:NRupUkl16RVRwU1nTM0&code=DE27FD&iradid=252615&mpid=10078&pcode=Impact_Radius_Fabletics_US&plabel=&scode=&sharedid=&slabel=&utm_campaign=Impact_Radius_Fabletics_US_Skimbit%20Ltd.&utm_content=&utm_medium=affiliate&utm_source=IRS","https://www.caliastudio.com/f/calia-yoga","https://www.astrologyhub.com/the-top-7-best-selling-astrology-books/","https://www.healingcrystals.com/","https://www.sagegoddess.com/?gclid=EAIaIQobChMItM-475qZ4gIVCRgMCh3kgg4BEAAYAyAAEgKc7vD_BwE","https://i-d.vice.com/en_us","https://lovewellness.co/","https://juicebeauty.com/?ranMID=38268&ranEAID=TnL5HPStwNw&utm_source=Skimlinks.com&utm_medium=affiliate&utm_campaign=&ranSiteID=TnL5HPStwNw-Bl6LYgTaAvKprUai4FkqJw&siteID=TnL5HPStwNw-Bl6LYgTaAvKprUai4FkqJw&LSNSUBSITE=Omitted_TnL5HPStwNw","https://supergoop.com/","https://www.anthropologie.com/wellness","https://www.freepeople.com/wellness-products/","https://holistichealeronline.com/","https://shop.goop.com/shop/products/city-skin-potion-trio?taxon_id=1291&country=USA","https://fabfitfun.com/get-the-box/?step=getbox&origin=welcome","https://aloha.com/","https://www.maharose.com/","https://www.costarastrology.com/","https://www.gotoskincare.com/","https://www.lorealparisusa.com/","https://www.laprairie.com/","https://www.bareminerals.com/","https://www.urbandecay.com/","https://www.honestbeauty.com/products/creme-blush","https://www.firstaidbeauty.com/","https://www.narscosmetics.com/","https://www.stilacosmetics.com/","https://www.shopreedclarke.com/products?tag=Fiona%20Stiles%20Beauty","https://www.beccacosmetics.com/","https://www.eyeko.com/","https://www.proactiv.com/","https://www.kyliecosmetics.com/","https://www.allure.com/story/kylie-jenner-skin-care-products-prices-details","https://www.dermstore.com/product_Advanced+Night+Repair+Concentrated+Recovery+PowerFoil+Mask_77441.htm?gclid=CjwKCAjwq-TmBRBdEiwAaO1en9ZRE6ntl_8u-rSz0XqhkGaOYnH7zgQING_HaSBTkDXFfYNNj3WlQhoChAYQAvD_BwE&scid=scplp77441&sc_intid=77441&iv_=__iv_p_1_g_73713728321_c_347170226830_w_aud-318912418799%3Apla-313456374895_n_g_d_c_v__l__t__r_1o4_x_pla_y_6790012_f_online_o_77441_z_US_i_en_j_313456374895_s__e__h_9004338_ii__vi__&utm_source=fro&utm_medium=paid_search&utm_term=makeup&utm_campaign=505479","https://www.sephora.com/","https://www.ulta.com/skin-care-treatment-serums-face-masks?N=27hf","https://www.shiseido.com/","https://www.esteelauder.com/","https://www.dove.com/us/en/home.html","https://www.lushusa.com/","https://www.covergirl.com/","https://www.stives.com/","https://www.potionnaturals.com/","https://www.revolve.com/","https://www.maccosmetics.com/home","https://www.aesop.com/us/","https://www.sprezzabox.com/","https://www.adoreme.com/","https://www.allbirds.com/","https://www.outdoorvoices.com/","https://www.graze.com/us","https://www.drinkhint.com/","https://www.ysl.com/us","https://www.prada.com/us/en.html","https://www.gucci.com/us/en/","https://www.lancome-usa.com/","https://www.supremenewyork.com/shop","https://stockx.com/","https://www.flightclub.com/","https://www.goat.com/","https://www.stadiumgoods.com/","https://shop.doverstreetmarket.com/us/","https://kith.com/pages/shop-treats","https://www.footlocker.com/","https://us.octobersveryown.com/","https://www.zumiez.com/odd-future-donut-allover-light-blue-crew-socks.html","https://www.canadagoose.com/ca/en/home-page","https://www.a-cold-wall.com/department/all/","https://www.grailed.com/","https://www.kicksonfire.com/","https://kinfolk.com/","https://www.nike.com/us/en_us/c/jordan","https://13month.com/product/collection_list.html?cate_no=103","https://dbtkco.com/","https://have-a-good-time.us/","https://canary---yellow.com/","https://www.youngmoney.com/","https://shop.kanyewest.com/password","https://unhappy.com/","https://travisscott.com/","https://fkatwi.gs/","https://drakeofficial.com/","https://good-music.com/","https://hypebeast.com/music","https://tankmagazine.com/","https://www.meninthistown.com/","https://humanbeing.co/","https://thegentlewoman.co.uk/magazine","https://1granary.com/journal/","http://www.papermag.com/","https://www.sneezemag.com/","https://recenspaper.com/","https://buffalozine.com/","https://www.xxlmag.com/","https://hiphopwired.com/","https://sneakernews.com/","https://footwearnews.com/","https://www.vice.com/en_us","https://www.highsnobiety.com/","https://www.complex.com/","https://www.sneakerfreaker.com/","https://hypebae.com/","https://supercopbot.com/","https://forcecop.com/","http://www.in-n-out.com/","https://www.jonandvinnys.com/","https://www.thrashermagazine.com/","https://store.pizzaslime.com/","https://www.cavempt.com/","https://www.wtaps.com/","https://www.streetwearofficial.com/","https://www.supremelosangeles.com/","https://www.stoneisland.com/us","https://www.crooksncastles.com/","https://thehundreds.com/","https://www.thenorthface.com/","https://www.louisvuitton.com/","https://www.ripndipclothing.com/","https://www.champion.com/","https://santacruzskateboards.com/","https://www.zumiez.com/","https://us.carhartt-wip.com/","https://www.justflip.com/","https://undefeated.com/","https://lacedup.com/","https://vetementswebsite.com/","https://www.hyeinseo.com/","https://www.moncler.com/gb/us/","https://www.antisocialsocialclub.com/","https://www.nike.com/launch/","https://polarskateco.com/","https://www.patta.nl/","https://www.palaceskateboards.com/","https://obeyclothing.com/","https://www.supremenewyork.com/","https://hypebeast.com/","https://www.bbcicecream.com/","https://www.stussy.com/","https://bape.com/index/","https://yeezysupply.com/","https://www.adidas.com/us/yeezy","https://www.balenciaga.com/us","https://www.off---white.com/en/US","https://kith.com/","https://www.heronpreston.com/en/US","https://thehouseofdrew.com/","https://www.vans.com/","https://www.crepprotect.com/","https://hbx.com/","https://www.eastbay.com/","https://www.jdsports.co.uk/","https://www.complexcon.com/","https://sneakercon.com/","https://www.luxurycard.com/goldcard","https://www.americanexpress.com/us/credit-cards/card-application/apply/platinum-charge-card/26129-10-0?pmccode=137&intlink=US-Acq-Shop-Consumer-CardDetails-Platinum-Prospect-Apply-Platinum-Header#/","https://combatgent.com/collections/sale","https://www.dstld.com/shop/womens","https://www.jhilburn.com/catalog/keylooks","https://www.acorns.com/","https://bellagio.mgmresorts.com/en.html","https://www.lurssen.com/en/","https://www.perininavi.it/","https://www.sunseeker.com/en-GB/","https://www.ferragamo.com/shop/us/en","https://www.manoloblahnik.com/us/","https://us.jimmychoo.com/en/home","https://www.patek.com/en/home","https://www.bulgari.com/en-us/","https://www.graff.com/","https://www.zara.com/us/","https://www.bmw.com/en/index.html","https://www.versace.com/us/en-us/home/","https://www.marcjacobs.com/","https://www.elliman.com/hamptons","https://www.germanhorsecenter.com/dressage-horses.html","https://www.christiesrealestate.com/eng/sales/tca/private-island-type","https://www.harneyre.com/features/horse-property/","https://www.danielgale.com/horse-properties","https://www.horseproperties.net/properties/new+york","https://lesliegarfield.com/properties/new-york","https://www.halstead.com/sales/hamptons/properties/tennis/","https://www.sothebysrealty.com/eng/sales/beverly-hills-ca-usa","https://www.corcoran.com/hamptons","https://www.nobleblack.com/properties/sale","https://www.stribling.com/","https://www.bhsusa.com/the-hamptons","https://thepointsguy.com/","https://www.thestreet.com/","https://www.thisismoney.co.uk/money/index.html","https://www.kiplinger.com/","https://money.cnn.com/data/markets/","https://www.stockpile.com/","https://www.betterment.com/","https://www.wealthbase.com/","https://us.etrade.com/home","https://www.coinbase.com/","https://www.ally.com/","https://robinhood.com/","https://www.ml.com/","https://finance.yahoo.com/","https://www.investopedia.com/","https://www.fool.com/","https://hakkasan.com/","https://marqueeny.com/","https://www.kittycatklub.net/","https://mgmgrand.mgmresorts.com/en.html","https://www.caesarscasino.com/","https://www.tomorrowland.com/global/","https://electriczoo.com/","https://www.amnesia.es/allevents/0/en/all-amnesia-tickets.html","https://www.standardhotels.com/new-york/features/biergarten-nyc","https://phdlounge.com/","https://www.bwin.com/","https://www.bet365.com/en/","https://lavony.com/","https://taodowntown.com/","https://www.katerblau.de/","https://www.christensenyachts.com/","https://www.alexandermcqueen.com/us","https://brianatwood.com/","https://www.stuartweitzman.com/home/","https://www.ulysse-nardin.com/","https://www.blancpain.com/en","https://www.girard-perregaux.com/en","https://www.breguet.com/en","https://www.vacheron-constantin.com/en2/home.html","https://www.piaget.com/","https://www.vancleefarpels.com/us/en.html","https://www.harrywinston.com/en","https://www.bugatti.com/","https://www.rolex.com/","https://www.cartier.com/","https://us.burberry.com/","https://www.coach.com/","https://www.dolcegabbana.com/","https://www.armani.com/us/armanicom","https://www.tiffany.com/","https://www.fendi.com/us","https://www.dior.com/en_us","https://www.chanel.com/us/","https://www.hermes.com/us/en/","https://us.louisvuitton.com/eng-us/homepage","https://www.oscardelarenta.com/","https://www.jaguarusa.com/index.html","https://www.lexus.com/","https://www.porsche.com/usa/","https://www.ferrari.com/en-US","https://www.audiusa.com/","https://www.mbusa.com/en/home","https://www.dickssportinggoods.com/p/potable-aqua-water-purification-tablets-16paquptblqxxxxxxcac/16paquptblqxxxxxxcac","https://www.walmart.com/ip/20-PACK-Emergency-Solar-Blanket-Survival-Safety-Insulating-Mylar-Thermal-Heat/749865211","https://www.rticcoolers.com/shop/coolers/softpak/Soft-Pack-30-Grey","https://www.getprepd.com/products/prepd-pack","https://www.tortugabackpacks.com/products/setout-duffle-bag","https://naturalforce.com/","https://www.kuiu.com/hunting-rain-gear/northridge-rain-jacket/14012.html?cgid=rain-gear&dwvar_14012_color=Verde2.0#start=4","https://wpstandard.com/439252/checkouts/28e47c486ce4f5fac99b82eb078e7c98","https://www.battlbox.com/","https://survivalist101.com/tutorials/preppers-guide-prepping-for-beginners/","https://www.amazon.com/Augason-Farms-Emergency-Servings-Calories/dp/B071KPGLBK?ref_=fsclp_pl_dp_12","https://www.amazon.com/Wise-Company-Serving-13x9x10-Inch-11-Pounds/dp/B004JTASAK?ref_=fsclp_pl_dp_11","https://www.amazon.com/Complete-Earthquake-Bag-Earthquakes-Hurricanes/dp/B07C9R2SH6?ref_=fsclp_pl_dp_10","https://www.amazon.com/Backpacking-Cycling-Waterproof-Laminate-Adventures/dp/B01HGSLB6K?ref_=fsclp_pl_dp_9","https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/N-5yc1vZbx5c","https://www.amazon.com/EVERLIT-Earthquake-Emergency-Hurricanes-Hand-Crank/dp/B07BFRV7K5?ref_=fsclp_pl_dp_6","https://www.amazon.com/Hour-Plus-Emergency-Candle-Clear/dp/B007KAX77G?ref_=fsclp_pl_dp_3","https://www.amazon.com/Five-Day-Survival-Pack-Camo/dp/B00I3LYJRI?ref_=fsclp_pl_dp_2","https://www.amazon.com/LifeStraw-Personal-Camping-Emergency-Preparedness/dp/B006QF3TW4/ref=pd_bxgy_2/142-8109673-6143527?_encoding=UTF8&pd_rd_i=B006QF3TW4&pd_rd_r=108b95eb-7cc7-11e9-ad0c-33f6b98a7451&pd_rd_w=X6peP&pd_rd_wg=v8b0j&pf_rd_p=a2006322-0bc0-4db9-a08e-d168c18ce6f0&pf_rd_r=QGCMMQRV8W6ZMAGB7T1J&psc=1&refRID=QGCMMQRV8W6ZMAGB7T1J","https://www.amazon.com/Potable-Aqua-Water-Purification-Treatment/dp/B001949TKS/ref=pd_bxgy_3/142-8109673-6143527?encoding=UTF8&pd_rd_i=B001949TKS&pd_rd_r=108b95eb-7cc7-11e9-ad0c-33f6b98a7451&pd_rd_w=X6peP&pd_rd_wg=v8b0j&pf_rd_p=a2006322-0bc0-4db9-a08e-d168c18ce6f0&pf_rd_r=QGCMMQRV8W6ZMAGB7T1J&psc=1&refRID=QGCMMQRV8W6ZMAGB7T1J","https://www.amazon.com/Emergency-Zone-840-2-Survival-Disaster/dp/B008HHX15Y?ref_=fsclp_pl_dp_1","https://www.bbcamerica.com/anglophenia/2018/03/10-apocalyptic-tv-shows-that-will-make-you-appreciate-life","https://www.spin.com/2017/02/tom-delonge-ufo-researcher-of-the-year-award-video/","https://variety.com/2018/music/news/tom-delonge-blink-182-strange-times-paranormal-1203083329/?fbclid=IwAR1UCFz0NwMDfuEOzO10d3Qzq--BLCqV_ZM-Sp7yjVFszi-HL3HdZ03NHp0","https://bloody-disgusting.com/tv/3546528/rumor-two-alien-franchise-tv-shows-works-one-ridley-scott-hulu/","https://www.syfy.com/aliennewsdesk","https://www.history.com/shows/ancient-aliens","https://pksafety.com/hazmat-suits/","https://slate.com/culture/2012/04/doomsday-preppers-on-national-geographic-is-the-survivalist-reality-show-exploitative.html","https://www.history.com/shows/project-blue-book","https://www.history.com/shows/alone","https://newrepublic.com/article/111393/walking-dead-doomsday-preppers-what-tv-post-apocalypse-fantasies-tell-","https://apartmentprepper.com/what-doomsday-films-and-shows-do-for-preppers/","https://survivalistprepper.net/prepper-movies-you-can-watch-instantly-on-netflix-amazon-or-youtube/","https://www.primalsurvivor.net/doomsday-movies/","https://urbansurvivalsite.com/20-best-prepper-survivalist-shows-netflix/","https://www.trueprepper.com/prepper-tv-shows/","https://www.sapiens.org/culture/preppers/","https://bugoutbagacademy.com/13-survival-kit-list-items/","https://montemlife.com/how-to-make-a-survival-kit/","https://eartheasy.com/off-grid-preparedness/","https://www.nitro-pak.com/black-friday/high-peak-alpinizmo-pilot-0-f-rectangular-sleeping-bag-with-free-stuff-sack-for-adult-camping-travel","https://www.nitro-pak.com/survival-kits/survival-supplies","https://www.selfrelianceoutfitters.com/collections/survival-gear","https://www.cabelas.com/category/Safety-Survival/104774580.uts","https://totalprepare.ca/","https://mypatriotsupply.com/","https://www.survivalistetc.com/category/survival-medicine/","https://prepperbroadcasting.com/medical/doomsday-medicine/","https://geekprepper.com/edc-survival-flashlight-buyers-guide/","https://www.amazon.com/slp/hazmat-suits/yxwaqjv5d5su8hu","https://www.scmp.com/news/world/united-states-canada/article/2124634/look-thing-dude-us-fighter-pilots-track-ufo-new","https://www.scmp.com/news/world/united-states-canada/article/2124872/us-government-admits-it-studies-ufos-so-about-those","https://content.time.com/time/specials/packages/article/0,28804,1860871_1860876_1861006,00.html","https://video.vice.com/en_us/show/motherboard-spaced-out","https://video.vice.com/en_us/video/the-man-who-hunts-spy-satellites/559be69ea8feaf3c462823a0","https://www.worldufoday.com/about-world-ufo-day/whatwherewhywhen/","https://www.vice.com/en_us/article/z43ygx/some-of-the-very-best-alien-conspiracy-theories-world-ufo-day","https://nymag.com/intelligencer/2019/05/los-angeles-fire-season-will-never-end.html","https://nymag.com/intelligencer/2018/03/13-reasons-to-believe-aliens-are-real.html","https://theprepared.com/prepping-basics/guides/survival-disaster-prepper-myths/","https://theweek.com/articles/565576/preppers-meet-paranoid-americans-awaiting-apocalypse","https://www.thehomesecuritysuperstore.com/collections/survival-flashlights","https://www.thebugoutbagguide.com/best-survival-flashlight/","https://survivorsfortress.com/10-best-survival-flashlights/","https://www.walmart.com/cp/4128","https://www.99boulders.com/best-water-purification-tablets","https://www.wisefoodstorage.com/","https://www.wholesalesurvivalkits.com/","https://www.thekeytosurvival.com/","https://www.chemsuits.com/hazmat-suits.html","https://www.sosproducts.com/","https://www.skilledsurvival.com/preppers-checklist/","https://www.skilledsurvival.com/free-bug-out-bag-checklist/","https://www.safetykitstore.com/bulkitems.html","https://www.redcross.org/get-help/how-to-prepare-for-emergencies/survival-kit-supplies.html","https://www.quakekare.com/","https://www.outdoorlife.com/blogs/survivalist/6-doomsday-supplies-youve-understocked","https://www.rei.com/product/407104/space-emergency-blanket","https://www.moreprepared.com/","https://www.galls.com/2017-09-survival-gear-sale","https://www.forgesurvivalsupply.com/","https://www.doomsdayprep.com/shop/bear-grylls-sliding-saw/","https://www.doomsdayprep.com/shop/165pc-first-aid-kit/","https://www.dollardays.com/wholesale-survival-gear.html","https://unchartedsupplyco.com/blogs/news/bug-out-bag-checklist","https://thepreppingguide.com/prepping-on-a-budget/","https://theprepared.com/prepping-basics/guides/emergency-preparedness-checklist-prepping-beginners/","https://prepperworld.org/bug-out-bags-emergency-survival-kits/","https://echo-sigma.com/","https://americansurvivalwholesale.com/","https://www.maydaysupplies.com/","https://www.primalsurvivor.net/mylar-space-blankets/","https://www.rei.com/c/camping-tents","https://www.timberland.com/shop/mens-boots","https://www.lowes.com/","https://www.coleman.com/coleman-sleepingbagsandbeds/","https://www.ramseyoutdoor.com/?SID=7vbjnejkqipdc8blj9n5eecej3","https://www.basspro.com/shop/en/camping","https://www.overstock.com/Sports-Toys/Camping-Hiking/2226/cat.html","https://mpgsport.com/collections/women?sscid=51k3_a95sy&utm_campaign=314743_851401&utm_medium=affiliate&utm_source=shareasale","https://www.welleco.com/","https://www.thirdlove.com/","https://www.sugarbearhair.com/","https://ritual.com/","https://www.chubbiesshorts.com/","https://www.stitchfix.com/","https://www.meundies.com/","https://www.glossier.com/","https://www.garnierusa.com/","https://www.katvondbeauty.com/sale","https://www.marcjacobsbeauty.com/","https://www.anastasiabeverlyhills.com/","https://www.chanel.com/us/makeup/p/172444/rouge-coco-ultra-hydrating-lip-colour/","https://www.makebeauty.com/","https://www.newbeauty.com/blog/skin-care/","https://www.loreal.com/","https://shop.goop.com/shop/collection/beauty/skincare/mask?country=USA","https://shop.goop.com/shop/products/revitalizing-day-moisturizer?taxon_id=622&country=USA","https://www.warbyparker.com/sunglasses/men","https://www.marriott.com/default.mi","https://www.priceline.com/","https://www.tripadvisor.com/","https://www.trivago.com/","https://www.kayak.com/","https://flights.idealo.com/","https://www.themileageclub.com/","https://www.united.com/en/us","https://www.gohawaii.com/islands/maui","https://www.booking.com/","https://visitmaldives.com/","https://www.travelzoo.com/","https://www.visitjamaica.com/plan-your-trip/","https://www.groupon.com/getaways","https://www.caribbeantravel.com/","https://www.expedia.com/Flights","https://www.kiragrace.com/giving-back/","https://www.prana.com/","https://carrotbananapeach.com/","https://www.earthyogaclothing.com/","https://www.greenappleactive.com/","https://teeki.com/","https://shop.lululemon.com/","https://asanarebel.com/","https://www.downdogapp.com/","https://www.glo.com/","https://www.headspace.com/","https://www.tenpercent.com/mindfulness-meditation-the-basics/","https://style.fabletics.com/dms25640/?bp=0&ccode=10078&clabel=Skimbit%20Ltd.&clickid=TvxSIqzSjxyJU210EWQ:NRupUkl16RVRwU1nTM0&code=DE27FD&iradid=252615&mpid=10078&pcode=Impact_Radius_Fabletics_US&plabel=&scode=&sharedid=&slabel=&utm_campaign=Impact_Radius_Fabletics_US_Skimbit%20Ltd.&utm_content=&utm_medium=affiliate&utm_source=IRS","https://www.caliastudio.com/f/calia-yoga","https://www.astrologyhub.com/the-top-7-best-selling-astrology-books/","https://www.healingcrystals.com/","https://www.sagegoddess.com/?gclid=EAIaIQobChMItM-475qZ4gIVCRgMCh3kgg4BEAAYAyAAEgKc7vD_BwE","https://i-d.vice.com/en_us","https://lovewellness.co/","https://juicebeauty.com/?ranMID=38268&ranEAID=TnL5HPStwNw&utm_source=Skimlinks.com&utm_medium=affiliate&utm_campaign=&ranSiteID=TnL5HPStwNw-Bl6LYgTaAvKprUai4FkqJw&siteID=TnL5HPStwNw-Bl6LYgTaAvKprUai4FkqJw&LSNSUBSITE=Omitted_TnL5HPStwNw","https://supergoop.com/","https://www.anthropologie.com/wellness","https://www.freepeople.com/wellness-products/","https://holistichealeronline.com/","https://shop.goop.com/shop/products/city-skin-potion-trio?taxon_id=1291&country=USA","https://fabfitfun.com/get-the-box/?step=getbox&origin=welcome","https://aloha.com/","https://www.maharose.com/","https://www.costarastrology.com/","https://www.gotoskincare.com/","https://www.lorealparisusa.com/","https://www.laprairie.com/","https://www.bareminerals.com/","https://www.urbandecay.com/","https://www.honestbeauty.com/products/creme-blush","https://www.firstaidbeauty.com/","https://www.narscosmetics.com/","https://www.stilacosmetics.com/","https://www.shopreedclarke.com/products?tag=Fiona%20Stiles%20Beauty","https://www.beccacosmetics.com/","https://www.eyeko.com/","https://www.proactiv.com/","https://www.kyliecosmetics.com/","https://www.allure.com/story/kylie-jenner-skin-care-products-prices-details","https://www.dermstore.com/product_Advanced+Night+Repair+Concentrated+Recovery+PowerFoil+Mask_77441.htm?gclid=CjwKCAjwq-TmBRBdEiwAaO1en9ZRE6ntl_8u-rSz0XqhkGaOYnH7zgQING_HaSBTkDXFfYNNj3WlQhoChAYQAvD_BwE&scid=scplp77441&sc_intid=77441&iv_=__iv_p_1_g_73713728321_c_347170226830_w_aud-318912418799%3Apla-313456374895_n_g_d_c_v__l__t__r_1o4_x_pla_y_6790012_f_online_o_77441_z_US_i_en_j_313456374895_s__e__h_9004338_ii__vi__&utm_source=fro&utm_medium=paid_search&utm_term=makeup&utm_campaign=505479","https://www.sephora.com/","https://www.ulta.com/skin-care-treatment-serums-face-masks?N=27hf","https://www.shiseido.com/","https://www.esteelauder.com/","https://www.dove.com/us/en/home.html","https://www.lushusa.com/","https://www.covergirl.com/","https://www.stives.com/","https://www.potionnaturals.com/","https://www.revolve.com/","https://www.maccosmetics.com/home","https://www.aesop.com/us/","https://www.sprezzabox.com/","https://www.adoreme.com/","https://www.allbirds.com/","https://www.outdoorvoices.com/","https://www.graze.com/us","https://www.drinkhint.com/"]

#input_list = ["https://www.msn.com", "https://www.yahoo.com"]

# Set a variable for the path to the local files (config.ini, etc.)
script_path = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(script_path, 'config.ini')

# Configuration file builder code
# Call buildNewConfigFile to create a new config.ini file.
def buildNewConfigFile():
	config = configparser.ConfigParser()
	config['DEFAULT'] = {'Input': 'urls.txt',
								'Passes': '1',
								'Tabs': '10',
								'Hold Time': '5',
								'Shuffle URLs': 'yes',
								'Minimize All': 'yes',
								'Max URLs': ''}
	with open(config_file, 'w') as configfile:
		config.write(configfile)

# Uncomment the next two lines and run the script to build a new config file.
# Re-comment the lines afterwards so script can function.
#buildNewConfigFile()
#exit()

# Argument handler
argP = argparse.ArgumentParser()

# Optional arguments
argP.add_argument("--input", help="A text file list of URLs you feed to the script. If a file isn't provided, a default list is used.", type=str, default=input_list)
argP.add_argument("--passes", help="Number of times to process the list. Default is 1.", type=int, default=1)
argP.add_argument("--tabs", help="Number of browser tabs to process in a batch. Opens x number of tabs at a time. Limit this based on available resources. Default is 10.", type=int, default=10)
argP.add_argument("--hold_time", help="Amount of time in seconds to wait for sites to load in a batch before closing the tabs. Default is 5.", type=int, default=5)
argP.add_argument("--shuffle_urls", help="Shuffles the list of URLs. Default is yes.", type=str, default='yes')
argP.add_argument("--minimize_all", help="Minimizes all windows to avoid closing the wrong window. Setting no will minimize only the active command prompt window used to launch the script. Default is yes.", type=str, default='yes')
argP.add_argument("--max_urls", help="Set the maximum number of URLs to load. Default processes all URLs in the supplied dictionary or default list.", type=int)

# Manual configuration argument
argP.add_argument("--conf", help="Reads configuration from config.ini instead of command line arguments.", action='store_true')
args = argP.parse_args()

# Initialize the configuration parser for manual configuration.
config = configparser.ConfigParser()

print("---- HTTP(S) Traffic Generator", "v" + str(version_string), "----\n")

# If --conf argument is supplied, read configuration file config.ini
#   and override argument variables with config file values.
if args.conf:
	print("--Executed using --conf argument.")
	config.read(config_file)
	print("--> Configuration file:", config_file)
	args.input = config['DEFAULT']['Input']
#	print("------", args.passes, type(args.passes))
	# The if/else blocks provide default settings if config.ini args are blank.
	# Default values are pulled from args.<argument_name> default set in argP.add_argument()
	if config['DEFAULT']['Passes'] == '':
		print("--> Passes argument is not set. Using default (%s pass)." % args.passes)
#		args.passes = args.passes
	else:
		args.passes = int(config['DEFAULT']['Passes'])
	if config['DEFAULT']['Tabs'] == '':
		print("--> Tabs argument is not set. Using default (%s tabs)." % args.tabs)
#		args.tabs = args.tabs
	else:
		args.tabs = int(config['DEFAULT']['Tabs'])
	if config['DEFAULT']['Hold Time'] == '':
		print("--> Hold Time argument is not set. Using default (%s seconds)." % args.hold_time)
#		args.hold_time = args.hold_time
	else:
		args.hold_time = int(config['DEFAULT']['Hold Time'])
	if config['DEFAULT']['Shuffle URLs'] == '':
		print("--> Shuffle URLs argument is not set. Using default (%s)." % args.shuffle_urls)
	else:
		args.shuffle_urls = config['DEFAULT']['Shuffle URLs']
	if config['DEFAULT']['Minimize All'] == '':
		print("--> Minimize All argument is not set. Using default (%s)." % args.minimize_all)
	else:
		args.minimize_all = config['DEFAULT']['Minimize All']
	if config['DEFAULT']['Max URLs'] == '':
		print("--> Max URLs argument is not set. No limit will be applied.")
	else:
		# If max_urls is not None, set to the configured value
		args.max_urls = int(config['DEFAULT']['Max URLs'])
	# This if statement is a little different because max_urls does not have a default value.
	# It is an integer if set, and None if not set. I commented this, but will
	# probably remove it. args.max_urls would only be set via CLI and must
	# have a value set. This essentially always hits because if the arg isn't
	# given, it's None. In this if it checks the arg, not config's value.
#	if args.max_urls is None:
#		print("hit")
#		# Sets max_urls to a blank string.
#		args.max_urls = config['DEFAULT']['Max URLs']
#		print(args.max_urls, type(args.max_urls))
#	else:
#		# If max_urls is not None, set to the configured value
#		args.max_urls = int(config['DEFAULT']['Max URLs'])


# Configuration summary
print("\n--Configuration summary:")
if args.passes:
	print("- Number of passes (--passes):", int(args.passes))

if args.tabs:
	print("- Tabs per batch (--tabs):", int(args.tabs))

if args.max_urls:
	print("- Maximum number of URLs (--max_urls):", int(args.max_urls))
else:
    print("- Maximum number of URLs not set (--max_urls): Processing all URLs.")

if args.hold_time:
	print("- Website loading hold time (--hold_time):", int(args.hold_time), "seconds")

if args.minimize_all:
		print("- Minimize all windows (--minimize_all):", args.minimize_all)

# If the input file argument is empty use the built in list.
if args.input == '':
	print("- Input file was not provided. Using built-in list.")
	args.input = input_list

# If the input file argument is True
if args.input:
#	print("Input file:", args.input)
	# If the object type of args.input is a list object...
	if "class 'list'" in str(type(args.input)):
		# Replace input_list (default list) with the argument value supplied.
		# I may need to refactor this as it is a bit confusing.
		# I think this will cover the case where the input_list is the default list passed by CLI argument.
		input_list = args.input
		print("- Input is a list of", str(len(input_list)), "URLs.")
	# Else (if the input argument is not a list assume its a file)
	else:
		# Make a copy of the input list in case of an exception reading the file.
		input_list_backup = input_list.copy()
		# Clear the input list before writing the input file to the list.
		input_list.clear()
		# Handle auto-correction of file paths for the input file
		if "\\" in args.input or "/" in args.input:
			pass
		else:
			args.input = os.path.join(script_path, args.input)
		try:
			with open(args.input, 'r') as openFile:
				for line in openFile:
					# If the line doesn't start with http prefix, add it and append to list.
					if line.startswith('http') == False:
						input_list.append("https://" + line)
					# Else if the line does start with http prefix, append to list.
					elif line.startswith('http') == True:
						input_list.append(line)
			print("- Input file (--input):", args.input, "(" + str(len(input_list)), "URLs)")
		except FileNotFoundError as e:
			print("- Input file not found. Using built-in list instead.\n--> Error:", e)
			input_list = input_list_backup.copy()
			input_list_backup.clear()
			print("- Input is a list of", str(len(input_list)), "URLs.")


if args.shuffle_urls:
	print("- Shuffle URLs (--shuffle_urls):", args.shuffle_urls)
	if args.shuffle_urls == 'yes':
		input_list = random.sample(input_list, k=len(input_list))

if args.max_urls:
#	print("hit", type(args.max_urls), type(args.passes))
	print("-", (int(args.max_urls) * int(args.passes)), "total URLs", "(" + str(args.max_urls), "input URLs multiplied by", str(args.passes) + ")\n")
#	print(input_list, type(input_list), type(args.max_urls), args.max_urls)
	input_list = random.sample(input_list, int(args.max_urls))
else:
	print("-", (len(input_list) * args.passes), "total URLs", "(" + str(len(input_list)), "input URLs multiplied by", str(args.passes) + ")\n")

# Print information when script is launched
print("-- !! IT IS VERY IMPORTANT THAT YOU REMAIN IDLE WHILE THE SCRIPT IS RUNNING. !! --")
print("-- ONCE THE SCRIPT IS DONE THE COMMAND PROMPT WILL BE RESTORED. PLEASE BE PATIENT.")
print("-- CTRL+C TO QUIT (CLOSE BROWSERS MANUALLY IF THE SCRIPT IS STOPPED DURING EXECUTION) --\n")
print("-- HIT THE 'SPACE BAR' TO CONTINUE OR 'CTRL+C' TO QUIT --\n")


# Pauses for user input to make sure they're ready.
try:
	keyboard.wait('space')
except KeyboardInterrupt:
	print("Cancelled.")
	exit()



# Checks if the threshold is divisible by 5, indicating 5 windows have opened
# If divisible by 5 (at every 5 windows opened), wait x seconds then close
# x number of windows.
# Accepts the index from processList and handles closing browsers
def closeSomeTabs(index):
	# Calculate if threshold is divisible by 5. Sets var to result
	# = 0 means no remainder. It is a factor of 5.
	# != 0 means remainder/not divisible by 5.
#	print(index+1, len(input_list))
#	print(index+1, args.max_urls, len(input_list))
	index_num = index
	index_result = index % (args.tabs-1)
	if index == 0:
#		print("first index")
		return
	if index+1 == args.max_urls:
#		print("if index+1 is max urls (index+1, max_urls, len of input list)", index+1, args.max_urls, len(input_list), index_result)
#		print("Hit URL limit.")
		time.sleep(args.hold_time) # Time for the sites to load
#		print("sent alt f4")
		keyboard.press_and_release('escape')
		time.sleep(0.2)
		keyboard.press_and_release('alt+f4')
		if args.passes > 1 and pass_counter < args.passes:
			time.sleep(3)
			webbrowser.open("http://", new=1, autoraise=True)
		return
	elif index+1 == len(input_list):
#		print(index+1, len(input_list))
#		print("if index+1 is len of input list (index+1, max_urls, len of input list)", index+1, args.max_urls, len(input_list), index_result)
		time.sleep(args.hold_time) # Time for the sites to load
#		print("sent alt f4")
		keyboard.press_and_release('escape')
		time.sleep(0.2)
		keyboard.press_and_release('alt+f4')
		return
#	close = index+1
	if index_result == 0:
#		print("if index result is 0 (index+1, max_urls, len of input list)", index+1, args.max_urls, len(input_list), index_result)
		time.sleep(args.hold_time) # Time for the sites to load
		# Closes the browser window.
#		print("sent alt f4")
		keyboard.press_and_release('escape')
		time.sleep(0.2)
		keyboard.press_and_release('alt+f4')
		# Wait 2 seconds and open a new browser window
		time.sleep(3)
		webbrowser.open("http://", new=1, autoraise=True)
		# Closes the tabs. This wasn't as clean as just closing the window. Damn pop-up tabs!
#		for i in range(0,close):
#			time.sleep(0.3)
#			print(i)
#			keyboard.press_and_release('ctrl+w')


# Processes the list and opens many many tabs.
# Don't blame me if your computer chokes :)
def processList(input_list):
	n = 0 # Index starts at 0
#	for line in input_list:
#		print(line)
#		if line not in urls:
#			print("Added", line)
#			urls.append(str(line).rstrip("\n"))
#		elif line in urls:
#			pass
#			print(line, "already in list")
#	if args.max_urls:
#		input_list = random.sample(input_list, args.max_urls)
	print("\n-- Pass #%s --" % pass_counter)
	try:
		for url in input_list:
			print(n+1, "-->", str(url).rstrip("\n")) # Prints index+1 to display 1.
#			webbrowser.open_new_tab(url)
			webbrowser.open_new_tab(str(url).rstrip("\n"))
			closeSomeTabs(n) # Sending index starting at 0
#			time.sleep(2)
#			keyboard.press_and_release('ctrl+w')
			n = n+1 # Increment index
	except KeyboardInterrupt:
		print("Aborted.")
		exit()
#	except:
#		raise()


# Minimize the command prompt window (should be the active window)
if args.minimize_all:
	if args.minimize_all == 'yes':
		keyboard.press_and_release('windows+m')
	else:
		keyboard.press_and_release('windows+down')
# Open a new web browser window (don't disturb other open browsers)
time.sleep(0.5)
webbrowser.open("http://", new=1, autoraise=True)
# Sleep momentarily so the browser window can open.
time.sleep(3)
pass_counter = 1
# Processes the file/list for the number of passes instructed.
for i in range(0,args.passes):
	processList(input_list)
	pass_counter = pass_counter+1
# Close the browser window.
#keyboard.press_and_release('alt+f4')
print("\nDone.")
# Sleep for a few seconds to give the browser windows time to close.
time.sleep(6)
# Send ALT+TAB shortcut to bring the command window back up.
#print("pressed alt tab")
keyboard.press_and_release('alt+tab')
#time.sleep(0.5)
#keyboard.press_and_release('windows+up')