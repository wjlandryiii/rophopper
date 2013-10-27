
def instructionString(inst):
	args = []
	for i in range(0, inst.getArgumentCount()):
		args += [inst.getFormattedArgument(i)]
	return inst.getInstructionString() + " " + ", ".join(args)

def instructionAtAddress(addr):
	inst = None	
	doc = Document.getCurrentDocument()
	seg = doc.getSegmentAtAddress(addr)
	try:
		inst = seg.getInstructionAtAddress(addr)
	except:
		inst = None
	return inst

def findAllRetsInRange(start, end):
	rets = []
	for addr in range(start, end):
		inst = instructionAtAddress(addr)
		if(inst != None):
			if inst.getInstructionString() == "ret" or inst.getInstructionString() == "retn":
				rets += [addr]
	return rets

def findSegmentByName(name):
	doc = Document.getCurrentDocument()
	for segment in doc.getSegmentsList():
		if segment.getName() == name:
			return segment
	return None


def findPreviousInstructions(addr):
	insts = []
	for x in range(1, 10):
		inst = instructionAtAddress(addr-x)
		if inst != None:
			if(inst.getInstructionLength() == x):
				if(inst.isAnInconditionalJump() == False and inst.isAConditionalJump() == False):
					insts += [addr-x]
	return insts


def findGadgetsStartAddress(addr):
	gadgets = []
	insts = findPreviousInstructions(addr)
	if len(insts) == 0:
		return [addr]
	for inst in insts:
		gadgets += findGadgetsStartAddress(addr - instructionAtAddress(inst).getInstructionLength())
	return gadgets


def printGadget(addr):
	print "GADGET:"
	inst = instructionAtAddress(addr)
	print "%08x:" % (addr), instructionString(inst)
	while(inst.isAnInconditionalJump() == False and inst.isAConditionalJump() == False):
		addr += inst.getInstructionLength()
		inst = instructionAtAddress(addr)
		print "%08x:" % (addr), instructionString(inst)
	print ""


def findGadgetsInSegment(seg):
	start = seg.getStartingAddress()
	end = seg.getStartingAddress() + seg.getLength()
	rets = findAllRetsInRange(start, end)
	gadgets = []
	for ret in rets:
		gadgets += findGadgetsStartAddress(ret)
	return gadgets


doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()

gadgets = findGadgetsInSegment(seg)

print "FOUND ", len(gadgets), " GADGETS"

for gadget in gadgets:
	printGadget(gadget)



