#
# Configuration...
#

MENUS_DEFS = { "clients":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFdDRm1sTDVndGpfcVplamRtRWllU2c&output=csv",\
	"partners":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEkzVm1qWE13MklHZ0Q5bk5VOEdzZlE&output=csv", \
	#"etcetera":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHNZR1hwZWswcXQ3NEIxSjQ0S0hpY3c&output=csv", \
	"mocap":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFdYUl96dkhhRnBLMFk0UWtsTGZxZnc&output=csv", \
	"axe":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDQ4dzNvVkczNWp6am1oUUJPeUNOSUE&output=csv", \
	"citypoly":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDlLa2VDc0dJWjNNdUxxRG9JcU9jTHc&output=csv", \
	#"interactive":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDdjLWp3cGFZbHk0bUdKNTZCMDlBcHc&output=csv", \
	#"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGlMZjVOSm40SzM1d1JBcW9IVjRIY3c&output=csv", \
	"storyboard":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEhLRGdYUXNvcjJvaWhWWXR2Y0tzYkE&output=csv", \
	"anim_cinem":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDRVRnBDUzQxbkdMbEUtRmsyM3Yza2c&output=csv", \
	"char_dev":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEpTc0V5dVhrdE5lbkVjbmRfU2paaVE&output=csv", \
	"motiondesign":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFhaNkRlLWp1OVZldDc3R0h4VldHdGc&output=csv", \
	"animation":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGMxeWcybnpzemtEVFdRbXlIS3ZtMWc&output=csv", \
	"appdesign":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGcxYXAtVElIbDNhVS1fSEYzcFVYSlE&output=csv", \
	"website":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFRXeE5Zc0tabHR2TzFfd1VNaTlvYWc&output=csv", \
	"touchscreen":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdDNPM0FEazYwNWVEZmtOZmpFajVzRGc&output=csv" \
	}

#
# Library...
#
import sys

import common
import gen_images
import gen_slide_shows
import gen_movies
import gen_movie_panels
import gen_multipage_slideshow
import gen_embeds

def create_option_script( asset_name, option, menus_dct ):
	menu_def = menus_dct[asset_name]
	script = ""
	for key in menu_def.keys():
		option_def = menu_def[key]
		for item in option_def:
			itemid = item["asset_name"]
			#script += "alert('%s');" % itemid
			if key == option:
				script += "document.getElementById('%s').style.visibility='visible';" % itemid
			else:
				script += "document.getElementById('%s').style.visibility='hidden';" % itemid
	return script

def create_option_scripts( asset_name, menus_dct ):
	script = {}
	menu_def = menus_dct[asset_name]
	for key in menu_def.keys():
		script[key] = create_option_script( asset_name, key, menus_dct )
	return script	

def expand_option( accum_ids, menu_name, menu_def, option_name, images_dct, action_scripts, init_hidden, \
	slide_shows_dct, movies_dct, mp_dct, is_dct, click_panels_dct, cpo_dct, embeds_dct ):

	option_def = menu_def[option_name]

	tot_style = ""
	tot_content = ""
	top_scripts = ""
	off_scriptlet = ""
	on_scriptlet= ""
	init_scriptlet = ""

	for item in option_def:
		asset_name = item["asset_name"]

		if asset_name.startswith("img"):
			# determine the script, if any...
			script = None
			ahref = None
			exturl = None
			if item.has_key("link") and item["link"]!="":
        			link = item["link"]
                		if link.startswith("option:"):
                			ltype,parm = link.split(":")
					funcname = "func_%s_%s" % (menu_name, parm)
                        		test = action_scripts[funcname]
					script = "%s ();" % funcname
				elif link.startswith("url:"):
					idx = link.find(":") + 1
					ahref = link[idx:]
                                elif link.startswith("nurl:"):
                                        idx = link.find(":") + 1
                                        ahref = link[idx:]
                                        exturl = True
				elif link.startswith("mss"):
					idx = link.find(":") + 1
					page_name = gen_multipage_slideshow.get_link( item, is_dct,"first")
					print "PAGEN->", page_name
					ahref = page_name
				else:
					print "ERROR: gen_menus: Unknown link type", asset_name, item
					sys.exit(1)	

			# determine initial css visibility, if any...
			init_vis = None
			if item.has_key("init") and item["init"]!="":
				init_vis = item["init"] 
			style, content, script, scriptlet_dct = gen_images.expand_item( accum_ids, item, images_dct, script, init_vis, ahref, exturl )

			tot_style += style
			tot_content += content
			top_scripts += script

			# accumulate on/off scriptlet...
			off_scriptlet += scriptlet_dct['off']	
			on_scriptlet += scriptlet_dct['on']	
			init_scriptlet += scriptlet_dct['init']

		elif asset_name.startswith("ss"):
			print "MENU - CALLING GEN SLIDE SHOWS EXPAND", asset_name, "cp->", click_panels_dct.keys()

			style, content, top_script, scriptlet_dct = gen_slide_shows.expand_item( accum_ids, item, images_dct, movies_dct, \
				mp_dct, click_panels_dct, slide_shows_dct, cpo_dct, embeds_dct )

			tot_style += style
			tot_content += content
			top_scripts += top_script

			# accumulate on/off scriptlet...
                        off_scriptlet += scriptlet_dct['off']
                        on_scriptlet += scriptlet_dct['on']
			init_scriptlet += scriptlet_dct['init']
			print "ss init->", init_scriptlet

                elif asset_name.startswith("mov"):
                        style, content, scr_dct = gen_movies.expand_item( accum_ids, item, images_dct, movies_dct )
                        tot_style += style
                        tot_content += content
               
			off_scriptlet += scr_dct['off']
                        on_scriptlet += scr_dct['on']
			init_scriptlet += scr_dct['init']


		elif asset_name.startswith("mp"):
			style, content, scr_dct = gen_movie_panels.expand_item( accum_ids, item, images_dct, movies_dct, mp_dct, embeds_dct )
			tot_style += style
			tot_content += content

			off_scriptlet += scr_dct['off']
			on_scriptlet += scr_dct['on']
			init_scriptlet += scr_dct['init']

		elif asset_name.startswith("embed"):
			style, content, foo, scr_dct = gen_embeds.expand_item( accum_ids, item, embeds_dct, images_dct, None, None )
			tot_style += style
			tot_content += content

			off_scriptlet += scr_dct['off']
			on_scriptlet += scr_dct['on']
			init_scriptlet += scr_dct['init']
		

		else:
			print "ERROR: gen_menus: Can't process asset->", asset_name, item
			sys.exit(1)



	scriptlet_dct = {}
	scriptlet_dct['on'] = on_scriptlet
	scriptlet_dct['off'] = off_scriptlet
	scriptlet_dct['init'] = init_scriptlet

	return [ tot_style, tot_content, top_scripts, scriptlet_dct ]

