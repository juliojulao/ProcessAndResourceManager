import RCB

global PCB_list
global curr_proc
global RL

class Process:
	def __init__(self, pid, state, parent, children, resources, priority):
		self.pid = pid
		self.state = state
		self.parent = parent
		self.children = children
		self.resources = resources
		self.priority = priority


	def __str__(self):
		return "\tPID: {}\n\tState: {}\n\tParent: {}\n\tChildren: {}\n\tResources: {}\n\tPriority: {}\n".format(self.pid,self.state,
			self.parent,self.children,self.resources,self.priority)


	def __repr__(self):
		return "Process {}".format(self.pid)


	def create(self,p):
		global RL
		if p > 2 or p <= 0:
			raise Exception
		free_PCB = get_free_PCB()
		proc = Process(free_PCB, 'ready', curr_proc.pid, [], {}, p)
		PCB_list[free_PCB] = proc
		self.children.append(proc)
		RL[p].append(proc)
		scheduler()


	def process_exists(self,j):
		# print("checking existence of {}".format(j))
		for i in self.children:
			if type(i) != int and j == i.pid:
				# print("{} exists".format(j))
				return True
		if j == self.pid:
			# print("{} exists/is self".format(j))
			return True
		# print("{} does not exist".format(j))
		raise Exception


	def find_WL(self,j):
		# print("looking in waitlist")
		for i in RCB.RCB_list:
			# print(i.ind)
			for k in i.waitlist:
				if j == k[0].pid:
					# print("{} found in waitlist".format(j))
					# print(i.ind,k)
					return (i.ind,k)


	def destroy_recur(self,j):
		global RL
		# print(PCB_list)
		l = self.get_tree(j)
		# print(l)
		for k in l:
			# print("Children of parent of {}: {}".format(k.pid,PCB_list[PCB_list[k.pid].parent].children))
			PCB_list[PCB_list[k.pid].parent].children.remove(PCB_list[k.pid])
			if PCB_list[k.pid] in RL[int(PCB_list[k.pid].priority)]:
				RL[int(PCB_list[k.pid].priority)].remove(PCB_list[k.pid])
			else:
				# print("Looking in waitlist")
				wl = self.find_WL(k.pid)
				RCB.RCB_list[wl[0]].waitlist.remove(wl[1])
			PCB_list[k.pid].release_all_resources()
			PCB_list[k.pid] = 0
			# print("Process {} destroyed".format(k.pid))
		self.update_RCB()
		scheduler()


	def get_tree(self,j):
		if self.process_exists(j):
			l = []
			if PCB_list[j].children == []:
				l.append(PCB_list[j])
				return l
			def recur(j,l):
				for k in PCB_list[j].children:
					recur(k.pid,l)
				l.append(PCB_list[j])
		recur(j,l)
		return l


	def request(self, r, k):
		global RL
		# print(self)
		# print("Current request by {} for {} units of resource {}".format(self.pid,r,k))
		if self.pid == 0 or k < 1:
			raise Exception
		if k > RCB.RCB_list[r].inventory:
			raise Exception
		if r in self.resources and k + self.resources[r] > RCB.RCB_list[r].inventory:
			raise Exception
		if k <= RCB.RCB_list[r].available:
			RCB.RCB_list[r].available -= k
			if r not in self.resources:
				self.resources[r] = k
			else:
				self.resources[r] += k
			# if (self,k) in RCB.RCB_list[r].waitlist:
				# RCB.RCB_list[r].waitlist.remove((self,k))
		else:
			self.state = 'blocked'
			RL[int(self.priority)].remove(self)
			RCB.RCB_list[r].waitlist.append((self,k))
			# print(RCB.RCB_list[r].waitlist)
			scheduler()


	def release(self, r, k):
		global RL
		# print("Releasing process {} of {} units in Resource {}".format(self.pid,k,r))
		# print(RCB.RCB_list)
		if k > self.resources[r] or r not in self.resources:
			raise Exception

		self.resources[r] -= k
		RCB.RCB_list[r].available += k
		if self.resources[r] == 0:
			del self.resources[r]

		if len(RCB.RCB_list[r].waitlist) == 0:
			# print("waitlist empty")
			pass
		else:
			# print(self)
			self.update_RCB()
		# 	# procj = RCB.RCB_list[r].waitlist[0][0]
		# 	# RL[int(procj.priority)].append(procj)
		# 	# procj.state = 'ready'
		# 	# procj.request(r,RCB.RCB_list[r].waitlist[0][1])
		# 	# del RCB.RCB_list[r].waitlist[0]
		# # print("Released {} of {} units".format(r,k))
		# self.update_RCB()
		scheduler()


	def update_RCB(self):
		l = []
		for r in RCB.RCB_list:
			for proc,amt in r.waitlist:
				print(proc.pid)
				if amt <= r.available:
					RL[int(proc.priority)].append(proc)
					proc.state = 'ready'
					proc.request(r.ind,amt)
					l.append((proc,amt))
					# r.waitlist.remove((proc,amt))
					# print(r.waitlist)
				else:
					break
			for i in l:
				if i in r.waitlist:
					print(r.waitlist)
					r.waitlist.remove(i)


	def release_all_resources(self):
		for k,v in self.resources.items():
			RCB.RCB_list[k].available += v


def scheduler():
	global curr_proc
	if len(RL[2]) > 0:
		curr_proc = RL[2][0]
		# print("RL 2")
	elif len(RL[1]) > 0:
		curr_proc = RL[1][0]
		# print("RL 1")
	elif len(RL[0]) > 0:
		curr_proc = RL[0][0]


def timeout():
	global curr_proc
	head = RL[int(curr_proc.priority)].pop(0)
	# print(head)
	RL[int(curr_proc.priority)].append(head)
	scheduler()


def get_free_PCB():
	for i, val in enumerate(PCB_list):
		if val == 0:
			return i
	raise Exception







		