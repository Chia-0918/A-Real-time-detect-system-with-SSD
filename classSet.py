def getClass():
    dataClass = ['eclip_x',
                'eclip_xx',
                'railspike_x',
                'railspike_xx',
                'others_break',
                'eclip_is_covered',
                'rail_x',
                'rail_xx',
                'slab_track_eclip_xx',
                'slab_track_eclip_x']

    return dataClass

def getColor():
    classColor={0:(20, 255, 255), # yollow
                1:(18, 18, 255), # red
                2:(20, 255, 255),
                3:(18, 18, 255),
                4:(18, 18, 255),
                5:(20, 255, 255),
                6:(20, 255, 255),
                7:(18, 18, 255),
                8:(18, 18, 255),
                9:(20, 255, 255)}

    return classColor

"""
['eclip_break_x',
	'eclip_break_xx',
	'railspike_break_x',
	'railspike_break_xx',
	'others_break',
	'covered']

classcolor={0:(0.96, 0.14,0.14),1:(0.95, 1, 0.09),2:(0.96, 0.14,0.14),3:(0.95, 1, 0.09),4:(0.96, 0.14,0.14)}
#(0, 0.9, 0.01)green
#(255, 18, 18)red
#(0.95, 1, 0.09)yollow

"""