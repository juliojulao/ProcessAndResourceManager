global RCB_list

class RCB:
	def __init__(self, ind, inventory, available, waitlist):
		self.ind = ind
		self.inventory = inventory
		self.available = available
		self.waitlist = waitlist

	def __str__(self):
		return "\tIndex: {}\n\tState: {}\n\tWaitlist: {}".format(self.ind,self.state,self.waitlist)

	def __repr__(self):
		return "\n(Resource {}, Max: {}, Available: {}, Waitlist: {})".format(self.ind,self.inventory,self.available,self.waitlist)