def expand_item(accum_ids, item, images_dct, menus_dct, slide_shows_dct, movies_dct, mp_dct, is_dct, click_panels_dct, cpo_dct, embeds_dct ):

	print "MENU EXPAND", "cp->", click_panels_dct.keys()

	menu_name = item["asset_name"]
	menu_def = menus_dct[menu_name]

	# pre the global scripts from scriptlets...
	action_scripts = {}
	for option in menu_def.keys():
		funcname = "func_%s_%s" % ( menu_name, option )
		action_scripts[ funcname ] = None

	# get init option, if any...
	init_option_name = None
	if item.has_key("init"):
		val = item["init"]
		if val.startswith("option:"):
			foo, init_option_name = val.split(":")
			print foo, init_option_name

	# iterate individual assets and expand...
	tot_style = ""
	tot_content = ""
	top_script = ""
	scriptlets_dct = {}
	init_script = False

	# iterate the options...
	for option in menu_def.keys():
		item_def = menu_def[option]
		style, content, script, scriptlet_dct = expand_option( \
			accum_ids, menu_name, menu_def, option, images_dct, action_scripts, True, slide_shows_dct, \
				movies_dct, mp_dct, is_dct, click_panels_dct, cpo_dct, embeds_dct )
		tot_style += style
		tot_content += content
		top_script += script
		scriptlets_dct[option] = scriptlet_dct

		# possibly use this option as init...
		print "options->", option, init_option_name
		if not init_script and option == init_option_name:
			# your problem might be here!
			init_script = scriptlets_dct[option]['init']
			print "menu option init->", init_script

        # create a total off scriplet for menu...
        tot_off = ""
        for option in scriptlets_dct.keys():
                tot_off += scriptlets_dct[option]['off']
        
	# create a total on scriplet for menu...
        tot_on = ""
        for option in scriptlets_dct.keys():
                tot_on += scriptlets_dct[option]['on']

	# finalize the action script dct...
	for option in menu_def.keys():
		funcname = "func_%s_%s" % ( menu_name, option )
		funcdef = "function %s () { %s };" % ( funcname, tot_off + scriptlets_dct[option]['on'] )
		action_scripts[ funcname ] = funcdef
	
	# append to header script...
	for item in action_scripts.keys():
		top_script += "\n\n" + action_scripts[item]

	# scriptlet dct...
	scriptlet_dct = {}
	scriptlet_dct['off'] = tot_off
	scriptlet_dct['on'] = tot_on
	print tot_off, init_script
	scriptlet_dct['init'] = tot_off + init_script

	print "MENU SCRIPTLET INIT->", init_script

	return [ tot_style, tot_content, top_script, scriptlet_dct ]

def get_dct( pagekeys=None ):

	if pagekeys==None:
		pagekeys = MENUS_DEFS.keys()

	newdct = {}
	for code in pagekeys:	
		if ( not code in MENUS_DEFS.keys()): continue
		items = common.parse_spreadsheet1( MENUS_DEFS[code] , "menus %s" % code )
		dct = common.dct_join( items,'menu_name','option_name')
		for ky in dct.keys():
			newdct[ky] = dct[ky]	
	return newdct

if __name__ == "__main__":
	dct = get_dct()
	print dct
