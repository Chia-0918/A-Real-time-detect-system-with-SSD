def getClass():
    dataClass = ['eclip_break_x',
                'eclip_break_xx',
                'railspike_break_x',
                'railspike_break_xx',
                'others_break',
                'covered']


    return dataClass

def getColor():
    classColor={0:(0.96, 0.14,0.14),1:(0.95, 1, 0.09),2:(0.96, 0.14,0.14),3:(0.95, 1, 0.09),4:(0.96, 0.14,0.14)}

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
#(0.96, 0.14,0.14)red
#(0.95, 1, 0.09)yollow

"""